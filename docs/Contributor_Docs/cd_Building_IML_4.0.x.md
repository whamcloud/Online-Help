# Building IML@4.0.x

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

Make sure you are in the integrated-manager-for-lustre repo and perform the following steps:

1. Create a new centos7 docker container and enter /bin/bash

    ```bash
    docker run -it --name iml-builder -v "$(pwd)":/integrated-manager-for-lustre centos:centos7 bash
    ```

1. Install necessary dependencies

    ```bash
    yum install -y yum-plugin-copr make git epel-release python-setuptools rpm-build ed python-virtualenv systemd-devel graphviz-devel createrepo;

    yum group install -y "Development Tools";

    yum copr enable managerforlustre/manager-for-lustre -y;

    yum copr enable ngompa/dnf-el7 -y;

    yum install -y nodejs npm dnf 'dnf-command(repoquery)' ruby libpqxx-devel;
    ```

1. Run the jenkins build script

    ```bash
    export distro=\${distro:-el7}

    cd integrated-manager-for-lustre/

    scripts/jenkins_build
    ```

This will generate several files in the `dist` and `artifacts` directories. The `artifacts` directory will contain a tar file for both the manager and the agent.

## Installing the rpm

1. Navigate to the Vagrantfiles repo:
    ```bash
    cd hpc-storage-sandbox-el7
    vagrant up adm
    ```

1. Copy the manager artifact from the `integrate-manager-for-lustre/artifacts` directory and paste it into the `hpc-storage-sandbox-el7` directory.
1. Vagrant sync the admin node to ensure it has the artifact in the /vagrant directory.
    ```bash
    vagrant rsync adm
    ```
1. Install the rpm
    ```bash
    vagrant ssh adm
    sudo su -
    cd /vagrant
    cp iml-manager-*.tar /tmp
    cd /tmp
    tar xvf iml-manager-*.tar
    yum install yum-plugin-copr
    yum copr enable managerforlustre/manager-for-lustre
    yum install yum-plugin-copr
    yum copr enable managerforlustre/manager-for-lustre
    yum install chroma-manager-libs-*.rpm
    yum install chroma-manager-cli-*.rpm
    yum install chroma-manager-cli-*.rpm
    chroma-config setup admin lustre localhost --no-dbspace-check
    ```


[Top](#building-iml40x)
