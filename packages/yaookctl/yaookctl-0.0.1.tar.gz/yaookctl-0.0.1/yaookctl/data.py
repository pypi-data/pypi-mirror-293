import click

import typing


class ContainerResolutionError(click.ClickException, LookupError):
    """
    Exception type to carry rich information about a
    :func:`resolve_component_container` failure.

    :param argname: Argument which needs at least to be provided for resolution
        to succeed.
    :param component: The component which was resolved, if any.
    :param plural: k8s resource plural, if any, for better diagnostics.
    :param instance: Resource instance name, if any, for better diagnostics.

    .. attribute:: argname

    .. attribute:: component

    """

    def __init__(
            self,
            argname: str,
            component: typing.Optional[str] = None,
            *,
            instance: typing.Optional[str] = None,
            plural: typing.Optional[str] = None,
    ):
        super().__init__(
            f"need {argname!r} to be set for resolution to complete"
        )
        self.argname = argname
        self.component = component
        self.instance = instance
        self.plural = plural

    def format_message(self) -> str:
        if self.plural is not None:
            if self.component is None:
                return (
                    "--pod/--component is required for "
                    f"{self.plural}/{self.instance or '*'}"
                )
            return (
                f"--container is required for component {self.component} of "
                f"{self.plural}/{self.instance or '*'}"
            )
        if self.component is None:
            return "--pod/--component is required for this command"
        return "--container is required for this command"


#: This is a list of resources to show for `yaookctl status openstack` and
#: similar future commands.
#:
#: The entries must be tuples which hold the API group, API version, the plural
#: and a human readable name.
OPENSTACK_RESOURCES = [
    ("yaook.cloud", "v1", "keystonedeployments", "Keystone"),
    ("yaook.cloud", "v1", "glancedeployments", "Glance"),
    ("yaook.cloud", "v1", "cinderdeployments", "Cinder"),
    ("yaook.cloud", "v1", "novadeployments", "Nova"),
    ("yaook.cloud", "v1", "neutrondeployments", "Neutron"),
    ("yaook.cloud", "v1", "barbicandeployments", "Barbican"),
    ("yaook.cloud", "v1", "gnocchideployments", "Gnocchi"),
    ("yaook.cloud", "v1", "ceilometerdeployments", "Ceilometer"),
    ("yaook.cloud", "v1", "heatdeployments", "Heat"),
    ("yaook.cloud", "v1", "horizondeployments", "Horizon"),
    ("compute.yaook.cloud", "v1", "novacomputenodes", "Nova Compute"),
    ("network.yaook.cloud", "v1", "neutronbgpdragents", "Neutron BGP"),
    ("network.yaook.cloud", "v1", "neutronl2agents", "Neutron L2"),
    ("network.yaook.cloud", "v1", "neutronl3agents", "Neutron L3"),
    ("network.yaook.cloud", "v1", "neutrondhcpagents", "Neutron DHCP"),
    ("network.yaook.cloud", "v1", "neutronovnagents",
     "Neutron OVN Controller"),
    ("network.yaook.cloud", "v1", "neutronovnbgpagents", "Neutron OVN BGP"),
]


#: This is a list of resources to show for `yaookctl status infra` and
#: similar future commands.
#:
#: The entries must be tuples which hold the API group, API version, the plural
#: and a human readable name.
INFRA_RESOURCES = [
    ("infra.yaook.cloud", "v1", "amqpservers", "RabbitMQ"),
    ("infra.yaook.cloud", "v1", "mysqlservices", "MySQL"),
    ("infra.yaook.cloud", "v1", "ovsdbservices", "OVSDB"),
]


#: This is a list of resources to show for `yaookctl status credentials` and
#: similar future commands.
#:
#: The entries must be tuples which hold the API group, API version, the plural
#: and a human readable name.
CREDENTIAL_RESOURCES = [
    ("infra.yaook.cloud", "v1", "amqpusers", "RabbitMQ"),
    ("infra.yaook.cloud", "v1", "mysqlusers", "MySQL"),
    ("yaook.cloud", "v1", "keystoneusers", "Keystone"),
    ("yaook.cloud", "v1", "keystoneendpoints", "Endpoints"),
]


