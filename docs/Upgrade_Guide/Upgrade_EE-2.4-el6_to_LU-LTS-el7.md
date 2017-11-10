# Upgrading Intel® EE for Lustre\* 2.4.2.7 to Lustre\* 2.10.x LTS and Intel® Manager for Lustre\* 4.0

## Introduction

This document provides a description of how to upgrade an existing Lustre\* server file system installation from Intel® EE for Lustre\* version 2.4.2.7 running on the RHEL/CentOS 6 OS distribution to Lustre\* 2.10 LTS and Intel® Manager for Lustre\* version 4 running on RHEL/CentOS 7.

Included in the process is a method for implementing migration of the server operating system from RHEL / CentOS 6.8 to version 7, which represents the most difficult part of the upgrade process.

CentOS is used for the examples. RHEL users will need to refer to Red Hat for instructions on enabling the High Availability add-on needed to install Pacemaker, Corosync and related support tools.

## Risks

The process of upgrading Intel® EE for Lustre\* to a newer Lustre\* and Intel® Manager for Lustre\* version requires careful consideration and planning. There will always be some disruption to services when major maintenance works are undertaken, although this can be contained and minimized.

The procedure is made more complex by the support policies for upgrades of the underlying operating system. In particular, upgrading from Red Hat Enterprise Linux version 6 to version 7 requires a complete re-installation of the base OS, because in-place upgrades are not available to the majority of RHEL deployments. This policy extends to the derivative OS distributions such as CentOS.

With very few exceptions, Red Hat does not provide a supported method for upgrading systems running RHEL version 6 to version 7 in-place: instead, one must backup the original server configuration, execute a fresh install of the new OS version and then restore the original server's configuration. The risks associated with such a procedure are significant.

Nevertheless, upgrades are possible.

The reference platform used throughout the documentation has been installed and is being managed by Intel® Manager for Lustre\* (IML), but the methods for the Lustre\* server components can be broadly applied to any approximately equivalent Lustre\* server environment running the RHEL or CentOS OS.

## Process Overview

1. Upgrade the Intel® Manager for Lustre\* manager server
    1. Backup the Intel® Manager for Lustre\* server (IML manager) configuration and database
    1. Install RHEL 7 or CentOS 7
    1. Install the latest version of the IML manager software for EL7
    1. Restore the IML manager configuration and database
    1. Start the IML manager services
1. Upgrade the metadata and object storage server pairs. For each HA pair:
    1. Backup the server configuration for both machines
    1. Machines are upgraded one at a time
        1. Failover all resources to a single node, away from the node being upgraded
        1. Set the node to standby mode and disable the node in Pacemaker
        1. Shut down the node to be upgraded. Verify that the Lustre\* services remain online
        1. Install the new OS
        1. Install the new EE software
        1. Restore the server configuration
        1. Create the Pacemaker framework
        1. Stop the resources on the secondary node
        1. Move the Pacemaker resources to the upgraded node
        1. Update the secondary node
        1. Add the secondary node into the Pacemaker configuration
        1. Re-balance the resources

**Note:** The procedure relies heavily on backups of server configuration information. The document will describe how to create a backup manifest for each type of server. It is recommended that this information is backed up periodically as a matter of routine, as it can be used to support disaster recovery scenarios.

**Note:** When restoring OS configuration files to the upgraded OS, make sure to follow the distribution vendor's guidelines for best practice and security, as there may be differences in software configuration between the older and newer OS releases.

## Upgrade Intel® Manager for Lustre\*

The first component in the environment to upgrade is the Intel® Manager for Lustre\* server and software. The manager server upgrade can be conducted without any impact to the Lustre\* file system services.

### Backup the Existing Intel® Manager for Lustre\* Configuration

1. Backup the Existing configuration. Prior to commencing the upgrade, it is essential that a backup of the existing configuration is completed.

    The following shell script can be used to capture the essential configuration information that is relevant to the Intel® Manager for Lustre\* software itself:

    ```bash
    #!/bin/sh
    # EE Intel Manager for Lustre (IML) server backup script

    BCKNAME=bck-$HOSTNAME-`date +%Y%m%d-%H%M%S`
    BCKROOT=$HOME/$BCKNAME
    mkdir -p $BCKROOT
    tar cf - --exclude=/var/lib/chroma/repo \
    /var/lib/chroma \
    /etc/sysconfig/network \
    /etc/sysconfig/network-scripts/ifcfg-* \
    /etc/yum.conf \
    /etc/yum.repos.d \
    /etc/hosts \
    /etc/passwd \
    /etc/group \
    /etc/shadow \
    /etc/gshadow \
    /etc/sudoers \
    /etc/resolv.conf \
    /etc/nsswitch.conf \
    /etc/rsyslog.conf \
    /etc/ntp.conf \
    /etc/selinux/config \
    /etc/ssh \
    /root/.ssh \
    | (cd $BCKROOT && tar xf -)

    # IML Database
    su - postgres -c "/usr/bin/pg_dumpall --clean" | /bin/gzip > $BCKROOT/pgbackup-`date +\%Y-\%m-\%d-\%H:\%M:\%S`.sql.gz

    cd `dirname $BCKROOT`
    tar zcf $BCKROOT.tgz `basename $BCKROOT`
    ```

1. Copy the backup tarball to a safe location that is not on the server being upgraded.

**Note:** This script is not intended to provide a comprehensive backup of the entire operating system configuration. It covers the essential components pertinent to Lustre\* servers managed by Intel® Manager for Lustre\* that are difficult to re-create if deleted.

***Do not skip the backup. Subsequent process steps rely on the content of the backup to restore the Intel® Manager for Lustre\* services to operation.***

### Install the Operating System Update for the Manager Node

1. [Optional] Stop  the `chroma-agent` daemon on each of the registered Lustre\* nodes. This step is optional, but will reduce the number of warnings and errors in the log files during the upgrade process. Stopping the `chroma-agent` will not affect Lustre\* file system services that are running and will not impact failover of Lustre\* file system cluster resources managed by Pacemaker.
1. Shut down the Intel® Manager for Lustre\* manager machine and install the new operating system version.
1. When the installation is complete, copy the configuration backup tarball onto the host and extract it:

    ```bash
    cd $HOME
    tar zxf bck-`hostname`-*.tgz
    ```

1. Restore the network interfaces, using the utilities provided by the OS (e.g. `nmtui edit`). The backup contains the raw configuration files for reference, in ``bck-`hostname`-*/etc/sysconfig/network-scripts``.

1. Restore the hosts database and DNS resolver configuration. For example:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/hosts /etc/.
    cp $HOME/bck-`hostname`-*/etc/resolv.conf /etc/.
    cp $HOME/bck-`hostname`-*/etc/nsswitch.conf /etc/.
    ```

1. Restore the user management configuration (`passwd`, `group`, `shadow`, `gshadow`, `sudoers`). For example:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/passwd /etc/.
    cp $HOME/bck-`hostname`-*/etc/group /etc/.
    cp $HOME/bck-`hostname`-*/etc/shadow /etc/.
    cp $HOME/bck-`hostname`-*/etc/gshadow /etc/.
    cp $HOME/bck-`hostname`-*/etc/sudoers /etc/.
    ```

1. Restore the SSH configuration from the backup. For example:

    ```bash
    mv /root/.ssh /root/.ssh.inst
    cp -a $HOME/bck-`hostname`-*/root/.ssh /root/.ssh/
    mv /etc/ssh /etc/ssh.inst
    cp -a $HOME/bck-`hostname`-*/etc/ssh /etc/ssh
    systemctl restart sshd
    ```

    **Note:** If SELinux is enabled, the permissions for the files in `/etc/ssh` will need to be updated with the correct SELinux label. For example:

    ```bash
    chcon -Rv system_u:object_r:sshd_key_t:s0 /etc/ssh/ssh_host_*
    ```

    Restoring the `/etc/ssh` configuration and root user ssh keys is optional but will make the process of upgrading easier.

1. Restore the NTP configuration. For example:

    ```bash
    # install ntp
    yum -y install ntp
    # Restore the NTP configuration
    mv /etc/ntp.conf /etc/ntp.conf.inst
    cp $HOME/bck-`hostname`-*/etc/ntp.conf /etc/.
    # Start NTP
    ntpd -qg
    systemctl enable ntpd
    systemctl start ntpd
    ```

### Install the Intel® Manager for Lustre\* Upgrade

The software upgrade process requires super-user privileges to run. Login as the `root` user or use `sudo` to elevate privileges as required.

1. Download the latest Intel® Manager for Lustre\* software from the project's release page:

    <https://github.com/intel-hpdd/intel-manager-for-lustre/releases>

