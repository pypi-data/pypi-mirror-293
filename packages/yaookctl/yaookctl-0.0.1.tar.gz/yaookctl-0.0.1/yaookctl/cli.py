import asyncio
import contextlib
import functools
import os
import typing
import subprocess
import sys
from datetime import datetime

import click
import click.shell_completion
from click_option_group import optgroup, MutuallyExclusiveOptionGroup
import prettytable

import aiohttp
import kubernetes_asyncio.client as kclient

import yaookctl.logs
import yaookctl.debugger
import yaookctl.galera
import yaookctl.ovsdb
from yaookctl.data import (
    OPENSTACK_RESOURCES,
    INFRA_RESOURCES,
    CREDENTIAL_RESOURCES,
    KIND_MAP,
    UPGRADABLE_KINDS,
    API_GROUP_MAP,
    MULTI_INSTANCE_PLURALS,
    DATABASE_ALIAS_MAP,
)
from yaookctl.lookups import (
    find_any_pod,
    find_downscaled_mysqlservice_sts,
    find_downscaled_ovsdbservice_sts,
    find_single_container,
    find_unique_object,
    get_component_label_selector,
    get_mysqlservice_label_selector,
)
from yaookctl.status import (
    get_node_profiles,
    evaluate_agent_status,
    evaluate_node_status,
    status_table,
)
from yaookctl.cliutil import (
    blocking,
    get_namespace,
    kubernetes_client,
    with_client,
)
from yaookctl.completion import (
    fixed_shell_complete,
    kind_shell_complete,
    name_shell_complete,
    target_shell_complete,
    upgradable_kind_shell_complete,
    component_shell_complete,
)


SPINNER = "|/-\\"


PAUSE_ANNOTATION = "state.yaook.cloud/pause"
PAUSE_ANNOTATION_JSONPATCH = PAUSE_ANNOTATION.replace("/", "~1")


HELP_CONTAINER_OPTION = """
Force to use a different container than the default for the given
kind and component
"""
HELP_COMPONENT_OPTION = """
Select a specific component of the given KIND, instead of the
default.

Components are defined in the corresponding operator code; they are
the left-hand side of the assignments in the custom resource class
definition in the python code.
"""


class SpinFun(typing.Protocol):
    def __call__(self, text: typing.Optional[str] = None) -> None:
        pass


@contextlib.contextmanager
def spinner(
        text: typing.Optional[str] = None,
) -> typing.Iterator[SpinFun]:
    i = 0

    def spin(text: typing.Optional[str] = text) -> None:
        nonlocal i
        i = (i + 1) % len(SPINNER)
        print(f"{SPINNER[i]} {text}", end="\r")

    try:
        yield spin
    finally:
        # clear the line
        print("\x1b[J")


def kubectl_argv(
        ctx: click.Context,
        *args: typing.Union[str, bytes]
) -> typing.List[typing.Union[str, bytes]]:
    argv: typing.List[typing.Union[str, bytes]] = ["kubectl"]
    try:
        context = ctx.obj["context"]
    except KeyError:
        pass
    else:
        if context is not None:
            argv.extend(("--context", context))
    try:
        argv.extend(("-n", ctx.obj["namespace"]))
    except KeyError:
        pass
    argv.extend(args)
    return argv


async def kubectl_block(
        ctx: click.Context,
        *args: typing.Union[str, bytes],
) -> None:
    argv = kubectl_argv(ctx, *args)
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdin=None,
        stdout=None,
        stderr=None,
    )
    await proc.wait()
    assert proc.returncode is not None  # for mypy mostly
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, argv)


def kubectl(
        ctx: click.Context,
        *args: typing.Union[str, bytes],
) -> None:
    argv = kubectl_argv(ctx, *args)
    os.execvp("kubectl", argv)


@click.group()
@click.option("-n", "--namespace")
@click.option("-c", "--context")
@click.pass_context
def main(
        ctx: click.Context,
        namespace: str,
        context: str,
) -> None:
    ctx.ensure_object(dict)

    ctx.obj["namespace"] = get_namespace(namespace)
    ctx.obj["context"] = context


@main.group()
def status() -> None:
    """
    Show the status of various yaook components.
    """
    pass


@status.command("openstack")
@with_client
async def status_openstack(
        ctx: click.Context,
        client: kclient.ApiClient,
) -> None:
    """
    Show the status of the openstack services.
    """
    namespace = ctx.obj["namespace"]
    tbl = await status_table(client, namespace, OPENSTACK_RESOURCES)
    print(tbl)


@status.command("infra")
@with_client
async def status_infra(
        ctx: click.Context,
        client: kclient.ApiClient,
) -> None:
    """
    Show the status of infra services (db, rabbitmq, memcached).
    """
    namespace = ctx.obj["namespace"]
    tbl = await status_table(client, namespace, INFRA_RESOURCES)
    tbl.sortby = "Name"
    print(tbl)


@status.command("credentials")
@with_client
async def status_credentials(
        ctx: click.Context,
        client: kclient.ApiClient,
) -> None:
    """
    Show status of various users and endpoints.
    """
    namespace = ctx.obj["namespace"]
    tbl = await status_table(client, namespace, CREDENTIAL_RESOURCES)
    print(tbl)