#: This maps node profile names to sets of labels.
#:
#: This is used by `yaookctl status nodes` to show an abbreviation of the
#: Yaook scheduling keys assigned to a node.
#:
#: If labels occur in multiple profiles, it is best if those profiles can be
#: ordered in a strict superset in order to guarantee a sensible and consistent
#: representation.
NODE_PROFILES = {
    "compute": {
        "compute.yaook.cloud/hypervisor",
    },
    "l3": {
        "network.yaook.cloud/neutron-l3-agent",
    },
    "dhcp": {
        "network.yaook.cloud/neutron-dhcp-agent",
    },
    "ctl": {
        "any.yaook.cloud/api",
        "block-storage.yaook.cloud/cinder-any-service",
        "ceilometer.yaook.cloud/ceilometer-any-service",
        "compute.yaook.cloud/nova-any-service",
        "gnocchi.yaook.cloud/metricd",
        "infra.yaook.cloud/any",
        "infra.yaook.cloud/caching",
        "key-manager.yaook.cloud/barbican-any-service",
        "key-manager.yaook.cloud/barbican-keystone-listener",
        "operator.yaook.cloud/any",
    },
}


#: Aliases when the CLI requires a "kind" (actually a plural).
KIND_MAP = {
    "bgp": "neutronbgpdragents",
    "dhcp": "neutrondhcpagents",
    "l3": "neutronl3agents",
    "compute": "novacomputenodes",
    "l2": "neutronl2agents",
    "keystone": "keystonedeployments",
    "glance": "glancedeployments",
    "cinder": "cinderdeployments",
    "nova": "novadeployments",
    "neutron": "neutrondeployments",
    "heat": "heatdeployments",
    "gnocchi": "gnocchideployments",
    "ceilometer": "ceilometerdeployments",
    "mysql": "mysqlservices",
    "db": "mysqlservices",
    "amqp": "amqpservers",
    "rabbitmq": "amqpservers",
    "mq": "amqpservers",
    "ovsdb": "ovsdbservices",
    "ovncontroller": "neutronovnagents",
    "ovnbgp": "neutronovnbgpagents",
}


#: Allowlist of plurals for `yaookctl force-upgrade`.
#:
#: This must only contain plurals which represent an agent of some kind.
#: Running force-upgrade on something like KeystoneDeployment would be
#: *desasterous*!
UPGRADABLE_KINDS = {
    "neutronbgpdragents",
    "neutronl3agents",
    "neutronl2agents",
    "novacomputenodes",
    "neutrondhcpagents",
}


#: Map those plurals which are not in the yaook.cloud group to their respective
#: API group.
#:
#: This is used to construct kclient.CustomApi calls from just the plural.
API_GROUP_MAP = {
    "neutronbgpdragents": "network.yaook.cloud",
    "neutrondhcpagents": "network.yaook.cloud",
    "neutronl2agents": "network.yaook.cloud",
    "neutronl3agents": "network.yaook.cloud",
    "neutronovnagents": "network.yaook.cloud",
    "neutronovnbgpagents": "network.yaook.cloud",
    "novacomputenodes": "compute.yaook.cloud",
    "mysqlservices": "infra.yaook.cloud",
    "mysqlusers": "infra.yaook.cloud",
    "amqpservers": "infra.yaook.cloud",
    "amqpusers": "infra.yaook.cloud",
    "ovsdbservices": "infra.yaook.cloud",
}


#: List the plurals for which we expect multiple instances.
#:
#: The behaviour of the CLI differs slightly for those, because the second
#: argument of e.g. `yaookctl logs` is then assumed to be the instance of the
#: resource instead of a component.
MULTI_INSTANCE_PLURALS = {
    "neutronbgpdragents",
    "neutronl3agents",
    "neutronl2agents",
    "novacomputenodes",
    "neutrondhcpagents",
    "neutronovnagents",
    "neutronovnbgpagents",
    "mysqlservices",
    "mysqlusers",
    "amqpservers",
    "amqpusers",
    "ovsdbservices",
}


#: A subset of :data:`MULTI_INSTANCE_PLURALS` which *also* have multiple pods
#: in their components.
#:
#: This further adjusts selection of pod targets to avoid "multiple pods found"
#: errors.
MULTI_POD_PLURALS = {
    "amqpservers",
    "mysqlservices",
    "ovsdbservices",
}


