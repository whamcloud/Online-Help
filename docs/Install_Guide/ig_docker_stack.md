# How to install IML using Docker stack

[**Software Installation Guide Table of Contents**](ig_TOC.md)

Starting with Integrated Manager for Lustre 5, the IML manager is available via docker using [docker stack](https://docs.docker.com/get-started/part5/). N.B. docker-compose is also supported but is _only intended for development use_.

## Setup

1. Install Docker on your node and init the swarm. The following assumes RHEL 7 as the host OS, but any docker compatible host should work.

   ```sh
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum install -y docker-ce
    systemctl enable --now docker
    docker swarm init --advertise-addr=127.0.0.1 --listen-addr=127.0.0.1
   ```

1. Pull the `docker-compose.yml` from the IML repo. This is used by `docker stack` to bring up IML.

   ```sh
    mkdir -p /etc/iml-docker/
    cd /etc/iml-docker/
    wget https://raw.githubusercontent.com/whamcloud/integrated-manager-for-lustre/master/docker/docker-compose.yml
   ```

1. Create a new file `docker-compose.overrides.yml`, adjacent to docker-compose.yml. It should contain host to ip mappings for each storage server and any other necessary overrides, so the job-scheduler can map them correctly:

   ```yaml
   version: "3.7"
   services:
     job-scheduler:
       extra_hosts:
         - "<STORAGE_SERVER_X_NAME>:<STORAGE_SERVER_X_IP>"
         - "<STORAGE_SERVER_Y_NAME>:<STORAGE_SERVER_Y_IP>"
         - ...
       environment:
         - "NTP_SERVER_HOSTNAME=<NTP_TIMESERVER_ADDRESS>"
   ```

1. Create a [docker secret](https://docs.docker.com/engine/swarm/secrets/) with a new root IML password

   ```sh
    echo <PASSWORD_HERE> | docker secret create iml_pw -
   ```

1. Deploy the stack. This will bring up the manager within docker.

   ```sh
   docker stack deploy -c /etc/iml-docker/docker-compose.yml -c /etc/iml-docker/docker-compose.overrides.yml iml
   ```

1. Add the following executable script to `/usr/bin/iml`. This will allow for `iml` CLI access outside the swarm.

   ```sh
   #! /usr/bin/env bash

   trailer=$(docker service ps -f 'name=iml_iml-manager-cli.1' iml_iml-manager-cli -q --no-trunc | head -n1)

   docker exec -ti iml_iml-manager-cli.1.$trailer iml ${@:1}
   ```

1. Add an entry to each storage server's hostfile that maps the docker OS host IP to nginx

   ```text
   <HOST_IP>	nginx
   ```

1. Login to the GUI via `https:://<HOSTNAME>:7443` or `https:://<HOST_IP>:7443` and proceed to deploy agents to storage servers.

## Stopping

If you wish to stop the IML stack from running, do the following:

1. Stop the stack

   ```sh
    docker stack rm iml
    # make sure all services have stopped
    docker stack ls iml
   ```

1. Optionally stop and disable docker

   ```sh
    # Optionally stop docker
    systemctl stop docker
    # Optionally disable
    systemctl disable docker
   ```

## Starting

If you wish to start the IML stack again, do the following:

1. Optionally enable and start docker:

   ```sh
    systemctl enable --now docker
   ```

1. re-deploy the stack

   ```sh
    docker stack deploy -c /etc/iml-docker/docker-compose.yml -c /etc/iml-docker/docker-compose.overrides.yml iml
   ```
