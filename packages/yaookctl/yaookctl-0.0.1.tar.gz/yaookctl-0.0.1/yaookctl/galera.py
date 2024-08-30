import asyncio
import dataclasses
import json
import re
import subprocess
import typing

import kubernetes_asyncio.client as kclient
import kubernetes_asyncio.stream as kstream


RECOVERED_POSITION_RE = re.compile(
    rb"WSREP: Recovered position: (?P<uuid>[a-f0-9-]+):(?P<seqno>[0-9-]+)",
)

RECOVERY_COMMAND_BEGIN_MARKER = "\n### BEGIN OF YAOOKCTL INJECTION ###\n"
RECOVERY_COMMAND_END_MARKER = "\n### END OF YAOOKCTL INJECTION ###"

# the init.sql is supposed to force the passwords to be correct on recovery
# we run it on *all* nodes because apparently the stuff from init-file are not
# neccessarily replicated correctly...
RECOVERY_SCRIPT = """
cat > /tmp/init.sql <<EOF
ALTER USER '$MARIADB_ROOT_USER' IDENTIFIED BY '$MARIADB_ROOT_PASSWORD';
ALTER USER '$MARIADB_GALERA_MARIABACKUP_USER'@'localhost' IDENTIFIED BY '$MARIADB_GALERA_MARIABACKUP_PASSWORD';
EOF
MARIADB_EXTRA_FLAGS="$MARIADB_EXTRA_FLAGS --init-file=/tmp/init.sql"
if [[ "$MY_POD_NAME" == '{statefulset_name}-{volume_index}' ]]; then
    export MARIADB_GALERA_CLUSTER_BOOTSTRAP=yes
    export MARIADB_GALERA_FORCE_SAFETOBOOTSTRAP=yes
else
    sleep 15
fi
"""  # noqa:E501

ZERO_UUID = "00000000-0000-0000-0000-000000000000"


def _inject_command(
        start: str,
        end: str,
        body: str,
        into: str,
        fallback_index: int) -> str:
    start_index = into.find(start)
    end_index = into.find(end)
    if start_index == -1 and end_index == -1:
        return (
            into[:fallback_index] + start + body + end + into[fallback_index:]
        )
    if start_index == -1 or end_index == -1:
        raise ValueError("found start or end marker, but not both")
    return into[:start_index] + start + body + end + into[end_index+len(end):]


def parse_grastate_raw(data: bytes) -> typing.Dict[bytes, bytes]:
    result = {}
    for line in data.split(b"\n"):
        line = line.lstrip()
        if not line or line.startswith(b"#"):
            continue
        k, v = line.split(b":", 1)
        if k in result:
            raise ValueError(f"duplicate key in grastate: {k!r}")
        result[k] = v.lstrip()
    return result


@dataclasses.dataclass(frozen=True)
class GraState:
    safe_to_bootstrap: bool
    uuid: str
    seqno: int

    @classmethod
    def parse(cls, data: bytes) -> "GraState":
        kv_data = parse_grastate_raw(data)
        try:
            version = kv_data[b"version"]
        except KeyError:
            raise ValueError("unable to find version in grastate") from None
        if version != b"2.1":
            raise ValueError(f"unsupported grastate version: {version!r}")

        uuid = kv_data[b"uuid"].decode("ascii").strip()
        seqno = int(kv_data[b"seqno"].decode("ascii").strip())
        safe_to_bootstrap = kv_data[b"safe_to_bootstrap"].strip() == b"1"
        return cls(
            uuid=uuid,
            seqno=seqno,
            safe_to_bootstrap=safe_to_bootstrap,
        )

    @classmethod
    def from_recovery(cls, log: bytes) -> "GraState":
        for line in log.split(b"\n"):
            match = RECOVERED_POSITION_RE.search(line)
            if not match:
                continue
            data = match.groupdict()
            return cls(
                uuid=data["uuid"].decode("ascii"),
                seqno=int(data["seqno"].decode("ascii")),
                safe_to_bootstrap=False,
            )
        raise ValueError("failed to find recovery line in log")

    @classmethod
    def zero(cls) -> "GraState":
        return cls(
            uuid=ZERO_UUID,
            safe_to_bootstrap=False,
            seqno=-1,
        )


async def pod_exec(
        client: kclient.ApiClient,
        *,
        namespace: str,
        pod: str,
        container: str,
        command: typing.Sequence[str],
) -> subprocess.CompletedProcess:
    async with kstream.WsApiClient(client.configuration) as ws_client:
        ws_core_v1 = kclient.CoreV1Api(ws_client)
        websock = await ws_core_v1.connect_get_namespaced_pod_exec(
            pod,
            namespace,
            container=container,
            command=command,
            tty=False,
            stdin=False,
            stdout=True,
            stderr=True,
            _preload_content=False,
        )
        stdout = bytearray()
        stderr = bytearray()
        while True:
            msg = await websock.receive_bytes()
            if msg[0] == 0x01:
                # stdout
                stdout.extend(msg[1:])
            elif msg[0] == 0x02:
                # stderr
                stderr.extend(msg[1:])
            elif msg[0] == 0x03:
                # end of command
                break
            else:
                raise RuntimeError(
                    "exec websocket protocol violation: unknown message "
                    f"type: {msg[0]!r}",
                )

        info = json.loads(msg[1:].decode("utf-8"))
        if info["status"] == "Failure":
            if info["reason"] == "NonZeroExitCode":
                try:
                    returncode, = [
                        int(cause["message"])
                        for cause in info["details"]["causes"]
                    ]
                except (ValueError, TypeError) as exc:
                    raise ValueError(
                        f"failed to process response JSON {info!r}: "
                        f"failed to read returncode: {exc}"
                    )
            else:
                raise RuntimeError(
                    f"failed to execute command via kubernetes: {info!r}",
                )
        elif info["status"] == "Success":
            returncode = 0
        else:
            raise RuntimeError(
                f"unexpected response JSON: {info!r}",
            )
        await websock.close()
        return subprocess.CompletedProcess(
            args=command,
            returncode=returncode,
            stdout=bytes(stdout),
            stderr=bytes(stderr),
        )