#: Provide a default for a container name for commands which operate on
#: containers.
#:
#: This maps a plural and component name to a container name. If this dict has
#: no entry for a given combination, the user will be required to provide a
#: container name explicitly.
DEFAULT_CONTAINER_MAP = typing.cast(
    # this cast only exists to make mypy shut up when we pass None as part of
    # the tuple to .get().
    typing.Dict[typing.Tuple[str, typing.Optional[str]], str],
    {
        ("neutronbgpdragents", "bgp_dragent"): "neutron-bgp-dragent",
        ("neutronl2agents", "l2_ovs_vswitchd"): "ovs-vswitchd",
        ("neutronl2agents", "l2_ovsdb_server"): "ovsdb-server",
        ("neutronl2agents", "l2_agent"): "neutron-openvswitch-agent",
        ("neutronl3agents", "l3_agent"): "neutron-l3-agent",
        ("neutrondhcpagents", "dhcp_agent"): "neutron-dhcp-agent",
        ("neutronovnagents", "ovn_controller"): "ovn-controller",
        ("neutronovnagents", "ovs_vswitchd"): "ovs-vswitchd",
        ("neutronovnagents", "ovsdb_server"): "ovsdb-server",
        ("neutronovnbgpagents", "bgp_agent"): "ovn-bgp-agent",
        ("novacomputenodes", "compute"): "nova-compute",
        ("novadeployments", "nova_api"): "nova-api",
        ("novadeployments", "nova_scheduler_sfs"): "nova-scheduler",
        ("novadeployments", "nova_conductor_sfs"): "nova-conductor",
        ("novadeployments", "placement_api"): "placement",
        ("novadeployments", "nova_metadata"): "nova-metadata",
        ("novadeployments", "vnc"): "nova-novncproxy",
        ("neutrondeployments", "api_deployment"): "neutron-api",
        ("neutrondeployments", "northd"): "northd",
        ("keystonedeployments", "api"): "keystone",
        ("glancedeployments", "api_deployment"): "glance-api",
        ("cinderdeployments", "api_deployment"): "cinder-api",
        ("cinderdeployments", "volume_deployment"): "cinder-volume",
        ("mysqlservices", "database"): "mariadb-galera",
        ("amqpservers", "amqpserver"): "rabbitmq",
        ("ovsdbservices", "ovsdb"): "ovsdb",
    },
)


#: Provide a default for a component for commands which need it.
#:
#: This maps a plural plus an optional container name to a componet name. Note
#: that not all contexts provide the container name, so `(plural, None)` should
#: always be part of the mapping if `(plural, _)` is part of it.
#:
#: If the context contains a preferred container name and no entry matches
#: that, the None entry is returned.
DEFAULT_COMPONENT_MAP = {
    ("novadeployments", None): "nova_api",
    ("neutrondeployments", None): "api_deployment",
    ("neutronbgpdragents", None): "bgp_dragent",
    ("neutronl2agents", None): "l2_agent",
    ("neutronl2agents", "ovs-vswitchd"): "l2_ovs_vswitchd",
    ("neutronl2agents", "ovsdb-server"): "l2_ovsdb_server",
    ("neutronl3agents", None): "l3_agent",
    ("neutrondhcpagents", None): "dhcp_agent",
    ("neutronovnagents", None): "ovn_controller",
    ("neutronovnbgpagents", None): "bgp_agent",
    ("novacomputenodes", None): "compute",
    ("glancedeployments", None): "api_deployment",
    ("mysqlservices", None): "database",
    ("amqpservers", None): "amqpserver",
    ("ovsdbservices", None): "ovsdb",
}


