# Building IML 4.0.x

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

This will produce `iml-4.0.x.0.tar.gz` in the `chroma-bundles` directory.

[Top](#building-iml-at-40x)
