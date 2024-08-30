RECOVERY_COMMAND_BEGIN_MARKER = "\n### BEGIN OF YAOOKCTL INJECTION ###\n"
RECOVERY_COMMAND_END_MARKER = "\n### END OF YAOOKCTL INJECTION ###"

INIT_RECOVERY_SCRIPT = """
if [[ "$MY_POD_NAME" != '{statefulset_name}-{volume_index}' ]]; then
    exit 0
else
    /init-raft.sh disaster-recovery
fi
"""  # noqa:E501


OVSDB_RECOVERY_SCRIPT = """
export INIT_CONTAINER_FINISHED_LOCKFILE=/etc/ovn/ovnnb_init_container_finished.txt
export FIRST_POD_FQDN={statefulset_name}-0.{statefulset_name}.yaook.svc.cluster.local
export HEADLESS_SERVICE_FQDN={statefulset_name}.yaook.svc.cluster.local
export CLUSTER_SIZE={cluster_size}
if [[ "$MY_POD_NAME" != '{statefulset_name}-{volume_index}' ]]; then
    sleep 120
    /init-raft.sh following-after-disaster
fi
"""  # noqa:E501


def _inject_command(
    start: str, end: str, body: str, into: str, fallback_index: int
) -> str:
    start_index = into.find(start)
    end_index = into.find(end)
    if start_index == -1 and end_index == -1:
        return (
            into[:fallback_index] + start + body + end + into[fallback_index:]
        )
    if start_index == -1 or end_index == -1:
        raise ValueError("found start or end marker, but not both")
    return (
        into[:start_index] + start + body + end + into[end_index + len(end):]
    )


def inject_ovsdb_recovery_command(
    shell_script: str, index: int, statefulset_name: str
) -> str:
    try:
        fallback_index = shell_script.rindex("\necho exec")
    except ValueError:
        raise ValueError("failed to find ovsdb-server command")
    return _inject_command(
        start=RECOVERY_COMMAND_BEGIN_MARKER,
        end=RECOVERY_COMMAND_END_MARKER,
        body=OVSDB_RECOVERY_SCRIPT.format(
            volume_index=index, statefulset_name=statefulset_name,
            cluster_size=index+1
        ),
        into=shell_script,
        fallback_index=fallback_index,
    )


def inject_init_recovery_command(index: int, statefulset_name: str) -> str:
    return (
        RECOVERY_COMMAND_BEGIN_MARKER
        + INIT_RECOVERY_SCRIPT.format(
            volume_index=index, statefulset_name=statefulset_name
        )
        + RECOVERY_COMMAND_END_MARKER
    )