#: Shorthands for components.
#:
#: In commands which need a component, this allows to define per-plural
#: aliases for the components to allow shorthands like
#: `yaookctl logs nova api` instead of `yaookctl logs nova nova_api`.
COMPONENT_ALIAS_MAP = typing.cast(
    # this cast only exists to make mypy shut up when we pass None as part of
    # the tuple to .get().
    typing.Dict[typing.Tuple[str, typing.Optional[str]], str],
    {
        ("novadeployments", "api"): "nova_api",
        ("novadeployments", "scheduler"): "nova_scheduler_sfs",
        ("novadeployments", "conductor"): "nova_conductor_sfs",
        ("novadeployments", "metadata"): "nova_metadata",
        ("novadeployments", "placement"): "placement_api",
        ("novadeployments", "vnc"): "vnc",
        ("neutrondeployments", "api"): "api_deployment",
        ("glancedeployments", "api"): "api_deployment",
        ("cinderdeployments", "api"): "api_deployment",
        ("cinderdeployments", "volume"): "volume_deployment",
        ("neutronbgpdragents", "agent"): "bgp_dragent",
        ("neutronl2agent", "agent"): "l2_agent",
        ("neutronl2agent", "ovs"): "l2_ovs_vswitchd",
        ("neutronl2agent", "ovsdb"): "l2_ovsdb_server",
        ("neutronl3agents", "agent"): "l3_agent",
        ("neutrondhcpagents", "agent"): "dhcp_agent",
        ("neutronovnagents", "controller"): "ovn_controller",
        ("neutronovnagents", "ovs"): "ovs_vswitchd",
        ("neutronovnagents", "ovsdb"): "ovsdb_server",
        ("neutronovnbgpagents", "agent"): "bgp_agent",
    },
)


#: Shorthands for database components.
#:
#: In commands which target a database, this allows to define per-plural
#: aliases for the database components to allow shorthands like
#: `yaookctl sql nova api` instead of `yaookctl sql nova api_db`.
DATABASE_ALIAS_MAP = typing.cast(
    # this cast only exists to make mypy shut up when we pass None as part of
    # the tuple to .get().
    typing.Dict[typing.Tuple[str, typing.Optional[str]], str],
    {
        ("novadeployments", "cell0"): "cell0_db",
        ("novadeployments", "cell1"): "cell1_db",
        ("novadeployments", "api"): "api_db",
        ("novadeployments", "placement"): "placement_db",
    },
)


def get_default_component(
        plural: str,
        selected_container: typing.Optional[str] = None,
) -> typing.Optional[str]:
    """
    Return the default component for a given plural, potentially taking the
    selected container name into account.

    :param plural: The k8s plural of the resource.
    :param selected_container: Optionally, a container name the user has
        requested.
    """
    try:
        return DEFAULT_COMPONENT_MAP[(plural, selected_container)]
    except KeyError:
        return DEFAULT_COMPONENT_MAP.get((plural, None))


def resolve_component(
        plural: str,
        component: typing.Optional[str],
        *,
        selected_container: typing.Optional[str] = None,
) -> typing.Optional[str]:
    """
    Find the best match for a component based on an optional component name
    (potentially an alias) and an optional preferred target container.

    :param plural: The k8s resource plural to work with.
    :param component: Optional Yaook component name or alias.
    :param selected_container: Optional container name to target.
    :return: The resolved Yaook component name, if any.

    If the component is a defined alias (see :data:`COMPONENT_ALIAS_MAP`), the
    resolved alias is returned. Otherwise, :func:`get_default_component` is
    used to make a guess.

    If neither method succeeds, :data:`None` is returned.
    """
    component = COMPONENT_ALIAS_MAP.get((plural, component), component)
    if component is not None:
        return component
    return get_default_component(plural, selected_container=selected_container)


def resolve_component_container(
        plural: str,
        container: typing.Optional[str],
        component: typing.Optional[str],
) -> typing.Tuple[str, str]:
    """
    Resolve the provided arguments to a pair of component and container name.

    :param plural: The k8s resource plural to work with.
    :param component: Optional Yaook component name or alias.
    :param container: Optional container name to target.
    :raises ContainerResolutionError: There are no sufficient defaults defined
        and more data is required. More information can be retrieved from the
        exception attributes.

    After resolving the component using :func:`resolve_component`, the
    container is looked up from :data:`DEFAULT_CONTAINER_MAP` if it is not
    already provided.
    """

    component = resolve_component(
        plural, component,
        selected_container=container,
    )
    container = container or DEFAULT_CONTAINER_MAP.get((plural, component))
    if component is None:
        raise ContainerResolutionError("component", plural=plural)
    if container is None:
        raise ContainerResolutionError("container", component, plural=plural)
    return component, container
