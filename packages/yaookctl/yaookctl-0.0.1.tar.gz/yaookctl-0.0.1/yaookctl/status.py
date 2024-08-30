import asyncio
import json
import typing
from datetime import datetime

import prettytable

import kubernetes_asyncio.client as kclient

from .data import (
    NODE_PROFILES,
)

ParentKey = typing.Tuple[str, str, str]
WorkloadMapInner = typing.Mapping[str, typing.Sequence[typing.Any]]
WorkloadMap = typing.Mapping[ParentKey, WorkloadMapInner]


def extract_eviction_status(
        message: typing.Optional[str],
) -> typing.Optional[str]:
    if message is None:
        return None

    try:
        structured = json.loads(message)
    except ValueError:
        return message or None

    migrated = structured.get("migrated")
    migratable = structured.get("migratable")
    pending = structured.get("pending")
    in_progress = structured.get("in_progress")
    unhandleable = structured.get("unhandleable")
    unhandleable_agent = structured.get("unhandleable_agent", False)

    total: typing.Optional[int] = None
    if migrated is not None:
        # we have to go through a different variable name here, otherwise mypy
        # doesn't get that `total` is not None in this branch
        known_total = migrated
        known_total += migratable or 0
        known_total += pending or 0
        known_total += in_progress or 0
        known_total += unhandleable or 0
        total = known_total

    parts = []
    if total is not None:
        assert migrated is not None
        if total == 0:
            done = 1
        else:
            done = migrated / total
        parts.append(f"{done * 100:.0f}% done")

    if pending is not None or migratable is not None:
        todo = (pending or 0) + (migratable or 0)
        parts.append(f"{todo} todo")

    if unhandleable is not None:
        parts.append(f"{unhandleable} stuck")

    if unhandleable_agent:
        parts.insert(0, "agent stuck!")

    return " ".join(parts)


def extract_status(
        cr: typing.Mapping,
) -> typing.Optional[
    typing.Tuple[str, typing.Optional[datetime], typing.Optional[str]]
]:
    conditions = cr.get("status", {}).get("conditions", [])
    condition_map: typing.Mapping[str, typing.Mapping[str, str]] = {
        condition["type"]: condition
        for condition in conditions
    }

    try:
        converged_condition = condition_map["Converged"]
    except KeyError:
        return None

    message = None
    status = converged_condition["reason"]

    enabled_status = ""
    enabled_lastTransitionTime = ""
    try:
        enabled_condition = condition_map["Enabled"]
    except KeyError:
        pass
    else:
        enabled_status = enabled_condition["status"]
        enabled_lastTransitionTime = enabled_condition["lastTransitionTime"]

    try:
        evicted_condition = condition_map["Evicted"]
    except KeyError:
        pass
    else:
        if (evicted_condition["status"] != "NotEvicting"
                and not (enabled_status == "True"
                         and enabled_lastTransitionTime
                         > evicted_condition["lastTransitionTime"])):
            message = message or extract_eviction_status(
                evicted_condition.get("message")
            ) or evicted_condition["status"]
            status = evicted_condition["status"]

    message = message or converged_condition.get("message")

    try:
        target_release = cr["spec"]["targetRelease"]
        installed_release = cr["status"]["installedRelease"]
    except KeyError:
        pass
    else:
        if target_release != installed_release:
            upgrade_notice = \
                f"upgrading: {installed_release} → {target_release}"
            if not message:
                message = upgrade_notice
            else:
                message = f"{message}\n{upgrade_notice}"

    last_transition_time = None \
        if converged_condition.get("lastTransitionTime") is None \
        else datetime.strptime(converged_condition["lastTransitionTime"],
                               "%Y-%m-%dT%H:%M:%SZ")

    return (
        status,
        last_transition_time,
        message or None,
    )


async def get_workloads(
        client: kclient.ApiClient,
        namespace: str,
) -> WorkloadMap:
    apps_v1 = kclient.AppsV1Api(client)
    futures = [
        apps_v1.list_namespaced_deployment(namespace),
        apps_v1.list_namespaced_daemon_set(namespace),
        apps_v1.list_namespaced_stateful_set(namespace),
    ]

    map: typing.Dict[ParentKey, typing.Dict[str, typing.List[typing.Any]]] = {}

    deployments, daemonsets, statefulsets = await asyncio.gather(*futures)
    for (kind, result) in (("deploy", deployments),
                           ("ds", daemonsets),
                           ("sts", statefulsets)):
        for item in result.items:
            labels = item.metadata.labels or {}
            try:
                parent_plural = labels["state.yaook.cloud/parent-plural"]
                parent_name = labels["state.yaook.cloud/parent-name"]
                parent_group = labels["state.yaook.cloud/parent-group"]
            except KeyError:
                continue
            map.setdefault(
                (parent_group, parent_plural, parent_name),
                {},
            ).setdefault(kind, []).append(item)

    return map


