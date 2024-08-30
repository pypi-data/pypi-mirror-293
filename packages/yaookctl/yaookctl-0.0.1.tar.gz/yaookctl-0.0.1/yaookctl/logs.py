import asyncio
import functools
import json
import logging
import math
import time
import typing

import aiohttp
import click

import kubernetes_asyncio.client as kclient
import kubernetes_asyncio.watch as kwatch


def format_json_log_line(line: str) -> typing.Optional[str]:
    line = line.strip()
    if line.endswith("\x1b[00m"):
        line = line[:-5]
    # what the double quote... seen in the wild.
    if line.endswith("\\x1b[00m"):
        line = line[:-8]
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None

    # openstack logs
    try:
        asctime = data["asctime"]
        levelname = data["levelname"]
        name = data["name"]
        message = data["message"]
        try:
            traceback = data["traceback"] or []
        except KeyError:
            traceback = ""
        else:
            traceback.insert(0, "")
            traceback = "\n".join(traceback)
        return f"{asctime} {levelname} {name} {message}{traceback}"
    except KeyError:
        pass

    # apache logs
    try:
        asctime = data["asctime"]
        method = data["method"]
        status = data["status"]
        request = data["request"]
        name = data["name"]
        query = data.get("query", "")

        return f"{asctime} {method} {name}{request}{query} [{status}]"
    except KeyError:
        pass

    return None


def default_formatter(line: bytes) -> str:
    sline = line.decode("utf-8")
    if sline.startswith("{"):
        formatted = format_json_log_line(sline)
        if formatted:
            return formatted
    return sline.strip()