1. Extract the Intel® Manager for Lustre\* bundle. For example:

    ```bash
    cd $HOME
    tar zxf iml-4.0.0.0.tar.gz
    ```

1. As root, run the installer:

    ```bash
    cd $HOME/iml-*
    ./install [-h] | [-r] [-p] [-d]
    ```

    **Note:** For an explanation of the installation options, run the install script with the `--help` flag:

    ```bash
    usage: install [-h] [--no-repo-check] [--no-platform-check]
                   [--no-dbspace-check]

    optional arguments:
      -h, --help            show this help message and exit
      --no-repo-check, -r
      --no-platform-check, -p
      --no-dbspace-check, -d
    ```

### Restore the Intel® Manager for Lustre\* Configuration

1. When the initial installation is complete, stop the Intel® Manager for Lustre\* services on the host:

    ```bash
    chroma-config stop
    ```

1. Restore the Intel® Manager for Lustre\* certificates from the backup:

    ```bash
    mkdir /var/lib/chroma/certs-inst
    mv /var/lib/chroma/*.* /var/lib/chroma/certs-inst/
    cp $HOME/bck-`hostname`-*/var/lib/chroma/* /var/lib/chroma/.
    ```

1. Restore the Intel® Manager for Lustre\* database from the backup:

    ```bash
    zcat $HOME/bck-`hostname`-*/pgbackup-*.sql.gz | \
    su - postgres -c "psql postgres"
    ```

1. Run `chroma-config setup` to upgrade the restored database to the latest version. This will reconcile any schema changes that may exist between versions:

    ```bash
    chroma-config setup [-v]
    ```

    On successful completion, the Intel® Manager for Lustre\* software will be started automatically.

1. When the installation and restoration of the configuration is complete, connect to the Intel® Manager for Lustre\* service using a web browser and verify that the new version has been installed and is running.

### Create Local Repositories for the Lustre\* Packages

The Intel® Manager for Lustre\* distribution does not include Lustre\* software packages. These need to be acquired separately from the Lustre\* project's download server. The following instructions will establish the manager node as a YUM repository server for the network. The Intel® Manager for Lustre\* server is automatically configured as a web server, so it is a convenient location for the repository mirrors.

An alternative strategy is to copy the repository definition from step 1 directly onto each Lustre\* server and client (saving the file in `/etc/yum.repos.d` on each node), and skip the other steps that follow. This avoids creating a local repository on the manager node, and uses the Lustre\* download servers directly to download packages.

Also note that the manager server distribution includes a default repository definition in `/usr/share/chroma-manager/storage_server.repo`. This can be copied onto each Lustre\* server and client into `/etc/yum.repos.d` instead of using these instructions. The choice of method for distributing Lustre\* onto the target nodes is a matter of preference and suitability for the target environment.

1. Create a temporary YUM repository definition. This will be used to assist with the initial acquisition of the Lustre\* and related packages.

    ```bash
    cat >/tmp/lustre-repo.conf <<\__EOF
    [lustre-server]
    name=lustre-server
    baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7/server
    exclude=*debuginfo*
    gpgcheck=0

    [lustre-client]
    name=lustre-client
    baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7/client
    exclude=*debuginfo*
    gpgcheck=0

    [e2fsprogs-wc]
    name=e2fsprogs-wc
    baseurl=https://downloads.hpdd.intel.com/public/e2fsprogs/latest/el7
    exclude=*debuginfo*
    gpgcheck=0
    __EOF
    ```

    **Note:** The above example references the latest Lustre\* release available. To use a specific version, replace `latest-release` in the `[lustre-server]` and `[lustre-client]` `baseurl` variables with the version required, e.g., `lustre-2.10.1`. Always use the latest `e2fsprogs` package unless directed otherwise.

    **Note:** With the release of Lustre\* version 2.10.1, it is possible to use patchless kernels for Lustre\* servers running LDISKFS. The patchless LDISKFS server distribution does not include a Linux kernel. Instead, patchless servers will use the kernel distributed with the operating system. To use patchless kernels for the Lustre\* servers, replace the string `server` with `patchless-ldiskfs-server` at the end of the `[lustre-server]` `baseurl` string. For example:

    ```bash
    baseurl=https://downloads.hpdd.intel.com/public/lustre/latest-release/el7/patchless-ldiskfs-server
    ```

    Also note that the `debuginfo` packages are excluded in the example repository definitions. This is simply to cut down on the size of the download. It is usually a good idea to pull in these files as well, to assist with debugging of issues.

1. Use the `reposync` command (distributed in the `yum-utils` package) to download mirrors of the Lustre\* repositories to the manager server:

    ```bash
    cd /var/lib/chroma/repo
    reposync -c /tmp/lustre-repo.conf -n \
    -r lustre-server \
    -r lustre-client \
    -r e2fsprogs-wc
    ```

1. Create the repository metadata:

    ```bash
    cd /var/lib/chroma/repo
    for i in e2fsprogs-wc lustre-client lustre-server; do
    (cd $i && createrepo .)
    done
    ```

1. Create a YUM Repository Definition File

    The following script creates a file containing repository definitions for the Intel® Manager for Lustre\* Agent software and the Lustre\* packages downloaded in the previous section. Review the content and adjust according to the requirements of the target environment. Run the script on the upgraded Intel® Manager for Lustre\* host:

    ```bash
    hn=`hostname --fqdn`
    cat >/var/lib/chroma/repo/Manager-for-Lustre.repo <<__EOF
    [iml-agent]
    name=Intel Manager for Lustre Agent
    baseurl=https://$hn/repo/iml-agent/7
    enabled=1
    gpgcheck=0
    sslverify = 1
    sslcacert = /var/lib/chroma/authority.crt
    sslclientkey = /var/lib/chroma/private.pem
    sslclientcert = /var/lib/chroma/self.crt
    proxy=_none_

    [lustre-server]
    name=lustre-server
    baseurl=https://$hn/repo/lustre-server
    enabled=1
    gpgcheck=0
    sslverify = 1
    sslcacert = /var/lib/chroma/authority.crt
    sslclientkey = /var/lib/chroma/private.pem
    sslclientcert = /var/lib/chroma/self.crt
    proxy=_none_

    [lustre-client]
    name=lustre-client
    baseurl=https://$hn/repo/lustre-client
    enabled=1
    gpgcheck=0
    sslverify = 1
    sslcacert = /var/lib/chroma/authority.crt
    sslclientkey = /var/lib/chroma/private.pem
    sslclientcert = /var/lib/chroma/self.crt
    proxy=_none_

    [e2fsprogs-wc]
    name=e2fsprogs-wc
    baseurl=https://$hn/repo/e2fsprogs-wc
    enabled=1
    gpgcheck=0
    sslverify = 1
    sslcacert = /var/lib/chroma/authority.crt
    sslclientkey = /var/lib/chroma/private.pem
    sslclientcert = /var/lib/chroma/self.crt
    proxy=_none_
    __EOF
    ```

    This file needs to be distributed to each of the Lustre\* servers during the upgrade process to facilitate installation of the software.

    Make sure that the `$hn` variable matches the host name that will be used by the Lustre\* servers to access the Intel® Manager for Lustre\* host.

## Upgrade the Lustre\* Servers

Lustre\* server upgrades can be coordinated as either an online roll-out, leveraging the failover HA mechanism to migrate services between nodes and minimize disruption, or as an offline service outage, which has the advantage of usually being faster to deploy overall, with generally lower risk.

The upgrade procedure documented here shows how to execute the upgrade while the file system is online. It assumes that the Lustre\* servers have been installed in pairs, where each server pair forms an independent high-availability cluster built on Pacemaker and Corosync. Intel® Manager for Lustre\* deploys these configurations and includes its own resource agent for managing Lustre\* assets, called `ocf:chroma:Target`. Intel® Manager for Lustre\* can also configure STONITH agents to provide node fencing in the event of a cluster partition or loss of quorum.

The cluster configuration deployed by Intel® Manager for Lustre\* is straightforward and easy to reproduce from backups, and is further simplified by the `pcs` cluster management application that ships with RHEL and CentOS.

This documentation will demonstrate how to upgrade a single Lustre\* server HA pair. The process needs to be repeated for all servers in the cluster. It is possible to execute this upgrade while services are still online, with only minor disruption during critical phases. Nevertheless, where possible it is recommended that the upgrade operation is conducted during a planned maintenance window with the file system stopped.

In the procedure, "Node 1" or "first node" will be used to refer to the first server in each HA cluster to upgrade, and "Node 2" or "second node" will be used to refer to the second server in each HA cluster pair.

The software upgrade process requires super-user privileges to run. Login as the `root` user or use `sudo` to elevate privileges as required to complete tasks.

