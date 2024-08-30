import typing
import sys

import kubernetes_asyncio.client as kclient

from .data import (
    API_GROUP_MAP,
    KIND_MAP,
    MULTI_INSTANCE_PLURALS,
    MULTI_POD_PLURALS,
    ContainerResolutionError,
    resolve_component_container,
)


async def find_unique_object(
        client: kclient.ApiClient,
        namespace: str,
        plural: str,
) -> typing.Optional[typing.Mapping]:
    """
    Find a single object with the given plural in Kubernetes.

    :param client: Kubernetes API client
    :param namespace: Namespace to look in.
    :param plural: Plural to look for.
    :raises ValueError: If more than one object is found.
    :return: The object or None if none was found.
    """

    custom = kclient.CustomObjectsApi(client)
    objects = (await custom.list_namespaced_custom_object(
        API_GROUP_MAP.get(plural, "yaook.cloud"),
        "v1",
        namespace,
        plural,
    ))["items"]
    if len(objects) == 0:
        return None
    if len(objects) == 1:
        return objects[0]
    raise ValueError(
        f"found more than one instance of {plural}, which is unexpected",
    )


def select_by_component(
        parent_group: str,
        parent_plural: str,
        parent_name: typing.Optional[str],
        component: str,
) -> str:
    """
    Compose a label selectocr to find a Yaook pod.

    :param parent_group: k8s API group of the parent resource.
    :param parent_plural: k8s resource plural of the parent resource.
    :param parent_name: k8s resource name of the parent resource, or None to
        not filter on the name.
    :param component: Yaook component of the target resource.
    """

    label_selector_parts = [
        f"state.yaook.cloud/parent-plural={parent_plural}",
        f"state.yaook.cloud/component={component}",
    ]
    if parent_group is not None:
        label_selector_parts.append(
            f"state.yaook.cloud/parent-group={parent_group}"
        )
    if parent_name is None:
        label_selector_parts.append("state.yaook.cloud/parent-name")
    else:
        label_selector_parts.append(
            f"state.yaook.cloud/parent-name={parent_name}"
        )
    return ",".join(label_selector_parts)


async def get_pods_by_component(
        client: kclient.ApiClient,
        namespace: str,
        parent_group: str,
        parent_plural: str,
        parent_name: str,
        component: str,
) -> typing.List[kclient.V1Pod]:
    """
    List all pods which belong to the given component of the referenced Yaook
    resource.

    :param client: k8s Api client
    :param namespace: Name of the k8s namespace to work in.
    :param parent_group: k8s API group of the parent resource.
    :param parent_plural: k8s resource plural of the parent resource.
    :param parent_name: k8s resource name of the parent resource, or None to
        not filter on the name.
    :param component: Yaook component of the target resource.
    :return: List of V1Pod objects which matched the query.
    """
    core_v1 = kclient.CoreV1Api(client)
    label_selector = select_by_component(
        parent_group,
        parent_plural,
        parent_name,
        component,
    )
    return (await core_v1.list_namespaced_pod(
        namespace,
        label_selector=label_selector,
    )).items


async def find_unique_pod(
        client: kclient.ApiClient,
        namespace: str,
        parent_group: str,
        parent_plural: str,
        parent_name: str,
        component: str
) -> typing.Optional[kclient.V1Pod]:
    """
    Find exactly one pod of the given component of the referenced Yaook
    resource.

    :param client: k8s Api client
    :param namespace: Name of the k8s namespace to work in.
    :param parent_group: k8s API group of the parent resource.
    :param parent_plural: k8s resource plural of the parent resource.
    :param parent_name: k8s resource name of the parent resource.
    :param component: Yaook component of the target resource.
    :raises ValueError: if more than one pod is found.
    :return: The V1Pod object or None, if no pod is found.
    """
    pods = await get_pods_by_component(
        client, namespace, parent_group, parent_plural, parent_name, component,
    )
    if len(pods) == 0:
        return None
    if len(pods) == 1:
        return pods[0]
    raise ValueError(
        f"found multiple pods for component {component} of "
        f"{parent_plural}/{parent_name}",
    )


