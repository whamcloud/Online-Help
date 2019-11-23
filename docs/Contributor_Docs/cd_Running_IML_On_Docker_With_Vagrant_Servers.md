# Running IML On Docker With Vagrant Servers

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

## Overview

IML is capable of running in a docker swarm (using docker stack) where each manager service is run in its own container. This approach allows IML to be deployed quickly onto the host node. The lustre servers however, need to be somewhere with a full kernel. During development, it is common to deploy IML in a docker swarm and use virtuabox instances as servers. Setting up network communication between the docker swarm and the virtualbox nodes can be a bit tricky. This document describes the process of deploying IML to a docker swarm and how to connect it to virtualbox vm's when adding server nodes.

## Preparing the Network

If not already setup, pull down the [Vagrantfiles Repo](https://github.com/whamcloud/Vagrantfiles):

```sh
git clone git@github.com:whamcloud/Vagrantfiles.git
```

## Adding the host-only network

Once the vm's are up and running a host-only network will need to be configured. The virtualbox vm's have multiple interfaces that serve various purposes (lustre network, manager network, etc). To connect docker to these vm's, it will need to communicate with the management IP of each server node, which happens to be:

- mds1: 10.73.10.11
- mds2: 10.73.10.12
- oss1: 10.73.10.21
- oss2: 10.73.10.22

Even though the vm's are up and running, it's not possible to ssh into any of them without going through 127.0.0.1 using a specific port defined by vagrant (run `vagrant ssh-config` to see these details). Ultimately, this means that docker has no way to connect to the vm's. To solve this problem, a `host-only` adapter will be created to act as a gateway that connects the host to the virtual machines. This allows the host machine to connect to each of the vm's using the manager IP's above. In other words, once the `host-only` adapter is configured, an ssh session can be established by running: `ssh -i ~/repos/Vagrantfiles/iml-sandbox/id_rsa root@10.73.10.x` from the host. To create the host-only adpater, run the following:

```sh
vboxmanage hostonlyif create
vboxmanage hostonlyif ipconfig vboxnet0 --ip 10.73.10.1
```

The host-only adapter is now configured. When the vagrant nodes are brought up and provisioned they will each add the adapter as `vboxnet0` to a network interface.

## Loading Server Nodes

Now that the host-only network is configured, it's time to bring up the iscsi server and server nodes:

```sh
vagrant up iscsi mds1 mds2 oss1 oss2
```

Verify that an ssh connection can be established to each of the server nodes from the host:

```sh
 ssh -i ~/repos/Vagrantfiles/iml-sandbox/id_rsa root@10.73.10.11 "hostname"
 ssh -i ~/repos/Vagrantfiles/iml-sandbox/id_rsa root@10.73.10.12 "hostname"
 ssh -i ~/repos/Vagrantfiles/iml-sandbox/id_rsa root@10.73.10.21 "hostname"
 ssh -i ~/repos/Vagrantfiles/iml-sandbox/id_rsa root@10.73.10.22 "hostname"
```

The server nodes should now be up and running.

## Deploying Docker

There are two ways to deploy IML to docker:

- docker-compose: can be used for development only
- docker stack: can be used for both development and production environments

To setup a docker swarm using docker stack, following the instructions at [How to install IML using Docker stack](../Install_Guide/ig_docker_stack.md). If you prefer to use docker-compose and are running in a development environment, follow the instructions in [Using Docker-Compose](#using-docker-compose).

## Using Docker-Compose

Make sure docker-compose is installed on the host and navigate to the `docker` folder in the `Integrated-Manager-For-Lustre` repo. Follow these steps to bring up all containers:

1. Pull in the latest images:

   ```sh
   docker image ls | grep imlteam | awk '{print $1}' | xargs -I {} docker pull {}
   ```

1. Cleanup any previous networks and volumes. **Warning: This is destructive**

   ```sh
   docker-compose rm -fvs; docker volume prune -f; docker network prune -f
   ```

1. Map IP to server hosts in /etc/hosts on the host

   ```sh
   sudo sed -i '' '/10\.73\.10\.11     mds1\.local/d' /etc/hosts
   sudo sed -i '' '/10\.73\.10\.12     mds2\.local/d' /etc/hosts
   sudo sed -i '' '/10\.73\.10\.21     oss1\.local/d' /etc/hosts
   sudo sed -i '' '/10\.73\.10\.22     oss2\.local/d' /etc/hosts

   sudo -- sh -c "echo '10.73.10.11     mds1.local' >> /etc/hosts"
   sudo -- sh -c "echo '10.73.10.12     mds2.local' >> /etc/hosts"
   sudo -- sh -c "echo '10.73.10.21     oss1.local' >> /etc/hosts"
   sudo -- sh -c "echo '10.73.10.22     oss2.local' >> /etc/hosts"
   ```

1. Bring up the nodes

   ```sh
   docker-compose up
   ```

Wait until all services have loaded and are communicating. IML can now be reached by pointing to `https://127.0.0.1:7443/ui/`. Verify that IML loads properly in the browser.

## Configuring the Server Nodes

Now that IML is deployed, the job-scheduler service will need to be able to communicate with the service nodes. Communication will be done via ssh and thus it will need to have the identity file. Each of the server nodes must also update their /etc/hosts file to point to the nginx domain using the host-only gateway IP. A provisioning script automates this process. Run the following in the iml-sandbox folder.

```sh
vagrant provision mds1 --provision-with configure-docker-network
vagrant provision mds2 --provision-with configure-docker-network
vagrant provision oss1 --provision-with configure-docker-network
vagrant provision oss2 --provision-with configure-docker-network
```

Next, navigate to the `Servers` page and attempt to add the servers using the following pdsh expression: `mds[1,2].local, oss[1,2].local`. The dialog should show all four hosts as having green boxes, indicating that the agent can be deployed.

## Setting up Power Control

Power control will be setup in the `power-control` container similarly to how it is setup in vagrant on the admin node (see [Setting Up Power Control](./cd_Setting_Up_Power_Control.md)). Run the `fake_ipmi_vbox.py` script with the `--skip-validation` flag and use the **Host-Only Network Adapter Address** (See [Adding the host-only network](#adding-the-host-only-network)). Perform the following from `integrated-manager-for-lustre/docker` on the host:

```bash
$ docker-compose run power-control /bin/sh
sh-4.2# cd /usr/share/chroma-manager/
sh-4.2# python scripts/fake_ipmi_vbox.py --skip-validation
Enter the IP Address of your VM Host: 10.73.10.1 # Replace 10.73.10.1 with your Host-Only Network Adapter Address.
    # Enter your computer username
    # Enter your computer password
```

Continue following the instructions in [Setting Up Power Control](./cd_Setting_Up_Power_Control.md).

## Troubleshooting

If IML is not able to communicate with the server vm's, log into the docker container and make sure the server can be pinged:

```sh
{% raw %}
docker ps --format '{{.Names}}' | grep "job-scheduler" | xargs -I {} docker exec {} sh -c 'ping mds1.local'
{% endraw %}
```

If the ping does not respond then there is an issue with the docker network. To resolve this, simply restart the docker daemon. It's also worthwhile to upgrade to the latest docker, virtual box, and vagrant versions.

[Top](#running-iml-on-docker-with-vagrant-servers)