**Note:** It is recommended that Lustre\* clients are quiesced prior to executing the upgrade. This reduces the risk of disruption to the upgrade process itself. It is not usually necessary to unmount the Lustre\* clients, although this is a sensible precaution.

### Prepare for the Upgrade

Upgrade one server at a time in each cluster pair, starting with Node 1, and make sure the upgrade is complete on one server before moving on to the second server in the pair.

1. As a precaution, create a backup of the existing configuration for each server. The following shell script can be used to capture the essential configuration information that is relevant to Intel® Manager for Lustre\* managed mode servers:

    ```bash
    #!/bin/sh
    BCKNAME=bck-$HOSTNAME-`date +%Y%m%d-%H%M%S` BCKROOT=$HOME/$BCKNAME
    mkdir -p $BCKROOT
    tar cf - \
    /var/lib/chroma \
    /etc/sysconfig/network \
    /etc/sysconfig/network-scripts/ifcfg-* \
    /etc/yum.conf \
    /etc/yum.repos.d \
    /etc/hosts \
    /etc/passwd \
    /etc/group \
    /etc/shadow \
    /etc/gshadow \
    /etc/sudoers \
    /etc/resolv.conf \
    /etc/nsswitch.conf \
    /etc/rsyslog.conf \
    /etc/ntp.conf \
    /etc/selinux/config \
    /etc/modprobe.d/iml_lnet_module_parameters.conf \
    /etc/corosync/corosync.conf \
    /etc/ssh \
    /root/.ssh \
    | (cd $BCKROOT && tar xf -)

    # Pacemaker Configuration:
    cibadmin --query > $BCKROOT/cluster-cfg-$HOSTNAME.xml

    cd `dirname $BCKROOT`
    tar zcf $BCKROOT.tgz `basename $BCKROOT`
    ```

    **Note:** This is not intended to be a comprehensive backup of the entire operating system configuration. It covers the essential components pertinent to Lustre\* servers managed by Intel® Manager for Lustre\* that are difficult to re-create if deleted.

    ***Do not skip the backup. Subsequent process steps rely on the content of the backup to restore the Lustre\* services to operation.***

1. Copy the backups for each server's configuration to a safe location that is not on the servers being upgraded.

**Note:** The `pcs` command provides a way to create a set of commands intended to help recreate a cluster, as an alternative form of configuration backup. It is invoked as follows:

```bash
pcs config export pcs-commands | pcs-commands-verbose
```

However, it is ***not*** a suitable replacement for a backup of the running configuration, and there are several issues with the resulting output. In particular:

* The generated commands assume that all of the nodes in the pacemaker cluster have been reinitialized and are being upgraded simultaneously. This means that servers cannot be upgraded one at a time, and will require a full outage of the nodes in the HA cluster.
* If moving from an older OS version to a newer one, some of the naming conventions have changed and will not be captured in the command list. Specifically, the node names in the "backup" may not have fully qualified domain names. It is recommended that clusters use fully qualified domain names, so this has to be factored into the restore process and edits made to the output.
* The command does not correctly export node attributes.
* The command output uses colour formatting when available, even when the output is directed to a file. This can lead to files that contain spurious escape sequences, causing syntax errors.

The `pcs config export` command can be useful as a cross reference when restoring the desired configuration, but it is not used in the procedures documented here because of the issues indicated above.

### Migrate the Resources on Node 1

1. Login to node 1 and failover all resources to the standby node. The easiest way to do this is to set the server to standby mode:

    ```bash
    pcs cluster standby [<node name>]
    ```

    **Note:** if the node name is omitted from the command, only the node currently logged into will be affected.

1. Verify that the resources have moved to the second node and that the resources are running (all storage targets are mounted on the second node only):

    ```bash
    # On node 2:
    pcs resource show
    df -ht lustre
    ```

1. [Optional] Disable the node that is being upgraded:

    ```bash
    pcs cluster disable [<node name>]
    ```

    **Note:** This command prevents the Corosync and Pacemaker services from starting automatically on system boot. The command is optional, because the node is going to be rebuilt, but it is a simple and useful way to ensure that if the server is accidentally rebooted into the old OS, it won't try to join the cluster and disrupt services running on the secondary node. If the node name is omitted from the command, only the node currently logged into will be affected.

### Upgrade Node 1

#### Install the New Operating System Version on Node 1

1. Shut down the first server, node 1
1. Following the vendor's instructions, install the new OS version on node 1

#### Restore the Node 1 OS Configuration from Backup

1. When the initial OS installation is complete, login to node 1.
1. Copy the backup tarball onto the new installation on node 1 and extract it:

    ```bash
    cd $HOME
    tar zxf bck-`hostname`-*.tgz
    ```

1. Restore the network interfaces, using the utilities provided by the OS (e.g. `nmtui-edit`). The backup contains the raw configuration files for reference, in ``bck-`hostname`-*/etc/sysconfig/network-scripts``. Do not forget to restore the network configuration of the direct network connection between the server nodes (used as `ring1` for Corosync communications).
1. Restore the hosts database and DNS resolver configuration. For example:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/hosts /etc/.
    cp $HOME/bck-`hostname`-*/etc/resolv.conf /etc/.
    cp $HOME/bck-`hostname`-*/etc/nsswitch.conf /etc/.
    ```

1. Restore the user management configuration (`passwd`, `group`, `shadow`, `gshadow`, `sudoers`). For example:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/passwd /etc/.
    cp $HOME/bck-`hostname`-*/etc/group /etc/.
    cp $HOME/bck-`hostname`-*/etc/shadow /etc/.
    cp $HOME/bck-`hostname`-*/etc/gshadow /etc/.
    cp $HOME/bck-`hostname`-*/etc/sudoers /etc/.
    ```

1. Restore the SSH configuration from the backup:

    ```bash
    mv /root/.ssh /root/.ssh.inst
    cp -a $HOME/bck-`hostname`-*/root/.ssh /root/.ssh/
    mv /etc/ssh /etc/ssh.inst
    cp -a $HOME/bck-`hostname`-*/etc/ssh /etc/ssh
    ```

    **Note:** If SELinux is enabled, the permissions for the files in `/etc/ssh` will need to be updated with the correct SELinux label. For example:

    ```bash
    chcon -Rv system_u:object_r:sshd_key_t:s0 /etc/ssh/ssh_host_*
    ```

    Restoring the `/etc/ssh` configuration and root user ssh keys is optional but will make the process of upgrading easier.

1. Restore the NTP configuration. For example:

    ```bash
    # install ntp
    yum -y install ntp
    # Restore the NTP configuration
    mv /etc/ntp.conf /etc/ntp.conf.inst
    cp $HOME/bck-`hostname`-*/etc/ntp.conf /etc/.
    # Start NTP
    ntpd -qg
    systemctl enable ntpd
    systemctl start ntpd
    ```

