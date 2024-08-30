# yaookctl

A command-line tool to inspect the health of a Yaook cluster using information obtained from Kubernetes.

## Installation

```console
$ pip3 install -e .
```

### Shell completion

To enable shell completion, add the following to your shell configuration:

* For bash: `eval "$(_YAOOKCTL_COMPLETE=bash_source yaookctl)"`
* For zsh: `eval "$(_YAOOKCTL_COMPLETE=zsh_source yaookctl)"`
* For fish: `eval (env _YAOOKCTL_COMPLETE=fish_source yaookctl)`

See also the upstream documentation on [enabling shell completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion).

## Usage

You need to have a valid `KUBECONFIG` set to use `yaookctl`. If you installed yaookctl using `pip`, you can invoke it using `yaookctl`. Otherwise, you may have to use `python3 -m yaookctl`.

### Obtain status overview

```console
$ yaookctl -n default status openstack
+------------+----------+------------+---------------------+----------------------------+-----------+
| Kind       | Name     | Status     | Since               | Message                    | Workloads |
+------------+----------+------------+---------------------+----------------------------+-----------+
| Keystone   | keystone | Success    | 2022-04-04 13:27:38 |                            | all ready |
| Glance     | glance   | Dependency | 2022-04-04 13:23:13 | Waiting for api_deployment | all ready |
| Cinder     | cinder   | Success    | 2022-04-04 13:39:42 |                            | all ready |
| Nova       | <absent> |            |                     |                            |           |
| Neutron    | <absent> |            |                     |                            |           |
| Barbican   | <absent> |            |                     |                            |           |
| Gnocchi    | <absent> |            |                     |                            |           |
| Ceilometer | <absent> |            |                     |                            |           |
| Heat       | <absent> |            |                     |                            |           |
| Horizon    | <absent> |            |                     |                            |           |
+------------+----------+------------+---------------------+----------------------------+-----------+
$ yaookctl -n default status infra
+----------+----------------+---------+---------------------+---------+-----------+
| Kind     | Name           | Status  | Since               | Message | Workloads |
+----------+----------------+---------+---------------------+---------+-----------+
| MySQL    | cinder-686dh   | Success | 2022-04-04 13:28:30 |         | all ready |
| RabbitMQ | cinder-crlhg   | Success | 2022-04-04 13:26:42 |         | all ready |
| MySQL    | glance-wcqrn   | Success | 2022-04-04 13:27:19 |         | all ready |
| MySQL    | keystone-htfql | Success | 2022-04-04 13:27:35 |         | all ready |
+----------+----------------+---------+---------------------+---------+-----------+
```

### Get a shell

```console
$ yaookctl shell nova api
note: selecting pod nova-api-58cd999ddf-vglkd out of 3
root@nova-api-58cd999ddf-vglkd:/# exit
$ yaookctl shell l2 cmp-yopo-0361
[root@cmp-yopo-0361 /]# exit
```

### Get a debug pod

```console
$ yaookctl debug keystone api
note: selecting pod keystone-api-5544d7cfc7-4c7g6 out of 3

If you don't see a command prompt, try pressing enter.
root@keystone-api-5544d7cfc7-4c7g6:/# exit

$ yaookctl debug l2 m1r2

If you don't see a command prompt, try pressing enter.
root@m1r2:/# exit
```

#### What is the difference between the debug pod and a shell?