async def find_any_pod(
        client: kclient.ApiClient,
        namespace: str,
        parent_group: str,
        parent_plural: str,
        parent_name: str,
        component: str
) -> typing.Optional[kclient.V1Pod]:
    """
    Find any pod of the given component of the referenced Yaook resource.

    :param client: k8s Api client
    :param namespace: Name of the k8s namespace to work in.
    :param parent_group: k8s API group of the parent resource.
    :param parent_plural: k8s resource plural of the parent resource.
    :param parent_name: k8s resource name of the parent resource.
    :param component: Yaook component of the target resource.
    :return: The V1Pod object or None, if no pod is found.

    If more than one pod is found, prints a diagnostic to stderr and returns
    the first one.
    """
    pods = await get_pods_by_component(
        client, namespace, parent_group, parent_plural, parent_name, component,
    )
    if len(pods) == 0:
        return None
    if len(pods) == 1:
        return pods[0]
    print(f"note: selecting pod {pods[0].metadata.name} out of {len(pods)}",
          file=sys.stderr)
    return pods[0]


def get_component_label_selector(
        group: str,
        plural: str,
        name: typing.Optional[str],
        container: typing.Optional[str],
        component: typing.Optional[str],
) -> typing.Tuple[str, str]:
    """
    Resolve the component and build a label selector / container name pair.

    :param group: k8s API group of the parent resource.
    :param plural: k8s resource plural of the parent resource.
    :param name: k8s resource name of the parent resource, or None to
        not filter on the name.
    :param container: Preferred target container name, or None to use the
        default.
    :param component: Yaook component of the target resource, or None if to use
        the default.
    :raises ContainerResolutionError: if it is not possible to automatically
        resolve the component or container for this resource with the given
        arguments.
    :return: A tuple consisting of the generated pod label selector and the
        resolved container name.

    If :class:`ContainerResolutionError` is raised, the instance name is
    already correctly annotated.
    """
    try:
        component, container = resolve_component_container(
            plural, container, component,
        )
    except ContainerResolutionError as exc:
        exc.instance = name
        raise

    return (
        select_by_component(group, plural, name, component),
        container,
    )


async def find_single_container(
        client: kclient.ApiClient,
        namespace: str,
        kind: str,
        target: str,
        container: typing.Optional[str],
        pod_or_component: typing.Optional[str]
) -> typing.Tuple[kclient.V1Pod, str]:
    """
    High-level function to find a single container of a Yaook resource
    component.

    :param client: k8s Api client
    :param namespace: Name of the k8s namespace to work in
    :param kind: Kind or plural, will be resolved via
        :data:`yaookctl.data.KIND_MAP`.
    :param target: Resource name or Yaook component, depending on the kind.
    :param container: Preferred target container name.
    :param pod_or_component: If the resource requires naming, this must be the
        component name (or it will be defaulted if possible).
    :raises ContainerResolutionError: if it is not possible to resolve the
        container or component name using the given data.
    :raises LookupError: If no matching pod can be found or if the pod match
        is ambiguous.
    :raises LookupError: If there is no resource of the given `kind`.
    :return: A tuple consisting of the V1Pod object and the resolved container
        name.

    If :class:`ContainerResolutionError` is raised, the instance name is
    already correctly annotated.
    """

    kind = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(kind, "yaook.cloud")
    if kind in MULTI_INSTANCE_PLURALS:
        try:
            component, container = resolve_component_container(
                kind, container, pod_or_component,
            )
        except ContainerResolutionError as exc:
            exc.instance = target
            raise

        # for some plurals, we still need to allow "any" pod, e.g. amqpservers
        # which have replicas
        if kind in MULTI_POD_PLURALS:
            pod = await find_any_pod(
                client, namespace,
                group, kind, target,
                component,
            )
        else:
            pod = await find_unique_pod(
                client, namespace,
                group, kind, target,
                component,
            )
        if pod is None:
            raise LookupError(
                f"failed to find pod with component {component} for {target} "
                f"instance of {kind}",
            )
        return pod, container
    else:
        if pod_or_component is not None:
            raise ValueError(
                f"-p/-C/--pod/--component makes no sense with {kind}"
            )
        instance = await find_unique_object(client, namespace, kind)
        if instance is None:
            raise LookupError(f"no instance of {kind} found")

        name = instance["metadata"]["name"]
        try:
            component, container = resolve_component_container(
                kind, container, target,
            )
        except ContainerResolutionError as exc:
            exc.instance = name
            raise

        pod = await find_any_pod(
            client, namespace,
            group, kind, name,
            component,
        )
        if pod is None:
            raise LookupError(
                f"failed to find pod with component {component} for {name} "
                f"instance of {kind}",
            )
        return pod, container