1. Restore the LNet configuration (file name may vary, depending on how LNet was configured and any customization that may have been carried out). The following example assumes that the server has a configuration that was created by Intel® Manager for Lustre\*:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/modprobe.d/iml_lnet_module_parameters.conf /etc/modprobe.d/.
    ```

#### Install the EPEL Repository Definition on Node 1

1. Login to node 1.
1. Install EPEL repository support:

    ```bash
    yum -y install epel-release
    ```

#### Install the Intel® Manager for Lustre\* Agent on Node 1

1. Login to node 1.
1. Install the Intel® Manager for Lustre\* COPR Repository definition, which contains some dependencies for the Intel® Manager for Lustre\* Agent:

    ```bash
    yum-config-manager --add-repo \
    https://copr.fedorainfracloud.org/coprs/managerforlustre/manager-for-lustre/repo/epel-7/managerforlustre-manager-for-lustre-epel-7.repo
    ```

1. Install the DNF project COPR Repository definition. DNF is a package manager, and is used as a replacement for YUM in many distributions, such as Fedora. It does not replace YUM in CentOS, but Intel® Manager for Lustre\* does make use of some of the newer features in DNF for some of its tasks:

    ```bash
    yum-config-manager --add-repo \
    https://copr.fedorainfracloud.org/coprs/ngompa/dnf-el7/repo/epel-7/ngompa-dnf-el7-epel-7.repo
    ```

1. Restore the Intel® Manager for Lustre\* Agent configuration and certificates to the node:

    ```bash
    cp -a $HOME/bck-`hostname`-*/var/lib/chroma /var/lib/.
    ```

1. Install the Intel® Manager for Lustre\* Agent repository definition:

    ```bash
    curl -o /etc/yum.repos.d/Manager-for-Lustre.repo \
    --cacert /var/lib/chroma/authority.crt \
    --cert /var/lib/chroma/self.crt \
    --key /var/lib/chroma/private.pem \
    https://<admin server>/repo/Manager-for-Lustre.repo
    ```

    Replace `<admin server>` in the `https` URL with the appropriate Intel® Manager for Lustre\* hostname (normally the fully-qualified domain name).

1. Install The Intel® Manager for Lustre\* Agent and Diagnostics packages

    ```bash
    yum -y install chroma-\*
    ```

    **Note:** following warning during install / update is benign and can be ignored:

    ```bash
    ...
      /var/tmp/rpm-tmp.MV5LGi: line 5: /selinux/enforce: No such file or directory
      []

      {
        "result": null,
        "success": true
      }
    ...
    ```

#### Install the Lustre\* Server Software on Node 1

1. For systems that have **both** LDISKFS and ZFS OSDs:

    **Note:** This is the configuration that Intel® Manager for Lustre\* installs for all managed-mode Lustre\* storage clusters. Use this configuration for the highest level of compatibility with Intel® Manager for Lustre\*.

    1. Install the Lustre\* `e2fsprogs` distribution:

        ```bash
        yum --nogpgcheck --disablerepo=* --enablerepo=e2fsprogs-wc \
        install e2fsprogs e2fsprogs-devel
        ```

    1. If the installed `kernel-tools` and  `kernel-tools-libs` packages are at a higher revision than the patched kernel packages in the Lustre\* server repository, they will need to be removed:

        ```bash
        yum erase kernel-tools kernel-tools-libs
        ```

    1. Install the Lustre-patched kernel packages. Ensure that the Lustre\* repository is picked for the kernel packages, by disabling the OS repos:

        ```bash
        yum --nogpgcheck --disablerepo=base,extras,updates \
        install \
        kernel \
        kernel-devel \
        kernel-headers \
        kernel-tools \
        kernel-tools-libs \
        kernel-tools-libs-devel
        ```

    1. Install additional development packages. These are needed to enable support for some of the newer features in Lustre\* – if certain packages are not detected by Lustre's\* configure script when its DKMS package is installed, the features will not be enabled when Lustre\* is compiled. Notable in this list are `krb5-devel` and `libselinux-devel`, needed for Kerberos and SELinux support, respectively.

        ```bash
        yum install \
        asciidoc audit-libs-devel automake bc \
        binutils-devel bison device-mapper-devel elfutils-devel \
        elfutils-libelf-devel expect flex gcc gcc-c++ git \
        glib2 glib2-devel hmaccalc keyutils-libs-devel krb5-devel ksh \
        libattr-devel libblkid-devel libselinux-devel libtool \
        libuuid-devel libyaml-devel lsscsi make ncurses-devel \
        net-snmp-devel net-tools newt-devel numactl-devel \
        parted patchutils pciutils-devel perl-ExtUtils-Embed \
        pesign python-devel redhat-rpm-config rpm-build systemd-devel \
        tcl tcl-devel tk tk-devel wget xmlto yum-utils zlib-devel
        ```

    1. Ensure that a persistent hostid has been generated on the machine. If necessary, generate a persistent hostid (needed to help protect zpools against simultaneous imports on multiple servers). For example:

        ```bash
        hid=`[ -f /etc/hostid ] && od -An -tx /etc/hostid|sed 's/ //g'`
        [ "$hid" = `hostid` ] || genhostid
        ```

    1. Reboot the node.

        ```bash
        reboot
        ```

    1. Install Lustre\*, and the LDISKFS and ZFS `kmod` packages:

        ```bash
        yum --nogpgcheck install \
        kmod-lustre-osd-ldiskfs \
        lustre-dkms \
        lustre-osd-ldiskfs-mount \
        lustre-osd-zfs-mount \
        lustre \
        lustre-resource-agents \
        zfs
        ```

    1. Verify that the DKMS kernel modules for Lustre\*, SPL and ZFS have installed correctly:

        ```bash
        dkms status
        ```

        All packages should have the status `installed`. For example:

        ```bash
        # dkms status
        lustre, 2.10.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        spl, 0.7.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        zfs, 0.7.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        ```

    1. Load the Lustre\* kernel modules to verify that the software has installed correctly:

        ```bash
        modprobe -v zfs
        modprobe -v lustre
        ```

1. For systems that use LDISKFS OSDs:
    1. Install the Lustre\* `e2fsprogs` distribution:

        ```bash
        yum --nogpgcheck \
        --disablerepo=* --enablerepo=e2fsprogs-wc install e2fsprogs
        ```

    1. Install the Lustre-patched kernel packages. Ensure that the Lustre\* repository is picked for the kernel packages, by disabling the OS repos:

        ```bash
        yum --nogpgcheck --disablerepo=base,extras,updates \
        install \
        kernel \
        kernel-devel \
        kernel-headers \
        kernel-tools \
        kernel-tools-libs \
        kernel-tools-libs-devel
        ```

    1. Reboot the node.

        ```bash
        reboot
        ```

    1. Install the LDISKFS `kmod` and other Lustre\* packages:

        ```bash
        yum --nogpgcheck install \
        kmod-lustre \
        kmod-lustre-osd-ldiskfs \
        lustre-osd-ldiskfs-mount \
        lustre \
        lustre-resource-agents
        ```

    1. Load the Lustre\* kernel modules to verify that the software has installed correctly:

        ```bash
        modprobe -v lustre
        ```

1. For systems with only ZFS-based OSDs:
    1. Install the kernel packages that match the latest supported version for the Lustre\* release:

        ```bash
        yum install \
        kernel \
        kernel-devel \
        kernel-headers \
        kernel-tools \
        kernel-tools-libs \
        kernel-tools-libs-devel
        ```

        It may be necessary to specify the kernel package version number in order to ensure that a kernel that is compatible with Lustre\* is installed. For example, Lustre\* 2.10.1 has support for RHEL kernel 3.10.0-693.2.2.el7:

        ```bash
        yum install \
        kernel-3.10.0-693.2.2.el7 \
        kernel-devel-3.10.0-693.2.2.el7 \
        kernel-headers-3.10.0-693.2.2.el7 \
        kernel-tools-3.10.0-693.2.2.el7 \
        kernel-tools-libs-3.10.0-693.2.2.el7 \
        kernel-tools-libs-devel-3.10.0-693.2.2.el7
        ```

        **Note:** If the `kernel-tools` and  `kernel-tools-libs` packages that have been installed on the host prior to running this command are at a higher revision than the kernel version supported by Lustre\*, they will need to be removed first:

        ```bash
        yum erase kernel-tools kernel-tools-libs
        ```

        Refer to the [Lustre\* Changelog](http://wiki.lustre.org/Category:Changelog) for the list of supported kernels.

    1. Install additional development packages. These are needed to enable support for some of the newer features in Lustre\* – if certain packages are not detected by Lustre's\* configure script when its DKMS package is installed, the features will not be enabled when Lustre\* is compiled. Notable in this list are `krb5-devel` and `libselinux-devel`, needed for Kerberos and SELinux support, respectively.

        ```bash
        yum install \
        asciidoc audit-libs-devel automake bc \
        binutils-devel bison device-mapper-devel elfutils-devel \
        elfutils-libelf-devel expect flex gcc gcc-c++ git \
        glib2 glib2-devel hmaccalc keyutils-libs-devel krb5-devel ksh \
        libattr-devel libblkid-devel libselinux-devel libtool \
        libuuid-devel libyaml-devel lsscsi make ncurses-devel \
        net-snmp-devel net-tools newt-devel numactl-devel \
        parted patchutils pciutils-devel perl-ExtUtils-Embed \
        pesign python-devel redhat-rpm-config rpm-build systemd-devel \
        tcl tcl-devel tk tk-devel wget xmlto yum-utils zlib-devel
        ```

    1. Ensure that a persistent hostid has been generated on the machine. If necessary, generate a persistent hostid (needed to help protect zpools against simultaneous imports on multiple servers). For example:

        ```bash
        hid=`[ -f /etc/hostid ] && od -An -tx /etc/hostid|sed 's/ //g'`
        [ "$hid" = `hostid` ] || genhostid
        ```

    1. Reboot the node.

        ```bash
        reboot
        ```

    1. Install the packages for Lustre\* and ZFS:

        ```bash
        yum --nogpgcheck install \
        lustre-dkms \
        lustre-osd-zfs-mount \
        lustre \
        lustre-resource-agents \
        zfs
        ```

    1. Load the Lustre\* and ZFS kernel modules to verify that the software has installed correctly:

        ```bash
        modprobe -v zfs
        modprobe -v lustre
        ```

#### Configure the High Availability Framework on Node 1

1. Install the OS cluster software:

    ```bash
    yum -y install pcs pacemaker corosync fence-agents
    ```

1. Ensure `hacluster` user is present on the server. For example:

    ```bash
    [root@ct6-mds1 ~]# id hacluster
    uid=189(hacluster) gid=189(haclient) groups=189(haclient)
    ```

    If required, add the `hacluster` user – usually the user is created when the cluster software is installed.

1. Set the password for the `hacluster` user:

    ```bash
    passwd hacluster
    ```

1. Modify or disable the firewall. According to Red Hat, the following ports need to be enabled:
    1. TCP: ports 2224, 3121, 21064
    1. UDP: ports 5405
1. In RHEL / CentOS 7, the firewall software can be configured to permit cluster traffic as follows:

    ```bash
    firewall-cmd --permanent --add-service=high-availability
    firewall-cmd --add-service=high-availability
    ```

    **Note:** both commands are required. The first command writes a persistent record of the firewall rules without changing the running configuration, while the second command changes the running configuration.

1. Verify the firewall configuration as follows:

    ```bash
    firewall-cmd --list-service
    ```

1. Alternatively, disable the firewall completely:

    ```bash
    systemctl stop firewalld
    systemctl disable firewalld
    ```

1. Start the Pacemaker configuration daemon, `pcsd`, and enable it to start on system boot:

    ```bash
    systemctl start pcsd.service
    systemctl enable pcsd.service
    ```

1. Verify that the `pcsd` service is running:

    ```bash
    systemctl status pcsd.service
    ```

1. Set up PCS authentication by executing the following command on node 1:

    ```bash
    pcs cluster auth <node1 fqdn> -u hacluster
    ```

    For example:

    ```bash
    [root@ct6-mds1 ~]# pcs cluster auth ct6-mds1.lfs.intl -u hacluster
    Password:
    ct6-mds1.lfs.intl: Authorized
    ```

    **Note:** Only node 1 is added at this time, since node 2 has not yet been upgraded.

    **Note:** When working with host names in Pacemaker and Corosync, use the fully qualified domain names for the nodes.

1. From node 1, recreate the cluster framework:

    ```bash
    pcs cluster setup --name lustre-ha-cluster <node1 fqdn> \
    --transport udp \
    --rrpmode passive \
    --addr0 <net0-bindnetaddr> \
    --mcast0 <net0-mcastaddr> \
    --mcastport0 <net0-mcastport> \
    --addr1 <net1-bindnetaddr> \
    --mcast1 <net1-mcastaddr> \
    --mcastport1 <net1-mcastport> \
    --token 17000
    ```

    The network information is taken from the backup of the `corosync.conf` file. If the backup Corosync configuration is available, the following script can parse the content and print out a command line for recreating the cluster:

    ```bash
    awk -v nm=`hostname --fqdn` \
    'BEGIN{i=0; printf("pcs cluster setup --name lustre-ha-cluster %s \\\n",nm)}
    /interface/{i=1;next}
    i==1 && /\}/{i=0;
    printf ("--addr%s %s \\\n",rn,bn);
    printf ("--mcast%s %s \\\n",rn,mca);
    printf("--mcastport%s %s \\\n",rn,mcp);
    }
    i==1{
    if ($1 ~ "ringnumber"){rn=$2;next}
    if ($1 ~ "bindnetaddr"){bn=$2;next}
    if ($1 ~ "mcastaddr"){mca=$2;next}
    if ($1 ~ "mcastport"){mcp=$2;next}
    }
    END{printf("--transport udp \\\n--rrpmode passive \\\n--token 17000 \\\n--fail_recv_const 10\n")}' \
    $HOME/bck-`hostname`-*/etc/corosync/corosync.conf
    ```

    **Note:** the script assumes that the input `corosync.conf` file conforms to the Corosync configuration file syntax.

1. Start the cluster on the new node:

    ```bash
    pcs cluster start
    ```

    **Note:** The cluster framework will usually take a few seconds to initialize. Progress can be monitored in the syslog or by occasionally reviewing the output of the `pcs status` command.

1. Set the cluster-wide properties:

    ```bash
    ### No Quorum policy (what to do when there is no quorum)
    ###    For 2 node cluster:
    ###        no_quorum_policy = "ignore"
    ###    For > 2 node cluster:
    ###        no_quorum_policy = "stop"
    pcs property set no-quorum-policy=ignore

    ### stonith-enabled
    ### values: true (default) or false
    pcs property set stonith-enabled=true

    ### Symmetric cluster
    ### values: true (default) or false
    ### Should nearly always be set true: indicates that all
    ### nodes have equivalent configs and are equally capable of running
    ### the resources
    pcs property set symmetric-cluster=true
    ```

1. Set the cluster-wide resource defaults (taken from the pacemaker CIB XML):

    ```bash
    # How much does the resource prefer to stay where it is?
    # Higher the value, the more sticky the resource and the less likely it
    # is to migrate automatically to its most preferred location if it is
    # running in a non-preferred / non-default location and the resource is
    # healthy. Affects the behaviour of "auto-failback".
    #
    # If a resource is running on a non-preferred node, and it is healthy, it
    # will not be migrated automatically back to its preferred node.
    #
    # If the stickiness is higher than the preference score of a resource,
    # the resource will not move automatically while the machine it is
    # rurnning on remains healthy.
    pcs resource defaults resource-stickiness=1000

    # The window of time in which we count resource monitor failures
    pcs resource defaults failure-timeout=20m

    # The number of times in the above window that a resource monitor can
    # fail before the resource is migrated to another node
    pcs resource defaults migration-threshold=3
    ```

1. Set the cluster to maintenance-mode:

    ```bash
    pcs property set maintenance-mode=true
    ```

1. Add the basic Intel® Manager for Lustre\* STONITH fencing configuration for the `fence_chroma` resource (this is the same for all Intel® Manager for Lustre\* managed resources, irrespective of the underlying fencing mechanism):

    ```bash
    pcs stonith create st-fencing fence_chroma
    ```

1. Add the resources for each Lustre\* storage target. This requires the original resource name and target identifier assigned by Intel® Manager for Lustre\*. Both can be retrieved from the backup copy of the Pacemaker CIB XML file. The syntax of the command to create a resource is as follows:

    ```bash
    pcs resource create <resource name> ocf:chroma:Target \
    target=<target id> \
    op monitor interval=5 timeout=60 \
    stop interval=0 timeout=300 \
    start interval=0 timeout=300 \
    --disabled
    ```

    **Note:** the `--disabled` flag is absolutely essential at this phase in the rebuild process. It ensures that the resource is not started by the cluster framework, preventing a conflict with the other node that has not been upgraded yet.

    It is possible to extract the cluster resource information from the XML using the `pcs` command, and from that recreate the command line for creating resources. Use the following script as a guide:

    ```bash
    # To extract and view the configuration of the resources from the XML:
    pcs -f $HOME/bck-`hostname`-*/cluster-cfg-`hostname`.xml resource show --full

    # Use the output to generate a command line to recreate the resources:
    pcs -f $HOME/bck-`hostname`-*/cluster-cfg-`hostname`.xml resource show --full | awk \
    '$1~/Resource:/{rn=$2;split($3,c,"[(=)]");split($4,p,"[(=)]");split($5,t,"[(=)]");} \
    $1 ~ /Attributes:/ && rn != "" \
    {printf "pcs resource create %s %s:%s:%s \\\n%s \\\nop monitor interval=5 timeout=60 \\\nstop interval=0 timeout=300 \\\nstart interval=0 timeout=300 \\\n--disabled\n\n", rn, c[3],p[2],t[2],$2; rn=""}'
    ```

    The above script has hard-coded timeouts, which are taken from Intel® Manager for Lustre\*'s default settings. Adjust the values according to need, if the defaults are unsuitable.

    Copy and paste the output of the script into the command line to execute.

    The following is a complete example, demonstrating how to re-create an MGS resource:

    ```bash
    pcs resource create MGS_7706ac ocf:chroma:Target \
    target=9aaf3d9d-df51-48d5-9da1-49d57dee12c0 \
    op monitor interval=5 timeout=60 \
    stop interval=0 timeout=300 \
    start interval=0 timeout=300 \
    --disabled
    ```

    The next example re-creates a resource for a file system MDT:

    ```bash
    pcs resource create demo-MDT0000_af7220 ocf:chroma:Target \
    target=ea0ec37d-288e-48e2-8f11-922980e5cf37 \
    op monitor interval=5 timeout=60 \
    stop interval=0 timeout=300 \
    start interval=0 timeout=300 \
    --disabled
    ```

1. Set the location constraints for each resource:

    ```bash
    pcs constraint location <resource> prefers <primary node name>=20
    pcs constraint location <resource> prefers <secondary node name>=10
    ```

    The information for each constraint is acquired from the CIB XML backup as follows:

    ```bash
    pcs -f $HOME/bck-`hostname`-*/cluster-cfg-`hostname`.xml constraint show
    ```

    Remember that when setting the constraints (or any other parameters related to the cluster nodes), use the fully qualified domain name of each node.

    For example:

    ```bash
    # Constraints for an MGS resource called MGS_32834e:
    pcs constraint location MGS_32834e prefers ct6-mds1.lfs.intl=20
    pcs constraint location MGS_32834e prefers ct6-mds2.lfs.intl=10

    # Constraints for an MDT resource called demo-MDT0000_802c1b:
    pcs constraint location demo-MDT0000_802c1b prefers ct6-mds2.lfs.intl=20
    pcs constraint location demo-MDT0000_802c1b prefers ct6-mds1.lfs.intl=10
    ```

1. Create the mount points for the storage targets. If not, the resource agent, `ocf:chroma:Target` will fail. The expected mount points can be derived from the target configuration files in `/var/lib/chroma/targets/*`, or the backup copes of these files using the following script:

    ```bash
    for i in /var/lib/chroma/targets/*;do
    cat $i | python -m json.tool
    done
    ```

    For example:

    ```bash
    # Output has been cleaned up slightly, as the files do not contain newlines.
    for i in /var/lib/chroma/targets/*;do
    cat $i | python -m json.tool
    done
    {
        "backfstype": "ext4",
        "bdev": "/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_EEMGT0000",
        "device_type": "linux",
        "mntpt": "/mnt/MGS",
        "target_name": "MGS"
    }
    {
        "backfstype": "ext4",
        "bdev": "/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_EEMDT0000",
        "device_type": "linux",
        "mntpt": "/mnt/demo-MDT0000",
        "target_name": "demo-MDT0000"
    }
    ```

    The following is a simple script to create the mount points from the JSON data:

    ```bash
    for i in /var/lib/chroma/targets/*;do
    cat $i | python -c 'import sys, json; print json.load(sys.stdin)["mntpt"]' | xargs mkdir -p
    done
    ```

### Start the Agent Service and Load the Kernel Modules on Node 1

1. Start the `chroma-agent` service:

    ```bash
    systemctl start chroma-agent
    systemctl enable chroma-agent
    ```

1. Start the Lustre\* kernel modules (the Intel® Manager for Lustre\* `ocf:chroma:Target` resource agent expects the Lustre\* kernel modules to be loaded, or it will abort):

    ```bash
    modprobe lustre
    ```

    **Note:** This step is not always required, as the modules will be automatically loaded on system boot.

### Migrate the Lustre\* Services to Node 1

1. Stop the cluster service on the secondary node. Login to **node 2** and run:

    ```bash
    pcs cluster standby
    service pacemaker stop
    service corosync stop
    pcs cluster disable
    ```

    **Note:** This will incur an outage of the file system for the length of time it takes to shut down the services on node 2 and then restart them on the upgraded node 1 server. This interruption can be minimized with careful planning.

1. On node 1, take the new cluster configuration out of `maintenance-mode`:

    ```bash
    pcs property set maintenance-mode=false
    ```

1. On node 1, start the targets on the new cluster configuration:

    ```bash
    pcs resource enable <resource name>
    ```

    For example:

    ```bash
    [root@ct6-mds1 ~]# pcs resource
    MGS_32834e    (ocf::chroma:Target):    Stopped (disabled)
    demo-MDT0000_802c1b    (ocf::chroma:Target):    Stopped (disabled)

    [root@ct6-mds1 ~]# pcs resource enable MGS_32834e
    [root@ct6-mds1 ~]# pcs resource enable demo-MDT0000_802c1b

    [root@ct6-mds1 ~]# pcs resource
    MGS_32834e    (ocf::chroma:Target):    Started ct6-mds1.lfs.intl
    demo-MDT0000_802c1b    (ocf::chroma:Target):    Started ct6-mds1.lfs.intl
    ```

    The following script can be used to enable all resources in the cluster:

    ```bash
    for i in `pcs resource|awk '{print $1}'`; do
    pcs resource enable $i
    done
    ```

1. The resources should now be running on the upgraded cluster node.

### Upgrade Node 2

#### Install the New Operating System Version on Node 2

1. Shut down the second server, **node 2**
1. Following the vendor's instructions, install the new OS version on node 2

#### Restore the Node 2 OS Configuration from Backup

1. When the initial OS installation is complete, copy the backup tarball onto the new installation on node 2 and extract it:

    ```bash
    cd $HOME
    tar zxf bck-`hostname`-*.tgz
    ```

1. Restore the network interfaces, using the utilities provided by the OS (e.g. `nmtui-edit`). The backup contains the raw configuration files for reference, in ``bck-`hostname`-*/etc/sysconfig/network-scripts``. Do not forget to restore the network configuration of the direct network connection between the server nodes (used as `ring1` for Corosync communications).
1. Restore the NTP configuration. For example:

    ```bash
    # install ntp
    yum -y install ntp
    # Restore the NTP configuration
    mv /etc/ntp.conf /etc/ntp.conf.inst
    cp $HOME/bck-`hostname`-*/etc/ntp.conf /etc/.
    # Start NTP
    ntpd -qg
    systemctl enable ntpd
    systemctl start ntpd
    ```