The debug pod is a separate pod, which hooks into the target pod. The debug pod runs a version of [debugbox](https://gitlab.com/yaook/images/debugbox) by default (the target pod may override that).

The key differences are:

- The debug pod has its own filesystem, hence it comes with all the good tools installed. No more `bash: tcpdump: command not found`!
- The debug pod is a separate pod; It can only partially hook into the environment of the target pod. In particular, the following things are currently **not** identical to the target environment:

    - The debug pod may have more privileges.
    - Any `emptyDir` volumes will be empty in the debug pod (the CLI warns about this), which may be a problem if they contain sockets or other runtime data.

    There may be more, not yet known, differences.

- Spawning the debug pod may require to pull an image, which may not work if your cluster is fatally broken or offline.

### Get a MySQL Shell

```console
$ yaookctl sql neutron
note: selecting pod neutron-mqrzv-db-0 out of 3
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 154779
Server version: 10.2.43-MariaDB-log Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> Bye
```

In cases where multiple databases exist, you can either guess (sensible aliases
exist) or you can get a listing like this:

```console
$ yaookctl sql nova
multiple databases found for novadeployments/nova
nova-api-dn7bp  api_db
nova-cell0-gk8xf        cell0_db
nova-cell1-2x77l        cell1_db
placement-placement-4vfgw       placement_db
```

The second column of the listing is what you need to pass as argument to get
a shell:

```console
$ yaookctl sql nova cell1_db
```

For nova, aliases like these exist:

```console
$ yaookctl sql nova cell1
$ yaookctl sql nova api
```

### Watch logs

The log watch will follow appearing containers, so you'll have a continuous log stream throughout e.g. a `kubectl rollout restart deploy neutron-api`.

```console
$ yaookctl logs neutron api
==> new container: yaook/neutron-api-847576c979-cbnpz
2022-04-19 11:24:04 INFO neutron.wsgi 127.0.0.1 "GET / HTTP/1.1" status: 200  len: 227 time: 0.0043900
==> new container: yaook/neutron-api-847576c979-8ddl7
2022-04-19 11:24:08 INFO neutron.wsgi 127.0.0.1 "GET / HTTP/1.1" status: 200  len: 227 time: 0.0044227
2022-04-19 11:24:08 INFO neutron.wsgi 127.0.0.1 "GET / HTTP/1.1" status: 200  len: 227 time: 0.0044687
^C
Aborted!
```

For agents, you have to either pass the node name:

```console
$ yaookctl logs l3 m1r1
==> new container: yaook/neutron-l3-q6wgs-0
2022-04-15 11:50:58 INFO oslo.messaging._drivers.impl_rabbit [f7435328-79c8-46f8-a53b-dafc7f3edf1f] Reconnected to AMQP server on neutron-smq9g.yaook:5671 via [amqp] client with port 44954.
^C
Aborted!
```

Or `--all` to get the logs from all nodes:

```console
$ yaookctl logs l3 --all
==> new container: yaook/neutron-l3-nxk26-0
2022-04-15 11:50:51 INFO oslo.messaging._drivers.impl_rabbit [7da506e5-ce85-48d0-a3df-8bdbce5bcda1] Reconnected to AMQP server on neutron-smq9g.yaook:5671 via [amqp] client with port 57932.
==> new container: yaook/neutron-l3-96426-0
==> new container: yaook/neutron-l3-q6wgs-0
2022-04-15 11:50:58 INFO oslo.messaging._drivers.impl_rabbit [253b2517-1cca-4ad4-a492-ff2044650769] Reconnected to AMQP server on neutron-smq9g.yaook:5671 via [amqp] client with port 50774.
2022-04-15 11:50:58 INFO oslo.messaging._drivers.impl_rabbit [f7435328-79c8-46f8-a53b-dafc7f3edf1f] Reconnected to AMQP server on neutron-smq9g.yaook:5671 via [amqp] client with port 44954.
^C
Aborted!
```

### Force recreation of agent

Yaook generally will avoid disruption of the data plane at all cost. Sometimes, that'll make things get stuck, e.g. if instances cannot be live-migrated from a compute node which needs a config update.

To circumvent all of these safety mechanisms, you can use the following command:

```console
$ yaookctl force-upgrade compute $nodename
```

This will strip the finalizers and delete the compute object. If the node is not elegible as a compute node anymore, **this will cause permanent data loss**. If the compute service does not come up afterward, it will make the VMs unmanageable and may cause other issues.

Same holds for `l2`, `l3`, `dhcp` and `bgp` objects.

**Known Issue:** There is a possibility that the nova-compute custom resource could be shown as up, but in OpenStack it is shown as down. This will cause the nova-operator to continue eviction of the next service.


### Pause/Unpause

Yaook supports a "pause" annotation on the custom resources
(keystonedeployment, mysqlservice, amqpuser, ...)
which prevents the corresponding operator from reconciling the resource.
That is useful when you need to do an operation not supported by the operator
and do not want it to interfere.

To pause a resource:

```console
$ yaookctl pause mysql keystone-fmwlf --comment 'Optional comment used as annotation value'
```

To unpause a resource:

```console
$ yaookctl unpause mysql keystone-fmwlf
```

**Note:** You can only pause operators reconciling Yaook custom resources.
You cannot use pause to prevent an operator from *changing* a resource it manages.
(For instance,
you cannot pause the MySQLService statefulset
to prevent the operator from reverting a change you did --
you have to pause the MySQLService resource instead.)

### Galera recovery tools

Sometimes, a galera cluster breaks.
To fix that, the following helper commands are provided.

**Note:** Before using any of these,
you have to scale the StatefulSet down to 0 replicas:

```sh
kubectl -n yaook scale sts $DBNAME-db --replicas=0
```

To do so, you'll have to halt the infra operator
or pause the MySQLService
(see above for `yaookctl pause`).

#### find-wsrep-positions

This command extracts the last wsrep position from the MySQLService PVCs,
running `mariadbd --wsrep-recover` if necessary.
This command will refuse to operate if the StatefulSet still has replicas,
because it may do writes to the PVC.

```console
$ yaookctl galera find-wsrep-positions keystone-fmwlf
+--------------------------+--------------------------------------+-------+-------+------------+-------+
| PVC Name                 | UUID                                 | SeqNo | Safe? | Recovered? | Best  |
+--------------------------+--------------------------------------+-------+-------+------------+-------+
| data-keystone-fmwlf-db-0 | 02972cfb-1c8c-11ed-9639-4b191e1f7ba5 | 2217  | False | False      | False |
| data-keystone-fmwlf-db-1 | 02972cfb-1c8c-11ed-9639-4b191e1f7ba5 | 2218  | False | False      | False |
| data-keystone-fmwlf-db-2 | 02972cfb-1c8c-11ed-9639-4b191e1f7ba5 | 2219  | True  | False      | True  |
+--------------------------+--------------------------------------+-------+-------+------------+-------+
```

#### force-bootstrap

`force-bootstrap` allows to (re-)bootstrap a MySQLService cluster from a specific volume.
The volume is identified by the StatefulSet pod index it belongs to.
This command will refuse to operate if the StatefulSet still has replicas,
because it may do writes to the PVC.

```console
$ yaookctl galera force-bootstrap keystone-fmwlf 2
The MySQL service default/keystone-fmwlf-db will be forced to recover from the PVC data-keystone-fmwlf-db-2.Continue? [y/N] y
```

The command achieves this by modifying the MySQLService StatefulSet in the following ways:

- Increase the number of replicas to index + 1
  (i.e. spawn only the minimum amount of replicas necessary to bootstrap).
- For the one to bootstrap from,
  `MARIADB_GALERA_CLUSTER_BOOTSTRAP=yes` and `MARIADB_GALERA_FORCE_SAFETOBOOTSTRAP=yes` are set.
- For the other instances, startup is delayed by 15s;
  as they are unlikely to succeed to start,
  this delay is needed
  in order to allow the StatefulSet to move on to the next volume.
- Liveness, startup and readiness probes of the mariadb-galera container are removed.
  Otherwise, the pods will never become ready and
  the StatefulSet will never start the target pod.
- The root and mariabackup user passwords are reset using an `init-file`.
  This is especially helpful if you have to recover from a deleted MySQLService instance,
  and is otherwise harmless.

### OpenStack Client shell

Manages a Deployment with an image containing openstackclient, provides the
necessary environment variables to use it and opens a shell.

```console
$ yaookctl openstack shell

root@yaookctl-openstackclient-keystone-6b746f96b4-297j2:/# openstack user list
+----------------------------------+---------------------------------------------------------------+
| ID                               | Name                                                          |
+----------------------------------+---------------------------------------------------------------+
| 53aa0bf2b69441cdacfc4e59e216d898 | yaook-sys-maint                                               |
| bc4c177d33194fa2bbc9f05c31a0d02f | glance-5ngqs.default.cluster.local                            |
| 5ecc046524374f0f900320abd379524f | nova-api-wnntr.default.cluster.local                          |
| 18d1ab64e7e74a8b961d587f81c8d26a | neutron-qbwqp.default.cluster.local                           |
| 72af170e951b4b9b89b42f3f0fbecf0b | placement-api-l486h.default.cluster.local                     |
| 3a00819b62f741c2a3e561933141f197 | neutron-l2-managed-k8s-worker-0-575zk.default.cluster.local   |
| 3849ded53e4a42dab83b7cf9f576c00c | neutron-l2-managed-k8s-worker-2-7fx8s.default.cluster.local   |
| cdcbc95991ed4b3e8134f03650263f40 | neutron-l2-managed-k8s-worker-4-6jmf5.default.cluster.local   |
| d6da5791b4e04a108dec587a2acaff94 | neutron-dhcp-managed-k8s-worker-5-st4rp.default.cluster.local |
| 83d97911678645399b15c6cdbd4b28c7 | neutron-dhcp-managed-k8s-worker-3-nlvjp.default.cluster.local |
| 094c294b19014f27acb798839f76a4c7 | neutron-l2-managed-k8s-worker-3-nd7k4.default.cluster.local   |
| 956d90f1d112434b859403956e263002 | neutron-l2-managed-k8s-worker-5-9n5js.default.cluster.local   |
| 83e496a5fea247569037224cb96ef644 | neutron-l2-managed-k8s-worker-1-9s4hn.default.cluster.local   |
| f15d60f76972451c9ac24538a5a6385e | neutron-dhcp-managed-k8s-worker-1-9tklp.default.cluster.local |
+----------------------------------+---------------------------------------------------------------+
root@yaookctl-openstackclient-keystone-6b746f96b4-297j2:/#
```

### OVSDB Recovery Tools

It is possible that a ovsdb cluster breaks, i.e. when the majority of cluster members are not recoverable due to lost PVCs.
The remaining cluster members are unable to operate because they cannot form a quorum.
To fix that, the following helper command is provided.

**Note:** Before using any this,
you have to scale the StatefulSet down to 0 replicas.
To do so, you'll have to halt the infra operator
or pause the OVSDBService
(see above for `yaookctl pause`).

### disaster-recovery

`disaster-recovery` allows to recover a OVSDB cluster from a specific volume.
The volume is identified by the StatefulSet pod index it belongs to.
The first pod starts with index 0.
This command will refuse to operate if the StatefulSet still has replicas,
because it may create a new OVSDB cluster instead of joining the old cluster.
If more than one node has an intact clustered db file, the pod with the highest index should be used.
This way other cluster members with intact PVCs will join the new cluster as well and not try to connect to the old one.

```console
$ yaookctl ovsdb disaster-recovery neutron-northbound-rcfqz 2
The OVSDB service yaook/neutron-northbound-rcfqz-ovsdb will be forced to recover from the PVC data-neutron-northbound-rcfqz-ovsdb-2.Continue? [y/N] y
```

The command achieves this by modifying the OVSDBService StatefulSet in the following ways:

- Increase the number of replicas to index + 1
  (i.e. spawn only the minimum amount of replicas necessary to bootstrap).
- For the one to bootstrap from,
  `/init-raft.sh disaster-recovery` instead of `/init-raft.sh` is executed in the initContainer.
  The broken clustered DB will be transformed into a standalone DB. With this standalone DB a new clustered DB
  can be created, containing all the data.
- For the other instances the initContainer will be skipped.
  The actual ovsdb-container startup is delayed by 120s and the startup script is executed before starting the ovsdb-server.
  The startup script needs to successfully connect to cluster or else the ovsdb-server won't start properly.
- The probes of the ovsdb-container and the ssl-terminator and the ovsdb-monitoring container are removed or else the pods would not become ready.

## License

[Apache 2](LICENSE)
