import asyncio
import contextlib
import functools
import os
import typing
import typing_extensions

import click

import kubernetes_asyncio.config
import kubernetes_asyncio.client as kclient


P = typing_extensions.ParamSpec("P")
P2 = typing_extensions.ParamSpec("P2")
R = typing.TypeVar("R")


@contextlib.asynccontextmanager
async def kubernetes_client(
        context_name: typing.Optional[str],
) -> typing.AsyncIterator[kclient.ApiClient]:
    try:
        kubernetes_asyncio.config.load_incluster_config()
    except Exception:
        await kubernetes_asyncio.config.load_kube_config(context=context_name)
    config = kclient.Configuration.get_default_copy()
    async with kclient.ApiClient(config) as client:
        yield client


def blocking(
        f: typing.Callable[P2, typing.Coroutine[typing.Any, typing.Any, R]],
) -> typing.Callable[P2, R]:
    @functools.wraps(f)
    def blocked(*args: P2.args, **kwargs: P2.kwargs) -> R:
        return asyncio.run(f(*args, **kwargs))
    return blocked


def with_client(
    f: typing.Callable[
        typing_extensions.Concatenate[click.Context, kclient.ApiClient, P],
        typing.Awaitable[R]
    ],
) -> typing.Callable[P, R]:
    # it's not clear to me (and apparently nether to mypy) what's wrong with
    # the use of @blocking/@click.pass_context here:
    # error: Argument 1 to "blocking" has incompatible type
    #  "Callable[[Arg(Context, 'ctx'), **P], Coroutine[Any, Any, R]]";
    #  expected "Callable[[Arg(Context, 'ctx'), **P], Coroutine[Any, Any, R]]"
    # I'm assuming that'll go away at some point.
    @click.pass_context  # type:ignore
    @blocking
    @functools.wraps(f)
    async def awrapped(
            ctx: click.Context,
            *args: P.args,
            **kwargs: P.kwargs,
    ) -> R:
        context = ctx.obj.get("context")
        async with kubernetes_client(context) as client:
            return await f(ctx, client, *args, **kwargs)

    return awrapped


def get_namespace(from_param: typing.Optional[str]) -> str:
    return from_param or os.getenv("YAOOK_OP_NAMESPACE") or "yaook"