1. Restore the hosts database and DNS resolver configuration. For example:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/hosts /etc/.
    cp $HOME/bck-`hostname`-*/etc/resolv.conf /etc/.
    cp $HOME/bck-`hostname`-*/etc/nsswitch.conf /etc/.
    ```

1. Restore the user management configuration (`passwd`, `group`, `shadow`, `gshadow`, `sudoers`). For example:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/passwd /etc/.
    cp $HOME/bck-`hostname`-*/etc/group /etc/.
    cp $HOME/bck-`hostname`-*/etc/shadow /etc/.
    cp $HOME/bck-`hostname`-*/etc/gshadow /etc/.
    cp $HOME/bck-`hostname`-*/etc/sudoers /etc/.
    ```

1. Restore the SSH configuration from the backup:

    ```bash
    mv /root/.ssh /root/.ssh.inst
    cp -a $HOME/bck-`hostname`-*/root/.ssh /root/.ssh/
    mv /etc/ssh /etc/ssh.inst
    cp -a $HOME/bck-`hostname`-*/etc/ssh /etc/ssh
    ```

    **Note:** If SELinux is enabled, the permissions for the files in `/etc/ssh` will need to be updated with the correct SELinux label. For example:

    ```bash
    chcon -Rv system_u:object_r:sshd_key_t:s0 /etc/ssh/ssh_host_*
    ```

    Restoring the `/etc/ssh` configuration and root user ssh keys is optional but will make the process of upgrading easier.

