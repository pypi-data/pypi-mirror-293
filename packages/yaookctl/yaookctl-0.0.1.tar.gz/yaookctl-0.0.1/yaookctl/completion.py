import aiohttp
import typing

import click

import kubernetes_asyncio.client as kclient

from .cliutil import (
    blocking,
    get_namespace,
    kubernetes_client,
)
from .data import (
    API_GROUP_MAP,
    COMPONENT_ALIAS_MAP,
    KIND_MAP,
    MULTI_INSTANCE_PLURALS,
    UPGRADABLE_KINDS,
)


def namespace_from_raw_context(
        ctx: typing.Optional[click.Context],
) -> typing.Optional[str]:
    while ctx is not None:
        namespace = ctx.params.get("namespace")
        if namespace is not None:
            return namespace
        ctx = ctx.parent
    return None


def kind_shell_complete(
        ctx: click.Context,
        param: click.Parameter,
        incomplete: str,
) -> typing.List[click.shell_completion.CompletionItem]:
    options = sorted(set(KIND_MAP.keys()) | set(KIND_MAP.values()))
    return [
        click.shell_completion.CompletionItem(
            option,
            type="plain",
            help=(
                f"alias for {KIND_MAP.get(option)}"
                if KIND_MAP.get(option) is not None
                else None
            ),
        )
        for option in options
        if option.startswith(incomplete)
    ]


async def get_components(
        k8s_context: typing.Optional[str],
        k8s_namespace: str,
        group: str,
        plural: str,
        instance: typing.Optional[str],
        incomplete: str,
) -> typing.List[click.shell_completion.CompletionItem]:
    specific_alias_map = {
        alias: component
        for (known_plural, alias), component in COMPONENT_ALIAS_MAP.items()
        if known_plural == plural and alias is not None
    }
    discovered_components: typing.Set[str] = (
        set(specific_alias_map.keys()) | set(specific_alias_map.values())
    )
    try:
        async with kubernetes_client(k8s_context) as client:
            core_v1 = kclient.CoreV1Api(client)
            labels = [
                f"state.yaook.cloud/parent-plural={plural}",
                f"state.yaook.cloud/parent-group={group}",
            ]
            if instance is not None:
                labels.append(f"state.yaook.cloud/parent-name={instance}")
            options = (await core_v1.list_namespaced_pod(
                k8s_namespace,
                label_selector=",".join(labels),
            )).items
            for option in options:
                discovered_component = option.metadata.labels.get(
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


@blocking
async def target_shell_complete(
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
    k8s_namespace = get_namespace(namespace_from_raw_context(ctx))

    plural = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(plural, "yaook.cloud")
    if plural in MULTI_INSTANCE_PLURALS:
        try:
            async with kubernetes_client(k8s_context) as client:
                custom = kclient.CustomObjectsApi(client)
                options = (await custom.list_namespaced_custom_object(
                    group, "v1", k8s_namespace, plural,
                ))["items"]
                return [
                    click.shell_completion.CompletionItem(
                        option["metadata"]["name"],
                    )
                    for option in sorted(options,
                                         key=lambda x: x["metadata"]["name"])
                    if option["metadata"]["name"].startswith(incomplete)
                ]
        except (aiohttp.ClientConnectorError, kclient.ApiException):
            # we ignore those, we don't want to break the shell
            return []
    else:
        return await get_components(
            k8s_context,
            k8s_namespace,
            group,
            plural,
            None,
            incomplete,
        )


@blocking
async def component_shell_complete(
        ctx: click.Context,
        param: click.Parameter,
        incomplete: str,
) -> typing.List[click.shell_completion.CompletionItem]:
    kind = ctx.params["kind"]
    if kind is None:
        try:
            kind = ctx.args.pop(0)
        except ValueError:
            return []

    target = ctx.params["target"]
    if target is None:
        try:
            target = ctx.args.pop(0)
        except ValueError:
            pass

    if ctx.parent is not None:
        k8s_context = ctx.parent.params.get("context")
    else:
        k8s_context = None
    k8s_namespace = get_namespace(namespace_from_raw_context(ctx))

    plural = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(plural, "yaook.cloud")

    return await get_components(
        k8s_context,
        k8s_namespace,
        group,
        plural,
        target,
        incomplete,
    )


async def shell_complete_custom_k8s_names(
        client: kclient.ApiClient,
        group: str,
        version: str,
        namespace: str,
        plural: str,
        incomplete: str,
        ) -> typing.List[click.shell_completion.CompletionItem]:
    try:
        custom = kclient.CustomObjectsApi(client)
        options = (await custom.list_namespaced_custom_object(
            group, "v1", namespace, plural,
        ))["items"]
        return [
            click.shell_completion.CompletionItem(
                option["metadata"]["name"],
            )
            for option in sorted(options,
                                 key=lambda x: x["metadata"]["name"])
            if option["metadata"]["name"].startswith(incomplete)
        ]
    except (aiohttp.ClientConnectorError, kclient.ApiException):
        # we ignore those, we don't want to break the shell
        return []


@blocking
async def fixed_shell_complete(
        ctx: click.Context,
        param: click.Parameter,
        incomplete: str,
        group: str,
        version: str,
        plural: str,
) -> typing.List[click.shell_completion.CompletionItem]:
    if ctx.parent is not None:
        k8s_context = ctx.parent.params.get("context")
    else:
        k8s_context = None
    k8s_namespace = get_namespace(namespace_from_raw_context(ctx))

    async with kubernetes_client(k8s_context) as client:
        return await shell_complete_custom_k8s_names(
            client,
            group, version, k8s_namespace, plural,
            incomplete,
        )


@blocking
async def name_shell_complete(
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
    k8s_namespace = get_namespace(namespace_from_raw_context(ctx))

    plural = KIND_MAP.get(kind, kind)
    group = API_GROUP_MAP.get(plural, "yaook.cloud")
    async with kubernetes_client(k8s_context) as client:
        return await shell_complete_custom_k8s_names(
            client,
            group,
            "v1",
            k8s_namespace,
            plural,
            incomplete,
        )


def upgradable_kind_shell_complete(
        ctx: click.Context,
        param: click.Parameter,
        incomplete: str,
) -> typing.List[click.shell_completion.CompletionItem]:
    options = sorted(
        set(
            alias
            for alias, plural in KIND_MAP.items()
            if plural in UPGRADABLE_KINDS
        ) | set(UPGRADABLE_KINDS)
    )
    return [
        click.shell_completion.CompletionItem(
            option,
            type="plain",
            help=(
                f"alias for {KIND_MAP.get(option)}"
                if KIND_MAP.get(option) is not None
                else None
            ),
        )
        for option in options
        if option.startswith(incomplete)
    ]
