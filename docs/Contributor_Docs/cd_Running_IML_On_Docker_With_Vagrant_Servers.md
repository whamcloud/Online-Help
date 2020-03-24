# Running IML On Docker With Vagrant Servers

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

## Overview

IML is capable of running in a docker swarm (using docker stack) where each manager service is run in its own container. This approach allows IML to be deployed quickly onto a host. The Lustre servers however, need to be somewhere with a full kernel. During development, it is common to deploy IML in a docker swarm and use virtuabox instances as servers. Setting up network communication between the docker swarm and the virtualbox nodes can be a bit tricky. This document describes the process of deploying IML to a docker swarm and how to connect it to virtualbox vm's when adding server nodes.

## Preparing the Network

If not already setup, pull down the [IML Repo](https://github.com/whamcloud/integrated-manager-for-lustre):

```sh
git clone git@github.com:whamcloud/integrated-manager-for-lustre.git
```

## Adding the host-only network

Once the vm's are up and running a host-only network will need to be configured. The virtualbox vm's have multiple interfaces that serve various purposes (lustre network, manager network, etc). To connect docker to these vm's, it will need to communicate with the management IP of each server node, which happens to be:

- mds1: 10.73.10.11
- mds2: 10.73.10.12
- oss1: 10.73.10.21
- oss2: 10.73.10.22

Even though the vm's are up and running, it's not possible to ssh into any of them without going through 127.0.0.1 using a specific port defined by vagrant (run `vagrant ssh-config` to see these details). Ultimately, this means that docker has no way to connect to the vm's. To solve this problem, a `host-only` adapter will be created to act as a gateway that connects the host to the virtual machines. This allows the host machine to connect to each of the vm's using the manager IP's above. In other words, once the `host-only` adapter is configured, and an ssh config is created, an ssh session can be established by running: `ssh mds1` from the host. To create the host-only adpater, run the following:

```sh
vboxmanage hostonlyif create
vboxmanage hostonlyif ipconfig vboxnet0 --ip 10.73.10.1
```

The host-only adapter is now configured. When the vagrant nodes are brought up and provisioned they will each add the adapter as `vboxnet0` to a network interface.

To create a ssh-config that will allow root access to nodes, do the following:

```sh
ID_FILE_PATH="<PATH_TO_IML_INSTALL>/integrated-manager-for-lustre/vagrant/id_rsa"

cat <<EOF >> ~/.ssh/config
Host mds1
HostName 10.73.10.11
User root
IdentityFile $ID_FILE_PATH

Host mds2
HostName 10.73.10.12
User root
IdentityFile $ID_FILE_PATH

Host oss1
HostName 10.73.10.21
User root
IdentityFile $ID_FILE_PATH

Host oss2
HostName 10.73.10.22
User root
IdentityFile $ID_FILE_PATH

Host c1
HostName 10.73.10.31
User root
IdentityFile $ID_FILE_PATH

Host c2
HostName 10.73.10.32
User root
IdentityFile $ID_FILE_PATH
EOF
```

Substitute `PATH_TO_IML_INSTALL` with the path to your local IML installation.

## Loading Server Nodes

Now that the host-only network is configured, it's time to bring up the iscsi server and server nodes:

```sh
vagrant up iscsi mds1 mds2 oss1 oss2 c1
```

Verify that an ssh connection can be established to each of the server nodes from the host:

```sh
 ssh mds1 "hostname"
 ssh mds2 "hostname"
 ssh oss1 "hostname"
 ssh oss2 "hostname"
 ssh c1 "hostname"
```

The server nodes should now be up and running.

## Deploying Docker

To setup a docker swarm using docker stack, following the instructions at [How to install IML using Docker stack](../Install_Guide/ig_docker_stack.md).

## Overrides file

Place the following contents in `/etc/iml-docker/docker-compose.overrides.yml`. This will allow the docker swarm to communicate with vagrant storage servers:

```yaml
version: "3.7"
services:
  job-scheduler:
    extra_hosts:
      - "mds1.local:10.73.10.11"
      - "mds2.local:10.73.10.12"
      - "oss1.local:10.73.10.21"
      - "oss2.local:10.73.10.22"
      - "c1.local:10.73.10.31"
    environment:
      - "NTP_SERVER_HOSTNAME=10.73.10.1"
```

## Configuring the Server Nodes

Now that IML is deployed, the job-scheduler service will need to be able to communicate with the service nodes. Communication will be done via ssh and thus it will need to have the identity file. Each of the server nodes must also update their /etc/hosts file to point to the nginx domain using the host-only gateway IP. A provisioning script automates this process. Run the following in the iml-sandbox folder.

```sh
vagrant provision mds1 mds2 oss1 oss2 --provision-with configure-docker-network
```

We can now deploy monitored servers with the following command on the host

```sh
iml server add -h mds[1,2].local,oss[1,2].local -p  base_monitored
```

Next create some ldiskfs filesystems with the following provisioner

```sh
vagrant provision --provision-with=install-ldiskfs-no-iml,configure-lustre-network,create-ldiskfs-fs,create-ldiskfs-fs2,mount-ldiskfs-fs,mount-ldiskfs-fs2
```

Finally we can detect a filesystem by running this command on the host

```sh
iml filesystem detect
```

if everything was successful, you should see a list of filesystems with the following command on the host

```sh
iml filesystem list
```

[Top](#running-iml-on-docker-with-vagrant-servers)