1. Restore the LNet configuration (file name may vary, depending on how LNet was configured and any customization that may have been carried out). The following example assumes that the server has a configuration that was created by Intel® Manager for Lustre\*:

    ```bash
    cp $HOME/bck-`hostname`-*/etc/modprobe.d/iml_lnet_module_parameters.conf /etc/modprobe.d/.
    ```

#### Install the EPEL Repository Definition on Node 2

1. Login to node 2.
1. Install EPEL repository support:

    ```bash
    yum -y install epel-release
    ```

#### Install the Intel® Manager for Lustre\* Agent on Node 2

1. Login to node 2.
1. Install the Intel® Manager for Lustre\* COPR Repository definition, which contains some dependencies for the Intel® Manager for Lustre\* Agent:

    ```bash
    yum-config-manager --add-repo \
    https://copr.fedorainfracloud.org/coprs/managerforlustre/manager-for-lustre/repo/epel-7/managerforlustre-manager-for-lustre-epel-7.repo
    ```

1. Install the DNF project COPR Repository definition. DNF is a package manager, and is used as a replacement for YUM in many distributions, such as Fedora. It does not replace YUM in CentOS, but Intel® Manager for Lustre\* does make use of some of the newer features in DNF for some of its tasks:

    ```bash
    yum-config-manager --add-repo \
    https://copr.fedorainfracloud.org/coprs/ngompa/dnf-el7/repo/epel-7/ngompa-dnf-el7-epel-7.repo
    ```

1. Restore the Intel® Manager for Lustre\* Agent configuration and certificates to the node:

    ```bash
    cp -a $HOME/bck-`hostname`-*/var/lib/chroma /var/lib/.
    ```

1. Install the Intel® Manager for Lustre\* Agent repository definition:

    ```bash
    curl -o /etc/yum.repos.d/Manager-for-Lustre.repo \
    --cacert /var/lib/chroma/authority.crt \
    --cert /var/lib/chroma/self.crt \
    --key /var/lib/chroma/private.pem \
    https://<admin server>/repo/Manager-for-Lustre.repo
    ```

    Replace `<admin server>` in the `https` URL with the appropriate Intel® Manager for Lustre\* hostname (normally the fully-qualified domain name).

