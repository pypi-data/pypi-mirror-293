import logging
import json
import os
import typing

import kubernetes_asyncio.client as kclient


logger = logging.getLogger(__name__)


INIT_SCRIPT = """\
container_id="$0"
sandbox_id="$(crictl --runtime-endpoint unix:///yaook/debug/crictl/run/containerd/containerd.sock inspect "$container_id" | jq -r .info.sandboxID)"
container_pid="$(ps --no-headers -Ao pid,cmd | grep -F "$sandbox_id" | grep -vF grep | awk '{print $1}')"
if [ -z "$container_pid" ]; then
    echo "failed to find container PID"
    exit 255
fi
root_pid="$(ps --no-headers -o pid --ppid "$container_pid" | head -n1)"
if [ -z "$root_pid" ]; then
    echo "failed to find root PID"
    exit 255
fi
mkdir -p /.yaookctl-proc
nsenter -t "$root_pid" -p mount -t proc proc /.yaookctl-proc
exec nsenter -t "$root_pid" -n -i -u -p -C "$1"
"""  # noqa:E501


def transform_volume(volume: kclient.V1Volume) -> kclient.V1Volume:
    if volume.empty_dir is not None:
        logging.warn("volume %s is of type emptyDir, which will not work "
                     "correctly", volume.name)

    return volume


def make_debugger_pod_spec(
        target_pod: kclient.V1Pod,
        target_container: typing.Optional[str] = None,
        force_image: typing.Optional[str] = None,
        force_shell: typing.Optional[str] = None,
) -> kclient.V1PodSpec:
    node = target_pod.spec.node_name
    if node is None:
        raise ValueError("target pod is not scheduled")

    if force_image is not None:
        image = force_image
    else:
        image = (target_pod.metadata.annotations or {}).get(
            "debug.yaook.cloud/image",
            os.environ.get(
                "YAOOKCTL_DEFAULT_DEBUG_IMAGE",
                "registry.yaook.cloud/yaook/debugbox:devel",
            )
        )

    image_pull_policy = "IfNotPresent"
    if image.endswith(":devel"):
        image_pull_policy = "Always"

    if force_shell is not None:
        shell = force_shell
    else:
        shell = (target_pod.metadata.annotations or {}).get(
            "debug.yaook.cloud/shell",
            os.environ.get(
                "YAOOKCTL_DEFAULT_DEBUG_SHELL",
                "/bin/bash",
            )
        )

    container_id = [
        container_status.container_id.split("://", 2)[1]
        for container_status in target_pod.status.container_statuses
        if (target_container is None or
            container_status.name == target_container)
    ][0]

    container = [
        container
        for container in target_pod.spec.containers
        if target_container is None or container.name == target_container
    ][0]

    try:
        volume_annotation = json.loads(
            (target_pod.metadata.annotations or {})[
                "debug.yaook.cloud/volumes"
            ]
        )
    except KeyError:
        volume_mounts = container.volume_mounts
        relevant_volumes = set(mount.name for mount in volume_mounts)
        # we filter out irrelevant volumes here to avoid spurious warnings
        # about emptyDir.
        volumes = [
            transform_volume(volume)
            for volume in target_pod.spec.volumes
            if volume.name in relevant_volumes
        ]
    else:
        volume_map = {
            volume.name: volume
            for volume in target_pod.spec.volumes
        }

        volumes = []
        volume_mounts = []
        for volume_mount in volume_annotation:
            volumes.append(transform_volume(volume_map[volume_mount["name"]]))
            volume_mounts.append(kclient.V1VolumeMount(
                name=volume_mount["name"],
                mount_path=volume_mount["mountPath"],
                sub_path=volume_mount.get("subPath"),
            ))

    volumes.append(
        kclient.V1Volume(
            name="crictl-run",
            host_path=kclient.V1HostPathVolumeSource(
                path="/run/containerd"
            ),
        ),
    )
    volume_mounts.append(
        kclient.V1VolumeMount(
            name="crictl-run",
            mount_path="/yaook/debug/crictl/run/containerd",
        )
    )

    return kclient.V1PodSpec(
        containers=[
            kclient.V1Container(
                name="debugger",
                image=image,
                volume_mounts=volume_mounts,
                command=[
                    "/bin/sh", "-euc", INIT_SCRIPT,
                    container_id,
                    shell,
                ],
                tty=True,
                stdin=True,
                security_context=kclient.V1SecurityContext(
                    privileged=True,
                ),
                image_pull_policy=image_pull_policy,
                env=container.env,
            )
        ],
        host_network=True,
        host_pid=True,
        host_ipc=True,
        volumes=volumes,
        restart_policy="Never",
        node_name=node,
    )
