# Upgrading Integrated Manager for Lustre 5.0.0 to Lustre {{site.lustre_version}} and Integrated Manager for Lustre {{site.version}}

[**Upgrade Guide**](ug_TOC.md)

## Upgrade Integrated Manager for Lustre

The first component in the environment to upgrade is the Integrated Manager for Lustre server and software. The manager server upgrade can be conducted without any impact to the Lustre file system services.

### Backup the Existing configuration

Prior to commencing the upgrade, it is essential that a backup of the existing configuration is completed. This will enable recovery of the original configuration in the event of a problem occurring during execution of the upgrade.

The following shell script can be used to capture the essential configuration information that is relevant to the Integrated Manager for Lustre software itself:

```bash
#!/bin/sh
# Integrated Manager for Lustre (IML) server backup script

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

Copy the backup tarball to a safe location that is not on the server being upgraded.

**Note:** This script is not intended to provide a comprehensive backup of the entire operating system configuration. It covers the essential components pertinent to Lustre servers managed by Integrated Manager for Lustre that are difficult to re-create if deleted.

### Install the Integrated Manager for Lustre Upgrade

The software upgrade process requires super-user privileges to run. Login as the `root` user or use `sudo` to elevate privileges as required.

1. Download the latest Integrated Manager for Lustre release repo:

   ```sh
   yum-config-manager --add-repo=https://github.com/whamcloud/integrated-manager-for-lustre/releases/download/v5.1.0/chroma_support.repo
   ```

1. Verify that the old iml-5.0 repo file has been removed from the repolist and that the 5.1 repo has been added.

   ```bash
   yum clean all
   yum repolist
   ```

1. Run the OS upgrade.

   ```bash
   yum clean all
   yum update
   ```

Refer to the operating system documentation for details on the correct procedure for upgrading between minor OS releases. Note that a mapping of new installs and upgrades will be displayed. Look through this chart carefully and verify that python2-iml-manager is marked for upgrade and that it will be upgraded to {{site.version}}.

1. Run `chroma-config setup` to complete the installation.

1. Update the repos on each server node (run from the manager node):

   ```bash
   iml update-repo <node name>
   ```

1. Perform a hard refresh on the browser and verify that IML loads correctly.

## Upgrade the Lustre Servers

Lustre server upgrades can be coordinated as either an online roll-out, leveraging the failover HA mechanism to migrate services between nodes and minimize disruption, or as an offline service outage, which has the advantage of usually being faster to deploy overall, with generally lower risk.

The upgrade procedure documented here describes the faster and more reliable approach, which requires that the filesystem be stopped. It assumes that the Lustre servers have been installed in pairs, where each server pair forms an independent high-availability cluster built on Pacemaker and Corosync. Integrated Manager for Lustre deploys these configurations and uses both the stock Lustre resource agent and clusterlabs ZFS resource agent. Integrated Manager for Lustre can also configure STONITH agents to provide node fencing in the event of a cluster partition or loss of quorum.

### Backup Existing Server Data

1. As a precaution, create a backup of the existing configuration for each server. The following shell script can be used to capture the essential configuration information that is relevant to Integrated Manager for Lustre managed mode servers:

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

   **Note:** This is not intended to be a comprehensive backup of the entire operating system configuration. It covers the essential components pertinent to Lustre servers managed by Integrated Manager for Lustre that are difficult to re-create if deleted. Make sure to backup any other important configuration files that may be on your system, such as multipath configurations.

   The following files will need to be backed up if multipath is being used on the system:

   ```sh
   /etc/multipath/*
   /etc/multipath.conf
   ```

1. Copy the backups for each server's configuration to a safe location that is not on the servers being upgraded.

## Stopping the filesystem

IML requires that the filesystem(s) associated with each node to be upgraded must be stopped. Follow these steps:

1. Navigate to _Configuration->Filesystems_
1. For each filesystem listed:

   1. Click the filesystem's `Actions` button
   1. Select _Stop_

## Upgrade the OS on each server node

In order to upgrade, make sure yum is configured on each server node to pull down CentOS 7.6 packages. You may need to disable the CentOS base repo and enable the vault repos. For example:

```bash
sed -i "s/enabled=[0-1]//g" /etc/yum.repos.d/CentOS-Base.repo
sed -i "s/gpgcheck=\([0-1]\)/gpgcheck=\1\nenabled=0/g" /etc/yum.repos.d/CentOS-Base.repo
yum-config-manager --add-repo=http://vault.centos.org/7.6.1810/os/x86_64/
yum-config-manager --add-repo=http://vault.centos.org/7.6.1810/extras/x86_64/
yum-config-manager --add-repo=http://vault.centos.org/7.6.1810/updates/x86_64/
```

Next, from the manager node, upgrade the OS for each host using a pdsh expression (you may need to install pdsh via yum).

```bash
 pdsh -w root@mds[1,2] -w root@oss[1,2] "yum -y upgrade --exclude=python2-iml*"
```

## Run the updates

Next, navigate to the server page and proceed to update each of the servers:

1. Navigate to _Configuration->Servers_
1. Each storage server should report "Updates are ready for server X"
1. Click the _Install Updates_ button
1. Select all storage servers for upgrade and begin the upgrade.

## Summary

Start the filesystem once the upgrade job for each server completes. Connect a client and verify that it is able to access files on the filesystem.

[top](upgrading-integrated-manager-for-lustre-500-to-lustre-{{site.lustre_version | remove: '.'}}-and-integrated-manager-for-lustre-{{site.version | remove: '.'}})