1. Install The Intel® Manager for Lustre\* Agent and Diagnostics packages

    ```bash
    yum -y install chroma-\*
    ```

    **Note:** following warning during install / update is benign and can be ignored:

    ```bash
    ...
      /var/tmp/rpm-tmp.MV5LGi: line 5: /selinux/enforce: No such file or directory
      []

      {
        "result": null,
        "success": true
      }
    ...
    ```

#### Install the Lustre\* Server Software on Node 2

1. For systems that have **both** LDISKFS and ZFS OSDs:

    **Note:** This is the configuration that Intel® Manager for Lustre\* installs for all managed-mode Lustre\* storage clusters. Use this configuration for the highest level of compatibility with Intel® Manager for Lustre\*.

    1. Install the Lustre\* `e2fsprogs` distribution:

        ```bash
        yum --nogpgcheck --disablerepo=* --enablerepo=e2fsprogs-wc \
        install e2fsprogs e2fsprogs-devel
        ```

    1. If the installed `kernel-tools` and  `kernel-tools-libs` packages are at a higher revision than the patched kernel packages in the Lustre\* server repository, they will need to be removed:

        ```bash
        yum erase kernel-tools kernel-tools-libs
        ```

    1. Install the Lustre-patched kernel packages. Ensure that the Lustre\* repository is picked for the kernel packages, by disabling the OS repos:

        ```bash
        yum --nogpgcheck --disablerepo=base,extras,updates \
        install \
        kernel \
        kernel-devel \
        kernel-headers \
        kernel-tools \
        kernel-tools-libs \
        kernel-tools-libs-devel
        ```

    1. Install additional development packages. These are needed to enable support for some of the newer features in Lustre\* – if certain packages are not detected by Lustre's\* configure script when its DKMS package is installed, the features will not be enabled when Lustre\* is compiled. Notable in this list are `krb5-devel` and `libselinux-devel`, needed for Kerberos and SELinux support, respectively.

        ```bash
        yum install asciidoc audit-libs-devel automake bc \
        binutils-devel bison device-mapper-devel elfutils-devel \
        elfutils-libelf-devel expect flex gcc gcc-c++ git glib2 \
        glib2-devel hmaccalc keyutils-libs-devel krb5-devel ksh \
        libattr-devel libblkid-devel libselinux-devel libtool \
        libuuid-devel libyaml-devel lsscsi make ncurses-devel \
        net-snmp-devel net-tools newt-devel numactl-devel \
        parted patchutils pciutils-devel perl-ExtUtils-Embed \
        pesign python-devel redhat-rpm-config rpm-build systemd-devel \
        tcl tcl-devel tk tk-devel wget xmlto yum-utils zlib-devel
        ```

    1. Ensure that a persistent hostid has been generated on the machine. If necessary, generate a persistent hostid (needed to help protect zpools against simultaneous imports on multiple servers). For example:

        ```bash
        hid=`[ -f /etc/hostid ] && od -An -tx /etc/hostid|sed 's/ //g'`
        [ "$hid" = `hostid` ] || genhostid
        ```

    1. Reboot the node.

        ```bash
        reboot
        ```

    1. Install the metapackage that will install Lustre\* and the LDISKFS and ZFS 'kmod' packages:

        ```bash
        yum --nogpgcheck install lustre-ldiskfs-zfs
        ```

    1. Verify that the DKMS kernel modules for Lustre\*  SPL and ZFS have installed correctly:

        ```bash
        dkms status
        ```

        All packages should have the status `installed`. For example:

        ```bash
        # dkms status
        lustre, 2.10.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        spl, 0.7.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        zfs, 0.7.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        ```

    1. Load the Lustre\* and ZFS kernel modules to verify that the software has installed correctly:

        ```bash
        modprobe -v zfs
        modprobe -v lustre
        ```

1. For systems that use only LDISKFS OSDs:
    1. Install the Lustre\* `e2fsprogs` distribution:

        ```bash
        yum --nogpgcheck \
        --disablerepo=* --enablerepo=e2fsprogs-wc install e2fsprogs
        ```

    1. Install the Lustre-patched kernel packages. Ensure that the Lustre\* repository is picked for the kernel packages, by disabling the OS repos:

        ```bash
        yum --nogpgcheck --disablerepo=base,extras,updates \
        install \
        kernel \
        kernel-devel \
        kernel-headers \
        kernel-tools \
        kernel-tools-libs \
        kernel-tools-libs-devel
        ```

    1. Reboot the node.

        ```bash
        reboot
        ```

    1. Install the LDISKFS `kmod` and other Lustre\* packages:

        ```bash
        yum --nogpgcheck install \
        kmod-lustre \
        kmod-lustre-osd-ldiskfs \
        lustre-osd-ldiskfs-mount \
        lustre \
        lustre-resource-agents
        ```

    1. Load the Lustre\* kernel modules to verify that the software has installed correctly:

        ```bash
        modprobe -v lustre
        ```