@status.command("nodes")
@with_client
async def status_nodes(
        ctx: click.Context,
        client: kclient.ApiClient,
) -> None:
    """
    Show status of kubernetes nodes.
    """
    namespace = ctx.obj["namespace"]
    core_v1 = kclient.CoreV1Api(client)
    custom = kclient.CustomObjectsApi(client)
    nodes, l2_agents, l3_agents, dhcp_agents, computes = await asyncio.gather(
        core_v1.list_node(),
        custom.list_namespaced_custom_object(
            "network.yaook.cloud", "v1", namespace, "neutronl2agents",
        ),
        custom.list_namespaced_custom_object(
            "network.yaook.cloud", "v1", namespace, "neutronl3agents",
        ),
        custom.list_namespaced_custom_object(
            "network.yaook.cloud", "v1", namespace, "neutrondhcpagents",
        ),
        custom.list_namespaced_custom_object(
            "compute.yaook.cloud", "v1", namespace, "novacomputenodes",
        ),
    )

    l2_agent_map = {
        item["metadata"]["name"]: item
        for item in l2_agents["items"]
    }
    l3_agent_map = {
        item["metadata"]["name"]: item
        for item in l3_agents["items"]
    }
    dhcp_agent_map = {
        item["metadata"]["name"]: item
        for item in dhcp_agents["items"]
    }
    compute_map = {
        item["metadata"]["name"]: item
        for item in computes["items"]
    }

    tbl = prettytable.PrettyTable()
    tbl.field_names = ["Name", "Profile", "Status", "L2", "Agents"]
    tbl.align = "l"

    for node in nodes.items:
        node_name = node.metadata.name
        profiles = get_node_profiles(node.metadata.labels or {})
        l2_agent = l2_agent_map.get(node_name)
        l3_agent = l3_agent_map.get(node_name)
        dhcp_agent = dhcp_agent_map.get(node_name)
        compute = compute_map.get(node_name)

        statuses = []
        if l3_agent is not None:
            statuses.append(f"l3: {evaluate_agent_status(l3_agent)}")
        if dhcp_agent is not None:
            statuses.append(
                f"dhcp: {evaluate_agent_status(dhcp_agent)}",
            )
        if compute is not None:
            statuses.append(f"compute: {evaluate_agent_status(compute)}")

        tbl.add_row((
            node_name,
            "+".join(sorted(profiles)),
            evaluate_node_status(node),
            evaluate_agent_status(l2_agent) if l2_agent else "--",
            ", ".join(statuses) if statuses else "--",
        ))

    tbl.sortby = "Name"

    print(tbl)


@main.command("shell")
@with_client
@click.option(
    "-c", "--container",
    help=HELP_CONTAINER_OPTION,
)
@click.option(
    "-p", "-C", "--pod", "--component",
    help=HELP_COMPONENT_OPTION,
    shell_complete=component_shell_complete,
)
@click.argument("kind", shell_complete=kind_shell_complete)
@click.argument("target", shell_complete=target_shell_complete, required=False)
async def shell(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str,
        target: typing.Optional[str],
        container: typing.Optional[str],
        pod: typing.Optional[str],
) -> None:
    """
    Create a shell to the target pod specified by KIND and TARGET..

    KIND may be one of: openstack, {KIND}

    If KIND is openstack, this command behaves like yaookctl openstack shell,
    and TARGET is interpreted as keystone-ref argument, if given. It is not
    possible to pass an image or external-keystone-ref to this alias; use
    yaookctl openstack shell directly instead. Passing a container or pod is
    not supported and will fail with an error.

    Example:

        $ yaook shell compute node-1
    """
    if kind.lower().strip() == "openstack":
        if container is None and pod is None:
            return await openstack_shell_impl(ctx, client, target, None, None)
        else:
            raise click.ClickException(
                "yaookctl shell openstack does not support passing container "
                "or pod"
            )
    elif target is None:
        raise click.ClickException(
            "TARGET must be given (unless for yaookctl shell openstack)"
        )

    namespace = ctx.obj["namespace"]
    try:
        pod_obj, container = await find_single_container(
            client, namespace, kind, target, container, pod,
        )
    except (LookupError, ValueError) as exc:
        if not isinstance(exc, click.ClickException):
            raise click.ClickException(str(exc))
        raise

    return kubectl(
        ctx, "exec", "-it", "-c", container, pod_obj.metadata.name,
        "--", "/bin/bash",
    )


@main.command("logs")
@with_client
@click.option(
    "-c", "--container",
    help=HELP_CONTAINER_OPTION,
)
@click.option(
    "-p", "-C", "--pod", "--component",
    help=HELP_COMPONENT_OPTION,
    shell_complete=component_shell_complete,
)
@click.option(
    "--all/--not-all",
    help="""
    Select all targets of a multi-instance service (such as Neutron L3 or OVN
    agents).
    """,
    default=False,
)
@click.option(
    "-n", "--show-name/--no-show-name",
    help="""
    Prefix all log messages with the pod name which originated them.
    """,
    default=False,
)
@click.option(
    "--tail",
    help="""
    Number of log messages to fetch before the current instant. In contrast to
    other tools like kubectl or docker, the default of this option is 0. Note
    that older log messages are not interleaved correctly, i.e. you will see
    backward jumps in times because the historic logs from different pods are
    fetched in batches.
    """,
    type=int,
    default=0,
)
@click.argument("kind", shell_complete=kind_shell_complete)
@click.argument("target", shell_complete=target_shell_complete,
                required=False)