async def get_grastate(
        client: kclient.ApiClient,
        namespace: str,
        image: str,
        pvc_name: str,
) -> bytes:
    pod = kclient.V1Pod(
        metadata=kclient.V1ObjectMeta(
            generate_name="yaookctl-grastate-probe-",
            labels={
                "app.kubernetes.io/name": "yaookctl",
                "app.kubernetes.io/component": "grastate-probe",
                "app.kubernetes.io/instance": pvc_name,
            },
        ),
        spec=kclient.V1PodSpec(
            restart_policy="Never",
            containers=[
                kclient.V1Container(
                    name="grastate-probe",
                    command=[
                        "/bin/sleep", "infinity",
                    ],
                    image=image,
                    volume_mounts=[
                        kclient.V1VolumeMount(
                            name="galera-data",
                            mount_path="/mnt",
                        ),
                    ],
                )
            ],
            termination_grace_period_seconds=1,
            volumes=[
                kclient.V1Volume(
                    name="galera-data",
                    persistent_volume_claim=kclient.V1PersistentVolumeClaimVolumeSource(  # noqa:E501
                        claim_name=pvc_name,
                    ),
                ),
            ],
        )
    )
    core_v1 = kclient.CoreV1Api(client)

    pod = await core_v1.create_namespaced_pod(
        namespace,
        pod,
    )
    try:
        # we have to wait until the pod gets ready
        while True:
            pod_status = await core_v1.read_namespaced_pod_status(
                pod.metadata.name,
                namespace,
            )
            container_statuses = (
                pod_status.status and
                pod_status.status.container_statuses
            ) or []
            if not container_statuses:
                continue
            if container_statuses[0].started and container_statuses[0].ready:
                break
            await asyncio.sleep(1)

        state = await pod_exec(
            client,
            namespace=namespace,
            pod=pod.metadata.name,
            container="grastate-probe",
            command=["/bin/cat", "/mnt/data/grastate.dat"],
        )
        state.check_returncode()
        return state.stdout
    finally:
        await core_v1.delete_namespaced_pod(pod.metadata.name, namespace)


async def recover_grastate(
        client: kclient.ApiClient,
        namespace: str,
        image: str,
        pvc_name: str,
) -> bytes:
    pod = kclient.V1Pod(
        metadata=kclient.V1ObjectMeta(
            generate_name="yaookctl-grastate-probe-",
            labels={
                "app.kubernetes.io/name": "yaookctl",
                "app.kubernetes.io/component": "grastate-probe",
                "app.kubernetes.io/instance": pvc_name,
            },
        ),
        spec=kclient.V1PodSpec(
            restart_policy="Never",
            security_context=kclient.V1PodSecurityContext(
                run_as_user=2500010,
                run_as_group=2500010,
            ),
            containers=[
                kclient.V1Container(
                    name="grastate-probe",
                    command=[
                        "/bin/sleep", "infinity",
                    ],
                    image=image,
                    volume_mounts=[
                        kclient.V1VolumeMount(
                            name="galera-data",
                            mount_path="/bitnami/mariadb",
                        ),
                        kclient.V1VolumeMount(
                            name="tmp",
                            mount_path="/opt/bitnami/mariadb/tmp",
                        ),
                    ],
                )
            ],
            termination_grace_period_seconds=1,
            volumes=[
                kclient.V1Volume(
                    name="galera-data",
                    persistent_volume_claim=kclient.V1PersistentVolumeClaimVolumeSource(  # noqa:E501
                        claim_name=pvc_name,
                    ),
                ),
                kclient.V1Volume(
                    name="tmp",
                    empty_dir=kclient.V1EmptyDirVolumeSource(),
                ),
            ],
        )
    )
    core_v1 = kclient.CoreV1Api(client)

    pod = await core_v1.create_namespaced_pod(
        namespace,
        pod,
    )
    try:
        # we have to wait until the pod gets ready
        while True:
            pod_status = await core_v1.read_namespaced_pod_status(
                pod.metadata.name,
                namespace,
            )
            container_statuses = (
                pod_status.status and
                pod_status.status.container_statuses
            ) or []
            if not container_statuses:
                continue
            if container_statuses[0].started and container_statuses[0].ready:
                break
            await asyncio.sleep(1)

        state = await pod_exec(
            client,
            namespace=namespace,
            pod=pod.metadata.name,
            container="grastate-probe",
            command=["mariadbd", "--wsrep-recover"],
        )
        state.check_returncode()
        return state.stdout
    finally:
        await core_v1.delete_namespaced_pod(pod.metadata.name, namespace)


def inject_recovery_command(
        shell_script: str,
        index: int,
        statefulset_name: str) -> str:
    try:
        fallback_index = shell_script.rindex("\nexec ")
    except ValueError:
        raise ValueError("failed to find exec command")
    return _inject_command(
        start=RECOVERY_COMMAND_BEGIN_MARKER,
        end=RECOVERY_COMMAND_END_MARKER,
        body=RECOVERY_SCRIPT.format(volume_index=index,
                                    statefulset_name=statefulset_name),
        into=shell_script,
        fallback_index=fallback_index,
    )