def is_workload_healthy(
        kind: str,
        item: typing.Any,
) -> bool:
    if kind == "deploy" or kind == "sts":
        if item.status and item.status.ready_replicas == item.status.replicas:
            return True
        return False
    elif kind == "ds":
        status = item.status
        if status and status.number_ready == status.desired_number_scheduled:
            return True
        return False
    raise NotImplementedError(
        f"{kind} healthcheck support not implemented yet",
    )


def check_workloads(
        workloads: WorkloadMap,
        parent_group: str,
        parent_plural: str,
        parent_name: str,
) -> typing.Sequence[typing.Tuple[str, typing.Any]]:
    unhealthy = []
    for kind, items in workloads.get(
            (parent_group, parent_plural, parent_name), {}).items():
        for item in items:
            if not is_workload_healthy(kind, item):
                unhealthy.append((kind, item))

    return unhealthy


def get_node_profiles(
        node_label_map: typing.Mapping[str, str],
        ) -> typing.Collection[str]:
    node_label_set = set(node_label_map.keys())
    selected_labels: typing.Set[str] = set()
    result = set()
    # We iterate profiles so that we look at those with the most labels first.
    # That allows us to show the most generic profiles which apply for a node,
    # saving space.
    for profile_name, labels in sorted(
            NODE_PROFILES.items(),
            key=lambda x: len(x[1]),
            reverse=True):
        # Only consider profiles which have not been fully covered by other
        # profiles yet.
        if labels & selected_labels == labels:
            continue
        if labels & node_label_set != labels:
            continue
        selected_labels |= labels
        result.add(profile_name)

    return result


def evaluate_agent_status(agent: typing.Mapping) -> str:
    status = agent.get("status", {}).get("conditions", [])
    try:
        enabled_cond = [
            cond
            for cond in status if cond["type"] == "Enabled"
        ][0]
    except IndexError:
        return "spawning"
    try:
        converged_cond = [
            cond
            for cond in status if cond["type"] == "Converged"
        ][0]
    except IndexError:
        return "spawning"

    enabled = enabled_cond["status"]
    converged = converged_cond["reason"]

    try:
        eviction_cond = [
            cond
            for cond in status if cond["type"] == "Evicted"
        ][0]
    except IndexError:
        eviction = ""
    else:
        eviction = eviction_cond["status"]

    if enabled == "True":
        if converged != "Success":
            return f"{converged.lower()}+up"
        return "up"
    elif enabled == "False":
        if ((converged == "Dependency" or converged == "InProgress")
                and eviction == "Evicting"):
            return "evicting"
        if converged != "Success":
            return f"{converged.lower()}+disabled"
        return "disabled"
    else:
        return enabled.lower()


def evaluate_node_status(node: kclient.V1Node) -> str:
    status = node.status.conditions
    ready_cond = [
        cond for cond in status
        if cond.type == "Ready"
    ][0]
    if ready_cond.status == "True":
        return "ready"
    elif ready_cond.status == "False":
        return "unready"
    else:
        return ready_cond.status.lower()


async def status_table(
        client: kclient.ApiClient,
        namespace: str,
        resource_types: typing.Iterable[typing.Tuple[str, str, str, str]],
) -> prettytable.PrettyTable:
    custom = kclient.CustomObjectsApi(client)
    tbl = prettytable.PrettyTable()
    tbl.field_names = ["Kind", "Name", "Status", "Since", "Message",
                       "Workloads"]
    tbl.align = "l"

    futures = [
        custom.list_namespaced_custom_object(group, version, namespace, plural)
        for (group, version, plural, kind) in resource_types
    ]
    workloads, existing_resources = await asyncio.gather(
        get_workloads(client, namespace),
        asyncio.gather(*futures, return_exceptions=True),
    )

    for ((group, version, plural, kind), result) in zip(
            resource_types,
            existing_resources):
        if isinstance(result, kclient.exceptions.ApiException):
            if result.status == 404:
                items = []
            else:
                raise result
        elif isinstance(result, BaseException):
            raise result
        else:
            items = result["items"]
        if not items:
            tbl.add_row((kind, "<absent>", "", "", "", ""))
        for item in items:
            name = item["metadata"]["name"]
            status_data = extract_status(item)
            if status_data is None:
                status, since, message = "pending", "", None
            else:
                status, since_dt, message = status_data
                since = str(since_dt)
            unhealthy = "\n".join(
                f"{kind}/{item.metadata.name} is unhealthy"
                for (kind, item) in check_workloads(
                    workloads, group, plural, name,
                )
            ) or "all ready"
            tbl.add_row((kind, name, status, since, message or "", unhealthy))
    return tbl