async def logs(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str,
        target: typing.Optional[str],
        container: typing.Optional[str],
        pod: typing.Optional[str],
        show_name: bool,
        all: bool,
        tail: int,
) -> None:
    """
    Access logs of a specific KIND of k8s objects. If more than one target is
    found then TARGET must point to a instance of KIND or --all must be passed.

    KIND may be one of: {KIND}, or any Yaook CR plural (e.g. amqpservers).

    Example:

        $ yaook logs compute node-1
    """
    namespace = ctx.obj["namespace"]
    async with yaookctl.logs.LogViewer(
            client,
            show_name=show_name) as log_viewer:
        kind = KIND_MAP.get(kind, kind)
        group = API_GROUP_MAP.get(kind, "yaook.cloud")
        if kind in MULTI_INSTANCE_PLURALS:
            if target is None and not all:
                print(
                    "error: --all must be explicitly given when selecting all"
                    "instances of an multi-instance resource, as that may "
                    "cause a high load on both local and remote systems.",
                    file=sys.stderr,
                )
                sys.exit(2)
            instance_name = target
            component = pod
        else:
            if pod is not None and target is not None:
                print(
                    "error: -p/-C/--pod/--component makes no sense with "
                    f"{kind}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if pod is None and target is None:
                print(
                    f"error: for {kind}, the component must be explicitly "
                    "given as target or via --component",
                    file=sys.stderr,
                )
                sys.exit(1)
            instance = await find_unique_object(client, namespace, kind)
            if instance is None:
                print(
                    f"error: no instance of {kind} found",
                    file=sys.stderr,
                )
                sys.exit(1)
            instance_name = instance["metadata"]["name"]
            component = target or pod

        try:
            label_selector, container = get_component_label_selector(
                group,
                kind,
                instance_name,
                container,
                component,
            )
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(2)

        await yaookctl.logs.watch_pod_logs(
            client,
            log_viewer,
            ctx.obj["namespace"],
            label_selector,
            container,
            tail=tail,
        )


@main.command("debug")
@with_client
@click.option("-c", "--container")
@click.option("-I", "--force-image")
@click.option("-S", "--force-shell")
@click.option("-p", "-C", "--pod", "--component", "pod_or_component")
@click.argument("kind", shell_complete=kind_shell_complete)
@click.argument("target", shell_complete=target_shell_complete)
async def debug(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str,
        target: str,
        container: typing.Optional[str],
        pod_or_component: typing.Optional[str],
        force_image: typing.Optional[str],
        force_shell: typing.Optional[str],
) -> None:
    """
    Create a debug pod next to the target pod specified by KIND and TARGET.
    The pod is spawned with the same volume mounts as the target pod.

    KIND may be one of: {KIND}, or any Yaook CR plural (e.g. amqpservers).

    Example:

        $ yaook debug compute node-1
    """
    namespace = ctx.obj["namespace"]
    try:
        pod, container = await find_single_container(
            client, namespace, kind, target, container, pod_or_component,
        )
    except (LookupError, ValueError) as exc:
        if not isinstance(exc, click.ClickException):
            raise click.ClickException(str(exc))
        raise

    v1core = kclient.CoreV1Api(client)
    debugger_spec = yaookctl.debugger.make_debugger_pod_spec(
        target_pod=pod,
        target_container=container,
        force_image=force_image,
        force_shell=force_shell,
    )
    debugger = kclient.V1Pod(
        metadata=kclient.V1ObjectMeta(
            generate_name=f"{pod.metadata.name}-dbg-",
            namespace=pod.metadata.namespace,
        ),
        spec=debugger_spec,
    )
    debugger = await v1core.create_namespaced_pod(
        pod.metadata.namespace,
        debugger,
    )
    try:
        with spinner("waiting for container to start...") as spin:
            while True:
                status = await v1core.read_namespaced_pod_status(
                    debugger.metadata.name,
                    debugger.metadata.namespace,
                )
                try:
                    container_status = [
                        container for container in (
                            status.status.container_statuses or []
                        )
                        if container.name == "debugger"
                    ][0].ready
                except IndexError:
                    container_status = False
                if container_status:
                    break
                spin()
                await asyncio.sleep(0.5)

        await kubectl_block(
            ctx, "attach", "-it", "-c", "debugger", debugger.metadata.name,
        )
    finally:
        try:
            await v1core.delete_namespaced_pod(
                debugger.metadata.name,
                debugger.metadata.namespace,
            )
        except kclient.ApiException as exc:
            if exc.status != 404:
                raise


@main.command("force-upgrade")
@with_client
@click.option("--break-even-if-unnecessary/--no-break-even-if-unnecessary",
              default=False)
@click.option("--yes-i-mean-it/--no-i-do-not-mean-it",
              default=False)
@click.argument("kind", shell_complete=upgradable_kind_shell_complete)
@click.argument("node", shell_complete=target_shell_complete)
async def force_upgrade(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str,
        node: str,
        break_even_if_unnecessary: bool,
        yes_i_mean_it: bool,
) -> None:
    """
    Force the upgrade of a stateful Yaook service.

    Warning: This operation is dangerous! If the service does not come up
    properly after the upgrade, loss of the data plane (running VMs, network
    routes etc.) may be caused. Also, network data plane will most likely be
    interrupted for l2 and l3 services even in the best of circumstances.

    This effectively strips the finalizer of the resource and thus skips any
    cleanup steps.

    KIND may be one of: compute, l2, l3, dhcp, bgp.

    Example:

        $ yaookctl force-upgrade compute cmp-selu-6613
    """
    kind = KIND_MAP.get(kind, kind)
    if kind not in UPGRADABLE_KINDS:
        print(f"error: {kind} is not a thing which can be force-upgraded",
              file=sys.stderr)
        sys.exit(2)

    group = API_GROUP_MAP.get(kind, "yaook.cloud")
    namespace = ctx.obj["namespace"]

    custom = kclient.CustomObjectsApi(client)
    core_v1 = kclient.CoreV1Api(client)
    try:
        instance = await custom.get_namespaced_custom_object(
            group, "v1", namespace, kind, node,
        )
    except kclient.ApiException as exc:
        if exc.status == 404:
            print(f"error: {kind} {namespace}/{node} does not exist",
                  file=sys.stderr)
            sys.exit(1)
        raise

    is_deleting = instance["metadata"].get("deletionTimestamp") is not None
    # casting to bool here (instead of `is not None`) because we want to treat
    # both None and [] as falsey.
    has_finalizers = bool(instance["metadata"].get("finalizers"))
    recreation_required = len([
        condition
        for condition in instance.get(
            "status", {},
        ).get("conditions", {})
        if condition["type"] == "RequiresRecreation"
    ]) > 0

    if (not recreation_required and
            not is_deleting and
            not break_even_if_unnecessary):
        print(f"error: {kind} {namespace}/{node} is not being deleted and does"
              " not require recreation; refusing to break it",
              file=sys.stderr)
        print("hint: force by passing --break-even-if-unnecessary",
              file=sys.stderr)
        sys.exit(3)

    if not yes_i_mean_it and not click.confirm(
            f"The {kind} {namespace}/{node} will be force-deleted, causing "
            "potential loss of data and availability. Continue (pass "
            "--yes-i-mean-it to bypass this question)?",
            default=False,
            prompt_suffix=""):
        print("error: confirmation to delete the resource was denied.",
              file=sys.stderr)
        sys.exit(3)

    # if not already deleting, kill it now
    if not is_deleting:
        await custom.delete_namespaced_custom_object(
            group, "v1", namespace, kind, node,
        )

    # strip the finalizers away
    try:
        await custom.patch_namespaced_custom_object(
            group, "v1", namespace, kind, node,
            [
                {"op": "remove", "path": "/metadata/finalizers"},
            ]
        )
    except kclient.ApiException as exc:
        # if the status is 422 *and* we don't expect finalizers, we ignore the
        # error. we still attempt to remove finalizers always, because they
        # might be added concurrently.
        if exc.status != 422 or has_finalizers:
            raise

    lock_suffix = instance['spec'].get('lockName', instance['kind'])
    lock_annotation = f"l2-lock.maintenance.yaook.cloud/{lock_suffix}"
    lock_jsonpath = lock_annotation.replace("/", "~1")

    try:
        await core_v1.patch_node(
            node,
            [
                {"op": "remove",
                 "path": f"/metadata/annotations/{lock_jsonpath}"},
            ]
        )
    except kclient.ApiException as e:
        # lock already gone or non-locking resource emits 422
        if e.status != 422:
            raise


@blocking
async def database_shell_complete(
        ctx: click.Context,
        param: click.Parameter,
        incomplete: str,
) -> typing.List[click.shell_completion.CompletionItem]:
    try:
        kind = ctx.params["kind"]
    except KeyError:
        return []

    if ctx.parent is not None:
        k8s_context = ctx.parent.params.get("context")
    else:
        k8s_context = None
    k8s_namespace = get_namespace(
        ctx.parent.params.get("namespace")
        if ctx.parent is not None
        else None
    )

    plural = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(plural, "yaook.cloud")
    if plural in MULTI_INSTANCE_PLURALS:
        # not supported for the sql call anyway
        return []

    specific_alias_map = {
        alias: component
        for (known_plural, alias), component in DATABASE_ALIAS_MAP.items()
        if known_plural == plural and alias is not None
    }
    discovered_components: typing.Set[str] = (
        set(specific_alias_map.keys()) | set(specific_alias_map.values())
    )
    try:
        async with kubernetes_client(k8s_context) as client:
            custom = kclient.CustomObjectsApi(client)
            options = (await custom.list_namespaced_custom_object(
                "infra.yaook.cloud",
                "v1",
                k8s_namespace,
                "mysqlservices",
                label_selector=",".join([
                    f"state.yaook.cloud/parent-plural={plural}",
                    f"state.yaook.cloud/parent-group={group}",
                ]),
            ))["items"]
            for option in options:
                discovered_component = option["metadata"]["labels"].get(
                    "state.yaook.cloud/component",
                )
                if discovered_component is not None:
                    discovered_components.add(discovered_component)
    except (aiohttp.ClientConnectorError, kclient.ApiException):
        # we ignore those, we don't want to break the shell
        pass

    return [
        click.shell_completion.CompletionItem(
            option,
            type="plain",
            help=(
                f"alias for {specific_alias_map.get(option)}"
                if specific_alias_map.get(option) is not None
                else None
            ),
        )
        for option in sorted(discovered_components)
        if option.startswith(incomplete)
    ]


@main.command("sql")
@with_client
@click.argument("kind", shell_complete=kind_shell_complete)
@click.argument("database", shell_complete=database_shell_complete,
                required=False)
async def sql(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str,
        database: typing.Optional[str],
) -> None:
    """
    Create a mysql shell in the database specified by KIND and DATABASE.

    DATABASE may be omitted if the given KIND only has one database,
    otherwise it must be the name of a database component of that KIND.

    KIND may be one of: {KIND}, or any Yaook CR plural (e.g. amqpservers)

    Example:

        $ yaook sql nova api_db
    """
    namespace = ctx.obj["namespace"]
    plural = KIND_MAP.get(kind, kind)
    if plural == "mysqlservices":
        if database is None:
            print("DATABASE is a required argument for the MySQLService kind",
                  file=sys.stderr)
            sys.exit(2)
        db_name = database
    else:
        instance = await find_unique_object(client, namespace, plural)
        if instance is None:
            print(f"error: no instance of {plural} found", file=sys.stderr)
            sys.exit(1)
        name = instance["metadata"]["name"]

        custom = kclient.CustomObjectsApi(client)
        database = DATABASE_ALIAS_MAP.get((plural, database), database)
        label_selectors = [
            f"state.yaook.cloud/parent-plural={plural}",
            f"state.yaook.cloud/parent-name={name}",
            "state.yaook.cloud/parent-group=yaook.cloud",
        ]
        if database is not None:
            label_selectors.append(f"state.yaook.cloud/component={database}")

        candidates = (await custom.list_namespaced_custom_object(
            "infra.yaook.cloud", "v1", namespace, "mysqlservices",
            label_selector=",".join(label_selectors),
        ))["items"]

        if len(candidates) == 0:
            if database is not None:
                print(f"database {database} not found for {plural}/{name}",
                      file=sys.stderr)
            else:
                print(f"no database found for {plural}/{name}",
                      file=sys.stderr)
            sys.exit(1)

        if len(candidates) > 1:
            print(f"multiple databases found for {plural}/{name}",
                  file=sys.stderr)
            for candidate in candidates:
                labels = candidate["metadata"]["labels"]
                print(
                    candidate["metadata"]["name"],
                    labels["state.yaook.cloud/component"],
                    sep="\t",
                    file=sys.stderr,
                )
            sys.exit(2)

        db_name = candidates[0]["metadata"]["name"]

    pod = await find_any_pod(
        client, namespace,
        "infra.yaook.cloud", "mysqlservices", db_name,
        "database",
    )
    if pod is None:
        print(f"error: no database pod exists for database {name} of "
              f"{plural}/{name}", file=sys.stderr)
        sys.exit(3)

    return kubectl(
        ctx, "exec", "-it", pod.metadata.name, "-c", "mariadb-galera",
        "--", "/bin/sh", "-euc",
        "export MYSQL_PWD=\"$MARIADB_ROOT_PASSWORD\"; "
        "exec mariadb -u yaook-sys-maint \"$MARIADB_DATABASE\"",
    )


@main.command("pause")
@with_client
@click.argument("kind", shell_complete=kind_shell_complete)
@click.argument("name", shell_complete=name_shell_complete)
@click.option("--comment")
async def pause(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str, name: str, comment: typing.Optional[str]) -> None:
    """
    Add the pause annotation to a resource.

    The pause annotation stops the corresponding operator from reconciling the
    resource.

    Note: This only works on Yaook custom resources! You cannot pause e.g. a
    StatefulSet. If you want to prevent e.g. a StatefulSet from being updated,
    you have to pause the parent Yaook resource.
    """
    namespace = ctx.obj["namespace"]
    plural = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(plural, "yaook.cloud")
    custom = kclient.CustomObjectsApi(client)
    value = comment or "paused using yaookctl on {}".format(datetime.utcnow())
    await custom.patch_namespaced_custom_object(
        group, "v1", namespace, plural, name,
        [
            {"op": "add",
             "path": f"/metadata/annotations/{PAUSE_ANNOTATION_JSONPATCH}",
             "value": value}
        ]
    )


@main.command("unpause")
@with_client
@click.argument("kind", shell_complete=kind_shell_complete)
@click.argument("name", shell_complete=name_shell_complete)
async def unpause(
        ctx: click.Context,
        client: kclient.ApiClient,
        kind: str, name: str) -> None:
    """
    Remove the pause annotation from a resource.
    """
    namespace = ctx.obj["namespace"]
    plural = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(plural, "yaook.cloud")
    custom = kclient.CustomObjectsApi(client)
    try:
        await custom.patch_namespaced_custom_object(
            group, "v1", namespace, plural, name,
            [
                {"op": "remove",
                 "path": f"/metadata/annotations/{PAUSE_ANNOTATION_JSONPATCH}"}
            ]
        )
    except kclient.ApiException as e:
        if e.status != 422:  # precondition failed
            raise


@main.group("openstack")
def openstack() -> None:
    """
    Utilities to work with OpenStack.
    """
    pass


def is_deployment_ready(deployment: kclient.V1Deployment) -> bool:
    if not deployment.status:
        return False
    if not deployment.status.observed_generation:
        return False
    if not deployment.status.updated_replicas:
        return False
    if not deployment.status.ready_replicas:
        return False
    if not deployment.status.replicas:
        return False
    return (
        deployment.status.observed_generation == deployment.metadata.generation
        and deployment.status.replicas == deployment.spec.replicas
        and deployment.status.updated_replicas == deployment.spec.replicas
        and deployment.status.ready_replicas == deployment.spec.replicas
    )


async def openstack_shell_impl(
        ctx: click.Context,
        client: kclient.ApiClient,
        keystone_ref: typing.Optional[str],
        external_keystone_ref: typing.Optional[str],
        image: typing.Optional[str],
) -> None:
    """
    Manage a Deployment with openstackclient and provide a shell inside it.
    """

    namespace = ctx.obj['namespace']
    if keystone_ref is not None:
        plural = "keystonedeployments"
        name = keystone_ref
    elif external_keystone_ref is not None:
        plural = "externalkeystonedeployments"
        name = external_keystone_ref
    else:
        plural = "keystonedeployments"
        keystone_instance = await find_unique_object(
            client,
            namespace,
            plural,
        )
        if keystone_instance is None:
            plural = "externalkeystonedeployments"
            keystone_instance = await find_unique_object(
                client,
                namespace,
                plural,
            )
            if keystone_instance is None:
                print("error: failed to find a KeystoneDeployment or "
                      "ExternalKeystoneDeployment in namespace "
                      f"{namespace}",
                      file=sys.stderr)
                sys.exit(2)
        name = keystone_instance["metadata"]["name"]

    base_label_selector = (
        f"state.yaook.cloud/parent-plural={plural},"
        f"state.yaook.cloud/parent-name={name},"
        "state.yaook.cloud/parent-group=yaook.cloud"
    )

    core_v1 = kclient.CoreV1Api(client)
    apps_v1 = kclient.AppsV1Api(client)
    internal_endpoint, = (await core_v1.list_namespaced_config_map(
        namespace,
        label_selector=(
            f"{base_label_selector},"
            f"state.yaook.cloud/component=internal_config"
        )
    )).items
    ca_certs, = (await core_v1.list_namespaced_config_map(
        namespace,
        label_selector=(
            f"{base_label_selector},"
            f"state.yaook.cloud/component=ca_certs"
        )
    )).items
    admin_credentials, = (await core_v1.list_namespaced_secret(
        namespace,
        label_selector=(
            f"{base_label_selector},"
            f"state.yaook.cloud/component=admin_credentials"
        )
    )).items

    image_ref = image or os.environ.get(
        "YAOOKCTL_DEFAULT_OPENSTACKCLIENT_IMAGE",
        "registry.yaook.cloud/yaook/openstackclient:devel",
    )

    container = kclient.V1Container(
        name="openstackclient",
        image=image_ref,
        command=["/usr/bin/tini", "--", "/bin/sleep", "infinity"],
        env_from=[
            kclient.V1EnvFromSource(
                config_map_ref=kclient.V1ConfigMapEnvSource(
                    name=internal_endpoint.metadata.name,
                ),
            ),
            kclient.V1EnvFromSource(
                secret_ref=kclient.V1SecretEnvSource(
                    name=admin_credentials.metadata.name,
                ),
            ),
        ],
        env=[
            kclient.V1EnvVar(
                name="REQUESTS_CA_BUNDLE",
                value="/etc/pki/tls/certs/ca-bundle.crt",
            ),
        ],
        volume_mounts=[
            kclient.V1VolumeMount(
                name="cacerts",
                mount_path="/etc/pki/tls/certs/",
            ),
        ],
    )

    deployment = kclient.V1Deployment(
        metadata=kclient.V1ObjectMeta(
            namespace=namespace,
            name=f"yaookctl-openstackclient-{name}",
            labels={
                "app.kubernetes.io/name": "yaookctl",
                "app.kubernetes.io/instance": name,
                "app.kubernetes.io/component": "openstackclient",
            },
        ),
        spec=kclient.V1DeploymentSpec(
            replicas=1,
            selector=kclient.V1LabelSelector(
                match_labels={
                    "app.kubernetes.io/name": "yaookctl",
                    "app.kubernetes.io/instance": name,
                    "app.kubernetes.io/component": "openstackclient",
                },
            ),
            template=kclient.V1PodTemplateSpec(
                metadata=kclient.V1ObjectMeta(
                    labels={
                        "app.kubernetes.io/name": "yaookctl",
                        "app.kubernetes.io/instance": name,
                        "app.kubernetes.io/component": "openstackclient",
                    },
                ),
                spec=kclient.V1PodSpec(
                    containers=[container],
                    volumes=[
                        kclient.V1Volume(
                            name="cacerts",
                            config_map=kclient.V1ConfigMapVolumeSource(
                                name=ca_certs.metadata.name,
                            ),
                        ),
                    ],
                ),
            ),
        ),
    )

    try:
        deployment = await apps_v1.create_namespaced_deployment(
            namespace,
            deployment,
        )
    except kclient.ApiException as e:
        if e.status != 409:
            raise
        deployment = await apps_v1.patch_namespaced_deployment(
            deployment.metadata.name,
            namespace,
            deployment,
        )

    with spinner("waiting for deployment to update...") as spin:
        while not is_deployment_ready(deployment):
            deployment = await apps_v1.read_namespaced_deployment(
                deployment.metadata.name,
                deployment.metadata.namespace,
            )
            spin()
            await asyncio.sleep(0.5)

    pods = (await core_v1.list_namespaced_pod(
        namespace,
        label_selector=(
            "app.kubernetes.io/name=yaookctl,"
            "app.kubernetes.io/component=openstackclient,"
            f"app.kubernetes.io/instance={name}"
        )
    )).items
    # we want the newest pod, it'll be the right one (as we waited for the
    # deployment to be ok)
    pods.sort(key=lambda x: x.metadata.creation_timestamp, reverse=True)
    pod = pods[0]
    return kubectl(
        ctx, "exec", "-it", pod.metadata.name,
        "-c", "openstackclient",
        "--", "/bin/bash", "--login",
    )


@openstack.command("shell")
@with_client
@click.option("-i", "--image", type=str)
@optgroup.group("Keystone Instance",   # type:ignore
                cls=MutuallyExclusiveOptionGroup)
@optgroup.option("-k", "--keystone-ref", type=str)
@optgroup.option("-E", "--external-keystone-ref", type=str)
async def openstack_shell(
        ctx: click.Context,
        client: kclient.ApiClient,
        keystone_ref: typing.Optional[str],
        external_keystone_ref: typing.Optional[str],
        image: typing.Optional[str],
) -> None:
    return await openstack_shell_impl(
        ctx,
        client,
        keystone_ref,
        external_keystone_ref,
        image,
    )


@main.group()
def galera() -> None:
    """
    Utilities to work with Galera clusters.
    """
    pass


@galera.command("find-wsrep-positions")
@with_client
@click.option("--quiet/--not-quiet", "-q", default=False)
@click.argument("name", shell_complete=functools.partial(
        fixed_shell_complete,
        group="infra.yaook.cloud", version="v1", plural="mysqlservices"))
async def galera_find_wsrep_positions(
        ctx: click.Context,
        client: kclient.ApiClient,
        name: str,
        quiet: bool) -> None:
    namespace = ctx.obj["namespace"]
    core_v1 = kclient.CoreV1Api(client)
    label_selector = get_mysqlservice_label_selector(name)
    sts = await find_downscaled_mysqlservice_sts(client, namespace, name)

    mariadb_image, = [
        container.image
        for container in sts.spec.template.spec.containers
        if container.name == "mariadb-galera"
    ]
    pvcs = (await core_v1.list_namespaced_persistent_volume_claim(
        namespace,
        label_selector=label_selector,
    )).items

    pvc_state = []
    for pvc in pvcs:
        try:
            gra_state_raw = await yaookctl.galera.get_grastate(
                client,
                namespace,
                mariadb_image,
                pvc.metadata.name,
            )
        except subprocess.CalledProcessError:
            # force recheck using recover command
            gra_state = yaookctl.galera.GraState.zero()
        else:
            try:
                gra_state = yaookctl.galera.GraState.parse(gra_state_raw)
            except ValueError as e:
                print(
                    "warning: failed to parse grastate.dat from "
                    f"{pvc.metadata.name}: {e}",
                    file=sys.stderr,
                )
                gra_state = yaookctl.galera.GraState.zero()

        recover_needed = False
        if gra_state.seqno == -1:
            log = await yaookctl.galera.recover_grastate(
                client,
                namespace,
                mariadb_image,
                pvc.metadata.name
            )
            try:
                gra_state = yaookctl.galera.GraState.from_recovery(log)
            except ValueError as e:
                print("warning: failed to parse recovered position from log "
                      f"for {pvc.metadata.name}: {e}")
            recover_needed = True

        pvc_state.append((pvc.metadata.name, gra_state, recover_needed))

    safe_to_bootstrap: typing.Optional[typing.Tuple[str, yaookctl.galera.GraState]] = None  # noqa:E501
    highest_seqno: typing.Optional[typing.Tuple[str, yaookctl.galera.GraState]] = None  # noqa:E501
    uuid: typing.Optional[str] = None
    uuid_ok = True
    for pvc_name, gra_state, _ in pvc_state:
        if gra_state.safe_to_bootstrap:
            if safe_to_bootstrap is None:
                safe_to_bootstrap = (pvc_name, gra_state)
            else:
                print(f"warning: {pvc_name} is *also* safe to bootstrap!",
                      file=sys.stderr)
        if (gra_state.seqno >= 0 and
            (highest_seqno is None or
             highest_seqno[1].seqno < gra_state.seqno)):
            highest_seqno = (pvc_name, gra_state)
        if gra_state.uuid != yaookctl.galera.ZERO_UUID:
            if uuid is None:
                uuid = gra_state.uuid
            elif uuid != gra_state.uuid:
                print("error: mismatching UUIDs!", file=sys.stderr)

    uuid_ok = uuid_ok and uuid is not None

    best = safe_to_bootstrap or highest_seqno

    if not quiet:
        tbl = prettytable.PrettyTable()
        tbl.field_names = ["PVC Name", "UUID", "SeqNo",
                           "Safe?", "Recovered?", "Best"]
        tbl.align = "l"
        for pvc_name, gra_state, recover_needed in pvc_state:
            is_best = best is not None and best[0] == pvc_name
            tbl.add_row((pvc_name,
                         gra_state.uuid,
                         gra_state.seqno,
                         gra_state.safe_to_bootstrap,
                         recover_needed,
                         is_best))
        print(tbl)

    if uuid_ok and safe_to_bootstrap is not None:
        if quiet:
            print(f"{safe_to_bootstrap[0]}")
    elif uuid_ok and highest_seqno is not None:
        if quiet:
            print(f"{highest_seqno[0]}")
    else:
        print("found *no* suitable bootstrap source!", file=sys.stderr)
        if quiet:
            for pvc_name, gra_state, _ in pvc_state:
                print(pvc_name, gra_state, file=sys.stderr)
        sys.exit(1)


@galera.command("force-bootstrap")
@with_client
@click.argument("name", shell_complete=functools.partial(
        fixed_shell_complete,
        group="infra.yaook.cloud", version="v1", plural="mysqlservices"))
@click.argument("index", type=int)
async def galera_force_bootstrap(
        ctx: click.Context,
        client: kclient.ApiClient,
        name: str,
        index: int) -> None:
    namespace = ctx.obj["namespace"]
    apps_v1 = kclient.AppsV1Api(client)
    sts = await find_downscaled_mysqlservice_sts(client, namespace, name)

    mysql_container_index = [
        i
        for i, container in enumerate(sts.spec.template.spec.containers)
        if container.name == "mariadb-galera"
    ][0]
    mysql_container = sts.spec.template.spec.containers[mysql_container_index]

    shell_script = mysql_container.command[-1]
    shell_script = yaookctl.galera.inject_recovery_command(
        shell_script,
        index,
        sts.metadata.name,
    )

    if not click.confirm(
            f"The MySQL service {namespace}/{sts.metadata.name} will be forced"
            f" to recover from the PVC data-{sts.metadata.name}-{index}."
            "Continue?",
            default=False,
            prompt_suffix=""):
        print("error: confirmation to force recovery was denied.",
              file=sys.stderr)
        sys.exit(3)

    container_path = f"/spec/template/spec/containers/{mysql_container_index}"
    arg_index = len(mysql_container.command)-1

    await apps_v1.patch_namespaced_stateful_set(
        sts.metadata.name,
        namespace,
        [
            {
                "op": "replace",
                "path": f"{container_path}/command/{arg_index}",
                "value": shell_script,
            },
            {
                "op": "replace",
                "path": "/spec/replicas",
                "value": index + 1,
            },
            {
                "op": "remove",
                "path": "/spec/minReadySeconds",
            },
            {
                "op": "remove",
                "path": f"{container_path}/livenessProbe",
            },
            {
                "op": "remove",
                "path": f"{container_path}/startupProbe",
            },
            {
                "op": "remove",
                "path": f"{container_path}/readinessProbe",
            },
        ],
    )


@main.group()
def ovsdb() -> None:
    """
    Utilities to work with ovsdb clusters.
    """
    pass


@ovsdb.command("disaster-recovery")
@with_client
@click.argument("name", shell_complete=functools.partial(
        fixed_shell_complete,
        group="infra.yaook.cloud", version="v1", plural="ovsdbservices"))
@click.argument("index", type=int)
async def ovsdb_disaster_recovery(
        ctx: click.Context,
        client: kclient.ApiClient,
        name: str,
        index: int) -> None:
    namespace = ctx.obj["namespace"]
    apps_v1 = kclient.AppsV1Api(client)
    sts = await find_downscaled_ovsdbservice_sts(client, namespace, name)

    ovsdb_container_index = [
        i
        for i, container in enumerate(sts.spec.template.spec.containers)
        if container.name == "ovsdb"
    ][0]
    init_container_index = [
        i
        for i, container in enumerate(sts.spec.template.spec.init_containers)
        if container.name == "setup-ovsdb"
    ][0]
    monitoring_container_index = [
        i
        for i, container in enumerate(sts.spec.template.spec.containers)
        if container.name == "ovsdb-monitoring"
    ][0]
    ssl_container_index = [
        i
        for i, container in enumerate(sts.spec.template.spec.containers)
        if container.name == "ssl-terminator"
    ][0]
    ovsdb_container = sts.spec.template.spec.containers[ovsdb_container_index]

    ovsdb_shell_script = ovsdb_container.command[-1]
    ovsdb_shell_script = yaookctl.ovsdb.inject_ovsdb_recovery_command(
        ovsdb_shell_script,
        index,
        sts.metadata.name,
    )
    init_shell_script = yaookctl.ovsdb.inject_init_recovery_command(
        index,
        sts.metadata.name,
    )
    new_init_command = ["bash", "-ec", init_shell_script]

    if not click.confirm(
            f"The OVSDB service {namespace}/{sts.metadata.name} will be forced"
            f" to recover from the PVC data-{sts.metadata.name}-{index}."
            "Continue?",
            default=False,
            prompt_suffix=""):
        print("error: confirmation to force recovery was denied.",
              file=sys.stderr)
        sys.exit(3)

    ovsdb_container_path = \
        f"/spec/template/spec/containers/{ovsdb_container_index}"
    init_container_path = \
        f"/spec/template/spec/initContainers/{init_container_index}"
    monitoring_container_path = \
        f"/spec/template/spec/containers/{monitoring_container_index}"
    ssl_container_path = \
        f"/spec/template/spec/containers/{ssl_container_index}"
    arg_index = len(ovsdb_container.command)-1

    await apps_v1.patch_namespaced_stateful_set(
        sts.metadata.name,
        namespace,
        [
            {
                "op": "add",
                "path": f"{init_container_path}/command",
                "value": new_init_command
            },
            {
                "op": "replace",
                "path": f"{ovsdb_container_path}/command/{arg_index}",
                "value": ovsdb_shell_script,
            },
            {
                "op": "replace",
                "path": "/spec/replicas",
                "value": index + 1,
            },
            {
                "op": "remove",
                "path": f"{ovsdb_container_path}/lifecycle",
            },
            {
                "op": "remove",
                "path": f"{ovsdb_container_path}/livenessProbe",
            },
            {
                "op": "remove",
                "path": f"{ovsdb_container_path}/readinessProbe",
            },
            {
                "op": "remove",
                "path": f"{ovsdb_container_path}/startupProbe",
            },
            {
                "op": "remove",
                "path": f"{ovsdb_container_path}/securityContext",
            },
            {
                "op": "remove",
                "path": f"{ssl_container_path}/livenessProbe",
            },
            {
                "op": "remove",
                "path": f"{ssl_container_path}/readinessProbe",
            },
            {
                "op": "remove",
                "path": f"{monitoring_container_path}",
            },
        ],
    )
logs.help = logs.help.format(KIND=", ".join(KIND_MAP.keys()))  # type: ignore
debug.help = debug.help.format(KIND=", ".join(KIND_MAP.keys()))  # type: ignore
shell.help = shell.help.format(KIND=", ".join(KIND_MAP.keys()))  # type: ignore
sql.help = sql.help.format(KIND=", ".join(KIND_MAP.keys()))  # type: ignore