class LogViewer:
    """
    Management class for multiple log watchers.

    :param client: The API client to use to establish log watches.
    :param show_name: If true, each log message will be prefixed with the pod
        name.
    :param logger: Logger to use for administrative messages, **not** for the
        pod logs (pod logs always go to stdout).
    :param formatter: Function which formats a log line. The default formatter
        takes care of unwrapping JSON stuff.

    This class allows managing multiple streams of logs from containers. Log
    streams are *not* automatically restarted, so it is best used with a watch
    on e.g. a label selector and the attempt to re-create log streams on any
    add/modify of a container.
    """

    def __init__(
            self,
            client: kclient.ApiClient,
            *,
            show_name: bool,
            logger: typing.Optional[logging.Logger] = None,
            formatter: typing.Callable[[bytes], str] = default_formatter,
            ):
        self._show_name = show_name
        self._client = client
        self._core_v1 = kclient.CoreV1Api(self._client)
        if logger is None:
            logger = logging.getLogger(__name__)
            # force INFO level to show container add lines by default
            logger.setLevel(logging.INFO)
        self._logger = logger
        self._formatter = formatter
        self._workers: typing.Optional[typing.Dict[
            typing.Tuple[str, str, str],
            asyncio.Task
        ]] = {}

    async def __aenter__(self) -> "LogViewer":
        return self

    async def __aexit__(  # type: ignore
            self,
            exc_type,
            exc_value,
            traceback,
    ) -> bool:
        await self.shutdown()
        # do *not* suppress the exception, if any
        return False

    def _worker_cleanup(
            self,
            namespace: str, pod: str, container: str,
            task: asyncio.Task
    ) -> None:
        try:
            task.result()
        except asyncio.CancelledError:
            pass
        except BaseException:
            self._logger.error(
                "log watcher for container %s of pod %s/%s died unexpectedly",
                namespace, pod, container,
                exc_info=True,
            )

        # during shutdown, don't attempt to remove ourselves.
        # also, only check this down here to not lose exception logs during
        # shutdown
        if self._workers is None:
            return
        try:
            existing = self._workers[namespace, pod, container]
        except KeyError:
            return
        if existing is task:
            del self._workers[namespace, pod, container]

    def _autocreate_worker(
            self,
            namespace: str, pod: str, container: str,
            tail: typing.Optional[int],
    ) -> None:
        assert self._workers is not None
        try:
            worker = self._workers[namespace, pod, container]
        except KeyError:
            pass
        else:
            if not worker.done():
                return

        worker = asyncio.create_task(
            self._worker(namespace, pod, container, tail)
        )
        worker.add_done_callback(
            functools.partial(self._worker_cleanup, namespace, pod, container)
        )
        self._workers[namespace, pod, container] = worker

    async def _worker(
            self,
            namespace: str, pod: str, container: str,
            tail: typing.Optional[int]) -> None:
        last_message: typing.Optional[float] = None
        while True:
            if last_message is not None:
                since = math.ceil(time.monotonic() - last_message)
                if since > 0:
                    extra_kwargs = {"since_seconds": since}
                else:
                    extra_kwargs = {"tail_lines": 0}
            else:
                extra_kwargs = {"tail_lines": tail or 0}

            try:
                resp = await self._core_v1.read_namespaced_pod_log(
                    pod, namespace,
                    container=container, follow=True,
                    _preload_content=False,
                    **extra_kwargs
                )
                resp.raise_for_status()
            except aiohttp.ClientResponseError as exc:
                if exc.status == 400:
                    # incorrect state, exit
                    return
                if exc.status == 404:
                    # deleted, exit
                    return
                raise

            if last_message is not None:
                self._logger.warning(
                    "log view of container %s in pod %s/%s restarted, messages"
                    " might've been lost or duplicated",
                    container, namespace, pod,
                )
            else:
                self._logger.info("new container %s in pod %s/%s",
                                  container, namespace, pod)

            # on restarts, we want to get the stream starting at this instant.
            last_message = time.monotonic()
            while True:
                try:
                    line = await resp.content.readline()
                except asyncio.TimeoutError:
                    # restart watch
                    break
                if not line:
                    # end of stream: this is either the end of the container's
                    # output (stopped), or the server closed our stream for
                    # inactivity.
                    # the two cases are hard to distinguish:
                    # - If a container is really quiet, we may have multiple
                    #   watches where not a single line is returned.
                    # - If a kubernetes API is configured that way, it may
                    #   close our watches mere seconds after the last message.
                    #
                    # The only reliable way is to also look at the container
                    # status. This is obviously racy:
                    # - If the container has been restarted between our log
                    #   interruption and the query, we want to resume logs
                    #   immediately anyway.
                    # - If the container has been stopped, but the server has
                    #   closed our logs for inactivity, we'll actually
                    #   potentially lose a few log lines. This could be worked
                    #   around by making a non-follow log read, but that's
                    #   again racy. We'll have to ignore this hopefully rare
                    #   case.
                    try:
                        status = (
                            await self._core_v1.read_namespaced_pod_status(
                                pod,
                                namespace,
                            )
                        ).status
                    except kclient.exceptions.ApiException as exc:
                        if exc.status == 404:
                            # deleted, we can exit safely
                            return
                        raise
                    for container_status in status.container_statuses:
                        if container_status.name != container:
                            continue
                        if not container_status.started:
                            # container is not running, exit
                            return
                        break
                    # container not found in status or running, retry
                    break

                last_message = time.monotonic()
                line = self._formatter(line)
                if self._show_name:
                    print(f"{click.style(pod, bold=True)}: {line}")
                else:
                    print(line)

    async def shutdown(self) -> None:
        """
        Gracefully shut down all log workers and wait for their termination.
        """
        if self._workers is None:
            return

        to_await = []
        for task in self._workers.values():
            task.cancel()
            to_await.append(task)
        self._workers = None
        if to_await:
            await asyncio.wait(to_await, return_when=asyncio.ALL_COMPLETED)
        for fut in to_await:
            # retrieve and discard all results, to avoid spurious warnings
            # note that exceptions will still be logged by self._worker_cleanup
            try:
                fut.result()
            except BaseException:
                pass

    async def add_container(
            self,
            namespace: str,
            pod: str,
            container: str,
            *,
            tail: typing.Optional[int] = None,
    ) -> None:
        """
        Add a log stream for a container.

        :param namespace: Namespace of the pod
        :param pod: Name of the pod
        :param container: Name of the container whose logs should be printed
        :param tail: Number of lines of old log messages to request

        If a log stream is already open for the given container, it will not be
        duplicated.
        """
        if self._workers is None:
            raise RuntimeError("log manager shut down, cannot add container")
        self._autocreate_worker(namespace, pod, container, tail)


async def watch_pod_logs(
        client: kclient.ApiClient,
        log_viewer: LogViewer,
        namespace: str,
        label_selector: str,
        container: str,
        *,
        tail: typing.Optional[int] = None,
) -> None:
    core_v1 = kclient.CoreV1Api(client)
    # TODO: handle loss of all pods somehow (it should exit then, I guess)
    while True:
        watch = kwatch.Watch()
        try:
            async for ev in watch.stream(
                    core_v1.list_namespaced_pod,
                    namespace=namespace,
                    label_selector=label_selector,
                    ):
                type_ = ev.get("type", "").lower()
                if type_ == "added" or type_ == "modified":
                    await log_viewer.add_container(
                        ev["object"].metadata.namespace,
                        ev["object"].metadata.name,
                        container,
                        tail=tail,
                    )
        except kclient.exceptions.ApiException as exc:
            if exc.status == 410:  # watch expired, restart
                continue
            raise