def get_mysqlservice_label_selector(name: str) -> str:
    """
    Compose a selector for the StatefulSet of a MySQLService.
    """
    return (
        "state.yaook.cloud/parent-plural=mysqlservices,"
        "state.yaook.cloud/component=database,"
        f"state.yaook.cloud/parent-name={name}"
    )


async def find_downscaled_mysqlservice_sts(
        client: kclient.ApiClient,
        namespace: str,
        name: str,
) -> kclient.V1StatefulSet:
    """
    Find the StatefulSet of a MySQLService, requiring it to be downscaled.

    .. warning::

        This function calls :func:`sys.exit` directly on errors!

    :param client: k8s Api client
    :param namespace: Name of the k8s namespace to work in
    :param name: Name of the MySQLService resource to investigate.
    :return: The matching V1StatefulSet object.
    """

    apps_v1 = kclient.AppsV1Api(client)
    label_selector = get_mysqlservice_label_selector(name)
    stses = (await apps_v1.list_namespaced_stateful_set(
        namespace,
        label_selector=label_selector,
    )).items
    if len(stses) == 0:
        print(f"failed to find database sts for MySQLService {name}",
              file=sys.stderr)
        sys.exit(2)
    if len(stses) > 1:
        names = ', '.join(item.metadata.name for item in stses)
        print(f"found MULTIPLE databes sts for MySQLService {name}: {names}",
              file=sys.stderr)
        sys.exit(2)

    sts, = stses
    if sts.spec.replicas > 0 or (sts.status.current_replicas or 0) > 0:
        print(f"sts {sts.metadata.name} of MySQLService {name} has "
              f"{sts.status.current_replicas}/{sts.spec.replicas} replicas",
              file=sys.stderr)
        print("please scale it down and wait for it to be scaled down.",
              file=sys.stderr)
        sys.exit(2)
    return sts


def get_ovsdbservice_label_selector(name: str) -> str:
    """
    Compose a selector for the StatefulSet of a OVSDBService.
    """
    return (
        "state.yaook.cloud/parent-plural=ovsdbservices,"
        "state.yaook.cloud/component=ovsdb,"
        f"state.yaook.cloud/parent-name={name}"
    )


async def find_downscaled_ovsdbservice_sts(
        client: kclient.ApiClient,
        namespace: str,
        name: str,
) -> kclient.V1StatefulSet:
    """
    Find the StatefulSet of a OVSDBService, requiring it to be downscaled.

    .. warning::

        This function calls :func:`sys.exit` directly on errors!

    :param client: k8s Api client
    :param namespace: Name of the k8s namespace to work in
    :param name: Name of the OVSDBService resource to investigate.
    :return: The matching V1StatefulSet object.
    """

    apps_v1 = kclient.AppsV1Api(client)
    label_selector = get_ovsdbservice_label_selector(name)
    stses = (await apps_v1.list_namespaced_stateful_set(
        namespace,
        label_selector=label_selector,
    )).items
    if len(stses) == 0:
        print(f"failed to find database sts for OVSDBService {name}",
              file=sys.stderr)
        sys.exit(2)
    if len(stses) > 1:
        names = ', '.join(item.metadata.name for item in stses)
        print(f"found MULTIPLE database sts for OVSDBService {name}: {names}",
              file=sys.stderr)
        sys.exit(2)

    sts, = stses
    if sts.spec.replicas > 0 or (sts.status.current_replicas or 0) > 0:
        print(f"sts {sts.metadata.name} of OVSBDService {name} has "
              f"{sts.status.current_replicas}/{sts.spec.replicas} replicas",
              file=sys.stderr)
        print("please scale it down and wait for it to be scaled down.",
              file=sys.stderr)
        sys.exit(2)
    return sts