1. For systems with ZFS-based OSDs:
    1. Install the kernel packages that match the latest supported version for the Lustre\* release:

        ```bash
        yum install \
        kernel \
        kernel-devel \
        kernel-headers \
        kernel-tools \
        kernel-tools-libs \
        kernel-tools-libs-devel
        ```

        It may be necessary to specify the kernel package version number in order to ensure that a kernel that is compatible with Lustre\* is installed. For example, Lustre\* 2.10.1 has support for RHEL kernel 3.10.0-693.2.2.el7:

        ```bash
        yum install \
        kernel-3.10.0-693.2.2.el7 \
        kernel-devel-3.10.0-693.2.2.el7 \
        kernel-headers-3.10.0-693.2.2.el7 \
        kernel-tools-3.10.0-693.2.2.el7 \
        kernel-tools-libs-3.10.0-693.2.2.el7 \
        kernel-tools-libs-devel-3.10.0-693.2.2.el7
        ```

        **Note:** If the `kernel-tools` and  `kernel-tools-libs` packages that have been installed on the host prior to running this command are at a higher revision than the kernel version supported by Lustre\*, they will need to be removed first:

        ```bash
        yum erase kernel-tools kernel-tools-libs
        ```

        Refer to the [Lustre\* Changelog](http://wiki.lustre.org/Category:Changelog) for the list of supported kernels.

    1. Install additional development packages. These are needed to enable support for some of the newer features in Lustre\* – if certain packages are not detected by Lustre's\* configure script when its DKMS package is installed, the features will not be enabled when Lustre\* is compiled. Notable in this list are `krb5-devel` and `libselinux-devel`, needed for Kerberos and SELinux support, respectively.

        ```bash
        yum install \
        asciidoc audit-libs-devel automake bc \
        binutils-devel bison device-mapper-devel elfutils-devel \
        elfutils-libelf-devel expect flex gcc gcc-c++ git \
        glib2 glib2-devel hmaccalc keyutils-libs-devel krb5-devel ksh \
        libattr-devel libblkid-devel libselinux-devel libtool \
        libuuid-devel libyaml-devel lsscsi make ncurses-devel \
        net-snmp-devel net-tools newt-devel numactl-devel \
        parted patchutils pciutils-devel perl-ExtUtils-Embed \
        pesign python-devel redhat-rpm-config rpm-build systemd-devel \
        tcl tcl-devel tk tk-devel wget xmlto yum-utils zlib-devel
        ```

    1. Ensure that a persistent hostid has been generated on the machine. If necessary, generate a persistent hostid (needed to help protect zpools against simultaneous imports on multiple servers). For example:

        ```bash
        hid=`[ -f /etc/hostid ] && od -An -tx /etc/hostid|sed 's/ //g'`
        [ "$hid" = `hostid` ] || genhostid
        ```

    1. Reboot the node.

        ```bash
        reboot
        ```

    1. Install the packages for Lustre\* and ZFS:

        ```bash
        yum --nogpgcheck install \
        lustre-dkms \
        lustre-osd-zfs-mount \
        lustre \
        lustre-resource-agents \
        zfs
        ```

    1. Verify that the DKMS kernel modules for Lustre\*  SPL and ZFS have installed correctly:

        ```bash
        dkms status
        ```

        All packages should have the status `installed`. For example:

        ```bash
        # dkms status
        lustre, 2.10.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        spl, 0.7.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        zfs, 0.7.1, 3.10.0-693.2.2.el7_lustre.x86_64, x86_64: installed
        ```

    1. Load the Lustre\* and ZFS kernel modules to verify that the software has installed correctly:

        ```bash
        modprobe -v zfs
        modprobe -v lustre
        ```

#### Add Node 2 to the new High Availability Framework

1. Install the OS cluster software:

    ```bash
    yum -y install pcs pacemaker corosync fence-agents
    ```

1. Ensure `hacluster` user is present on the server. For example:

    ```bash
    [root@ct6-mds2 ~]# id hacluster
    uid=189(hacluster) gid=189(haclient) groups=189(haclient)
    ```

    If required, add the `hacluster` user – usually the user is created when the cluster software is installed.

1. Set the password for the `hacluster` user:

    ```bash
    passwd hacluster
    ```

1. Modify or disable the firewall. According to Red Hat, the following ports need to be enabled:
    1. TCP: ports 2224, 3121, 21064
    1. UDP: ports 5405
1. In RHEL / CentOS 7, the firewall software can be configured to permit cluster traffic as follows:

    ```bash
    firewall-cmd --permanent --add-service=high-availability
    firewall-cmd --add-service=high-availability
    ```

    **Note:** both commands are required. The first command writes a persistent record of the firewall rules without changing the running configuration, while the second command changes the running configuration.

1. Verify the firewall configuration as follows:

    ```bash
    firewall-cmd --list-service
    ```

1. Alternatively, disable the firewall completely:

    ```bash
    systemctl stop firewalld
    systemctl disable firewalld
    ```

1. Start the Pacemaker configuration daemon, `pcsd`, and enable it to start on system boot:

    ```bash
    systemctl start pcsd.service
    systemctl enable pcsd.service
    ```

1. Verify that the `pcsd` service is running:

    ```bash
    systemctl status pcsd.service
    ```

1. Set up PCS authentication by executing the following command on **node 1** (*not* node 2):

    ```bash
    pcs cluster auth <node1 fqdn> <node2 fqdn> -u hacluster
    ```

    **Note:** Both node 1 and node 2 need to be supplied on the command line, even though node 1 has already been previously added. For example:

    ```bash
    [root@ct6-mds1 ~]# pcs cluster auth \
      ct6-mds1.lfs.intl ct6-mds2.lfs.intl \
      -u hacluster
    Password:
    ct6-mds1.lfs.intl: Authorized
    ct6-mds2.lfs.intl: Authorized
    ```

    **Note:** When working with host names in Pacemaker and Corosync, use the fully qualified domain names for the nodes.

1. From **node 1**, add node 2 into the upgraded cluster framework:

    ```bash
    pcs cluster node add <node2 fqdn> [--start]
    ```

1. Login to **node 2** and start the cluster framework (if the `--start` flag was not used in the previous step):

    ```bash
    pcs cluster start
    ```

1. On **node 2**, create the mount points for the storage targets. If not, the resource agent, `ocf:chroma:Target` will fail. The expected mount points can be derived from the target configuration files in ``$HOME/bck-`hostname`-*/var/lib/chroma/targets/*``. The following script extracts the mount points from the files:

    ```bash
    # Simple script to create the mount points from the JSON data:
    for i in /var/lib/chroma/targets/*;do
    cat $i | python -c 'import sys, json; print json.load(sys.stdin)["mntpt"]' | xargs mkdir -p
    done
    ```

### Start the Agent Service and Load the Kernel Modules on Node 2

1. Start the `chroma-agent` service:

    ```bash
    systemctl start chroma-agent
    systemctl enable chroma-agent
    ```

1. Start the Lustre\* kernel modules (the Intel® Manager for Lustre\* `ocf:chroma:Target` resource agent expects the Lustre\* kernel modules to be loaded, or it will abort):

    ```bash
    modprobe lustre
    ```

    **Note:** this step is not always required, as the modules will be automatically loaded on system boot.

### Rebalance the Cluster Resources

1. Use the `pcs resource relocate show` command to review the changes that will be made to the cluster resources without committing the change:

    ```bash
    pcs resource relocate show
    ```

1. Use the `pcs resource relocate run` command to execute the relocation plan:

    ```bash
    pcs resource relocate run
    ```

1. Verify that the resources are running on their preferred nodes in the now-upgraded cluster pair:

    ```bash
    pcs resource show
    pcs constraint show
    ```

    For example:

    ```bash
    [root@ct6-mds2 ~]# pcs resource show
    MGS_32834e    (ocf::chroma:Target):    Started ct6-mds1.lfs.intl
    demo-MDT0000_802c1b    (ocf::chroma:Target):    Started ct6-mds2.lfs.intl

    [root@ct6-mds2 ~]# pcs constraint show
    Location Constraints:
    Resource: MGS_32834e
        Enabled on: ct6-mds1.lfs.intl (score:20)
        Enabled on: ct6-mds2.lfs.intl (score:10)
    Resource: demo-MDT0000_802c1b
        Enabled on: ct6-mds2.lfs.intl (score:20)
        Enabled on: ct6-mds1.lfs.intl (score:10)
    Ordering Constraints:
    Colocation Constraints:
    Ticket Constraints:
    ```

1. Both nodes are now upgraded.

**Note:** This guide does not enable Pacemaker and Corosync to start automatically on system boot. By not starting the services at boot time, the administrator has the opportunity to review the server configuration and run-time prior to re-introducing a node to the cluster framework.

When creating new file systems, Intel® Manager for Lustre\* will enable Pacemaker and Corosync to load on boot, and it is a supported configuration; however,disabling automatic startup can simplify maintenance and debugging procedures and can be less disruptive to the cluster should one of the nodes start to experience intermittent but frequent failures.

## Cluster Power Management Configuration

The power management controls for node fencing in Pacemaker are managed using Intel® Manager for Lustre\*'s `st-fencing` resource, which uses the `stonith:fence_chroma` agent. Intel® Manager for Lustre\* stores the fencing configuration variables as node attributes in the Pacemaker cluster configuration, and the variables can be retrieved using the `pcs property show` command:

```bash
pcs property show
```

For example:

```bash
[root@ct6-mds2 ~]# pcs property show
Cluster Properties:
 cluster-infrastructure: corosync
 cluster-name: lustre-ha-cluster
 dc-version: 1.1.15-11.el7_3.4-e174ec8
 have-watchdog: false
 last-lrm-refresh: 1492491703
 maintenance-mode: false
 no-quorum-policy: ignore
 stonith-enabled: true
 symmetric-cluster: true
Node Attributes:
 ct6-mds1.lfs.intl: 0_fence_agent=fence_virsh 0_fence_ipaddr=192.168.0.1 0_fence_ipport=22 0_fence_login=root 0_fence_password=calvin 0_fence_plug=ct6-mds1
 ct6-mds2.lfs.intl: 0_fence_agent=fence_virsh 0_fence_ipaddr=192.168.0.1 0_fence_ipport=22 0_fence_login=root 0_fence_password=calvin 0_fence_plug=ct6-mds2
```

To read in the node attributes from the cluster configuration backup file, use the following syntax:

```bash
pcs -f $HOME/bck-`hostname`-*/cluster-cfg-`hostname`.xml property show
```

As a consequence of this design, restoring the power control configuration to the nodes is straightforward. The `st-fencing` STONITH resource was added to the cluster in a previous step, so now use the `pcs property set` command to set the variables used by the fencing agent:

```bash
pcs property set --node <node fqdn> <name>=<var> [<name>=<var> ...]
```

For example:

```bash
pcs property set --node ct6-mds1.lfs.intl \
  0_fence_agent=fence_virsh \
  0_fence_ipaddr=192.168.0.1 \
  0_fence_ipport=22 \
  0_fence_login=kvmadmin \
  0_fence_password=xyzzy \
  0_fence_plug=ct6-mds1
```

The following script can be used to construct a command line to restore the cluster node attributes by extracting the values from the backup of the original configuration:

```bash
pcs -f $HOME/bck-`hostname`-*/cluster-cfg-`hostname`.xml property show | \
awk '/Node Attributes/{na=1;next} na==1 && /^[ \t]+/{sub(/:/,"",$1);printf "pcs property set --node %s ", $1;$1=""; print;next} na==1 && !/^[ \t]+/{na=0}'
```

**Note:** The power control configuration could be restored at an earlier phase in the process, but it is conducted last in order to minimize the chance of accidentally executing a STONITH action on one of the nodes during the upgrade process. The workflow outlined in this document is meant to allow operators to upgrade their Lustre\* environment with the least amount of disruption, so the final power control setup is left to the end.

Please also refer to the Intel® Manager for Lustre\* documentation and online help for instructions on how to configure cluster power management for the Lustre\* servers. If there are any issues with restoring the fencing agents for each cluster, it may be necessary to remove the original configuration from the Intel® Manager for Lustre\* UI and re-add.

\* Other names and brands may be claimed as the property of others.
