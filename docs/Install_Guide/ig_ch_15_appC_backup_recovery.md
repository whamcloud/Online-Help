# <a name="1.0"></a>Appendix C - Backup and Recovery of Servers Managed by Integrated Manager for Lustre* software

[**Software Installation Guide Table of Contents**](ig_TOC.md)

**In this Chapter**:

- [Introduction](#introduction)
- [Backup Overview](#backup-overview)
- [Example Backup Checklist](#example-backup-checklist)
- [Operating System](#operating-system)
- [Host Name Resolution](#host-name-resolution)
- [Package Update management environment (RPM & YUM)](#package-update-management-environment)
- [Identity configuration](#identity-configuration)
- [Security configuration](#security-configuration)
- [Creating a Backup Manifest for a Metadata Server or Object Storage Server](#creating-a-backup-manifest-for-a-metadata-server-or-object-storage-server)
- [Chroma Agent Configuration](#chroma-agent-configuration)
- [Integrated Manager for Lustre* software YUM Repository Configuration](#manager-for-lustre-yum-repository-configuration)
- [Network Configuration](#network-configuration)
- [SELinux Configuration](#selinux-configuration)
- [Lustre* LNET Configuration](#lustre-lnet-configuration)
- [Pacemaker and Corosync High Availability Framework](#pacemaker-and-corosync-high-availability-framework)
- [System Services Startup Scripts (rc.sysinit)](#system-services-startup-scripts)
- [Sample Automated Backup Script for Manager Lustre* Servers](#sample-automated-backup-script-for-manager-lustre-servers)
- [Restoring a Server from Backup](#restoring-a-server-from-backup)


**Note**: This appendix is outdated and in
revision.  Procedures in this appendix were developed for servers
running RHEL 6.7.  The process for servers running RHEL {{site.centos_version}} is very
similar, but *this appendix has not yet been revised or tested for RHEL
{{site.centos_version}}*.

Introduction
------------

This appendix provides guidance on how to conduct bare-metal recovery of
a Lustre* server from a combination of the original installation media
and a backup manifest for the servers. This content describes the
essential files required to recover the service to the point of the last
successful backup. From this, readers can create processes that are
compatible with their own environments.

**Note**: Backup and restoration of file system data is beyond the scope
of this procedure.

Integrated Manager for Lustre* software provides a way to configure Lustre
servers as metadata and object storage servers. Such servers are
configured into high availability cluster pairs as defined in this
section: [Building the System – The High Availability Configuration
Spec](ig_ch_03_building.md/#building-the-system-the-high-availability-configuration-spec).

For a high-availability Lustre* file system configured and managed by
Integrated Manager for Lustre* software, there must be at least one cluster
pair hosting the Management Server (MGS) and a Metadata Server (MDS) for
the file system. With the introduction of Distributed Namespace (DNE),
there may be additional metadata server pairs, hosting further MDS
resources.

In such an HA file system, there must also be at least one Object
Storage Server (OSS) high availability cluster pair. There may be a
large number of OSS pairs in a single Lustre* file system.

The process described herein assumes that Integrated Manager for Lustre*
software has provisioned Lustre* servers and that a Lustre* file system
has been successfully created. This process is restricted to coverage of
managed servers and applies equally to Metadata and Object Storage
servers.

Backup Overview
---------------

Just as for any critical server infrastructure, it is essential to
maintain a comprehensive and consistent backup of the system
configuration for all of the servers managed by Integrated Manager for Lustre* software server
software, and to maintain a repeatable and reliable method for
recovering file system services in the event of a failure.

Backup and recovery of Integrated Manager for Lustre* software MDS and OSS server software
involves the following components:

-   Operating system installation and configuration, to include:

    -   File system layout

    -   Core packages

    -   Boot loader

    -   Date, time and language

    -   Network configuration

    -   Name service (/etc/resolv.conf) and hosts table (/etc/hosts)

    -   Package Update management environment (RPM & YUM configuration)

    -   Identity configuration

        -   User databases (/etc/passwd, /etc/shadow, /etc/group,
            > /etc/gshadow)

        -   Name service switch (/etc/nsswitch.conf)

        -   Superuser privilege management (Sudo)

    -   Security configuration

        -   IPTables

        -   SELinux

        -   PAM

        -   SSH keys (host and user)

-   Integrated Manager for Lustre* software installation and configuration

    -   Additional packages required by Lustre

    -   NTP configuration

    -   SSL Certificates

    -   High availability software configuration

Rather than rely upon a standard backup of the operating platform root
disks, an alternative strategy of creating a repeatable build procedure
from first principals will deliver a more predictable mechanism in the
long term. Building servers to a recipe makes it easier to audit
installations for correctness by being able to compare the manifest
(recipe) to the deployed instance, as well as making it easier to track
and deploy changes. This also reduces reliance on backup infrastructure
for recovery, allowing one to concentrate backup efforts on those
critical data sets that cannot be reproduced. This will generally reduce
overall recovery times by reducing the amount of data that must be
restored from the backup infrastructure (which is often tape-based and
bandwidth-constrained).

### Example Backup Checklist

The following is an example checklist of high level tasks to perform in
executing a backup. Perform these tasks after creating an Integrated Manager for Lustre*
software file system using the Integrated Manager for Lustre* software dashboard.

-   Save Kickstart Template from OS Installation (or create one)

-   Save OS network configuration (can be included in Kickstart
    template)

-   Save YUM configuration

-   Save user configuration

-   Save SSH host keys \[optional\]

-   Save SSH root user keys \[optional\]

-   Save NTP configuration

-   Save Integrated Manager for Lustre* software agent configuration

-   Save the LNET configuration

-   Save the Pacemaker + Corosync configuration

Operating System
----------------

**Note**: This appendix is outdated and in revision.  Procedures in this
appendix were developed for servers running RHEL 6.7.  The process for
servers running RHEL {{site.centos_version}} is very similar, but this appendix has not yet
been revised or tested for RHEL {{site.centos_version}}.

Red Hat Enterprise Linux or CentOS Linux, version {{site.centos_version}} must be
installed on all Lustre* servers. The OS must be deployed in a consistent
and repeatable manner. All servers should be running the same OS and
version. For Red Hat Enterprise Linux and CentOS Linux, template-driven
provisioning using Kickstart has proven to be reliable and
straightforward to audit. RHEL-based operating systems generate a
Kickstart template during the normal, media-based installation process
and this can be an effective starting point for developing an automated
installation process.

An alternative to template-driven OS provisioning is to develop a binary
image that is ready to be written directly to bare storage on the
server. Image-based platforms can be more difficult to maintain and
audit, but are often faster to deploy and are especially effective when
the underlying hardware platform is guaranteed to be consistent over the
operational life-span of the service.

Regardless of the mechanism, the operating system installation and
recovery is usually driven from a description of the end-state, rather
than from a backup in the purest sense. It is assumed that the core
operating system changes infrequently and that any changes are
automatically incorporated into the provisioning platform (either by
editing the template or updating the "golden" image). It is further
assumed that there is nothing in the data held by the core OS that
requires routine archival. If this is not the case, additional
procedures may be required to ensure that relevant data is persistently
and reliably backed up

The following example Kickstart template describes a basic platform with
a small set of packages and two network interfaces: one for provisioning
the OS and connection to the Integrated Manager for Lustre* software management network,
the other might be used for Lustre* communications traffic (if Ethernet
is being used for Lustre* networking).

An *example* Kickstart template:


```
install
text
reboot
url --url=http://10.0.1.1/CS6.4/
lang en\_US.UTF-8
keyboard us
network --hostname ee-iml --onboot yes --device eth0 --bootproto static
--ip 10.0.2.1 --netmask 255.255.0.0 --gateway 10.0.0.1 --noipv6
--nameserver 8.8.8.8
network --onboot yes --device eth1 --bootproto static --ip 10.1.0.1
--netmask 255.255.0.0 --noipv6
rootpw  --iscrypted xyzzy
firewall --disabled
selinux --disabled
authconfig --enableshadow --passalgo=sha512
timezone --utc America/New\_York
bootloader --location=mbr --driveorder=vda --append="crashkernel=auto
console=ttyS0,115200 rd\_NO\_PLYMOUTH"
zerombr
clearpart --all --initlabel --drives=vda
autopart
repo --name="CentOS" --baseurl=http://10.0.1.1/CS6.4/ --cost=100
%packages
@core
@base
%end
```


Kickstart templates are flexible and powerful, and can be extended with
the addition of pre-install and post-install scripts. With a modest amount of
effort, the entire operating system installation can be fully automated.

### Host Name Resolution

The hosts database /etc/hosts often contains the names and IP addresses
for all of the members of the Lustre* server infrastructure; include a
copy of this file in the operating system manifest. The file
/etc/resolv.conf contains the list of DNS name servers in use on the
network; include a copy of this file in the manifest as well.

<a id="package-update-management-environment"></a>
### Package Update management environment (RPM & YUM)

The YUM configuration file /etc/yum.conf and files located at
/etc/yum.repos.d/\* must be configured so that package dependencies for
Integrated Manager for Lustre* software can be automatically installed.

### Identity configuration

Ensure that any local user information is appropriately accounted for,
including:

-   User databases (i.e., /etc/passwd, /etc/shadow, /etc/group,
    /etc/gshadow)

-   Superuser privilege management (Sudo)

-   Name service switch (/etc/nsswitch.conf)

### Security configuration

Include the security configuration in the operating system's
provisioning or backup manifest, including firewall rules (IPTables),
Security Enhanced Linux (must be disabled), pluggable authentication
modules (PAMs) and SSH (including Host and User keys).

### Creating a Backup Manifest for a Metadata Server or Object Storage Server

The following sections describe how to rebuild a server from the base
operating system install. It does not include information on OS
installation itself. Instructions are executed as the root superuser on
an example server configuration, for the purpose of demonstration.
Procedures for copying the resulting data off the server to a reliable
medium are not covered here, but can be a simple secure copy (e.g. scp)
from the source to a destination system (such as the server running the
Integrated Manager for Lustre* software GUI), or an integrated enterprise backup
platform.

Backups must be run for each server in the file system and, minimally,
must be run each time a configuration change is made.

### Chroma Agent Configuration

The Integrated Manager for Lustre* software client agent, called chroma-agent, keeps
a set of configuration files in /var/lib/chroma. It is essential that
all files in this directory are saved. In addition to SSL authentication
keys, the directory contains configuration information pertinent to the
server's purpose and supplemental information regarding the storage
configuration used to manage the resources in Pacemaker.

\# SSL Certificates and Chroma Settings:

/var/lib/chroma/\*

### Integrated Manager for Lustre* software YUM Repository Configuration

Integrated Manager for Lustre* software is distributed as RPM packages. These
are hosted in YUM repositories on the manager server running the
Integrated Manager for Lustre* software and GUI.

\# YUM Configuration for IML Repositories:

/etc/yum.repos.d/Intel-Lustre-Agent.repo

### Network Configuration

Copy the network configuration, if it is not already part of an
installation process for the server.

\# Network Configuration:

/etc/sysconfig/network-scripts/ifcfg-\*

/etc/sysconfig/system-config-firewall

/etc/rsyslog.conf

/etc/ntp.conf

### SELinux Configuration

Either copy the SELinux configuration file, or make sure to disable
SELinux during provisioning of the server. For RHEL and CentOS systems,
there is a configuration setting for disabling SELinux in the file:
/etc/selinux/config

### Lustre* LNET Configuration

This is normally set by the Integrated Manager for Lustre* software, but can be
recovered by making a copy of the following file.
```
# Lustre* LNet Configuration:
/etc/modprobe.d/iml_lnet_module_parameters.conf
```

### Pacemaker and Corosync High Availability Framework

The Corosync configuration is held in a plain text file, but the
Pacemaker configuration is more complex and must be exported from the
running cluster resource manager service. Fortunately, there is a simple
command to export the Pacemaker configuration.
```
# Corosync Configuration:
/etc/corosync/corosync.conf

# Pacemaker Configuration:
cibadmin --query > $HOME/cluster-cfg-$HOSTNAME.xml
```

<a id="system-services-startup-scripts"></a>
### System Services Startup Scripts (rc.sysinit)

The following awk script parses the output from the chkconfig command
and creates a shell script that can be executed to re-apply the
runlevels for each of the installed services.

```bash
# RC.Sysinit Services Configuration:

chkconfig --list | awk '{

on="";
off="";

for (i=2;i<=8;i++) {
  if ($i ~ /on$/) {
    on=sprintf("%s%s",on,substr($i,1,1))
  } else {
    off=sprintf("%s%s",off,substr($i,1,1))
  }
}

if (length(off)>0)
    printf("/sbin/chkconfig --levels %s %s off\n",off,$1);
if (length(on)>0)
    printf("/sbin/chkconfig --levels %s %s on\n",on,$1)
}' > $HOME/chkconfig-output-$HOSTNAME.sh
```

<a id="sample-automated-backup-script-for-manager-lustre-servers"></a>
### Sample Automated Backup Script for Integrated Manager for Lustre* software Servers

For a server managed by Integrated Manager for Lustre* software, this script can
be used as the basis for automating the backup of server configuration
information.

```bash
#!/bin/sh

BCKNAME=bck-$HOSTNAME-`date +%Y%m%d-%H%M%S`

BCKROOT=$HOME/$BCKNAME

mkdir -p $BCKROOT

tar cf - \

/var/lib/chroma \

/etc/yum.repos.d/Intel-Lustre-Agent.repo \

/etc/sysconfig/network-scripts/ifcfg-* \

/etc/sysconfig/system-config-firewall \

/etc/rsyslog.conf \

/etc/ntp.conf \

/etc/selinux/config \

/etc/modprobe.d/iml_lnet_module_parameters.conf \

/etc/corosync/corosync.conf \

| (cd $BCKROOT && tar xf -)

# Pacemaker Configuration:

cibadmin --query > $BCKROOT/cluster-cfg-$HOSTNAME.xml

# RC.Sysinit Services Configuration:

chkconfig --list | awk '{

on="";
off="";

for (i=2;i<=8;i++) {
  if ($i ~ /on$/) {
    on=sprintf("%s%s",on,substr($i,1,1))
  } else {
    off=sprintf("%s%s",off,substr($i,1,1))
  }
}

if (length(off)>0)
  printf("/sbin/chkconfig --levels %s %s off\n",off,$1);

if (length(on)>0)

printf("/sbin/chkconfig --levels %s %s on\n",on,$1)

}' > $BCKROOT/chkconfig-output-$HOSTNAME.sh

cd `dirname $BCKROOT`

tar zcf $BCKROOT.tgz `basename $BCKROOT`
```

### Restoring a Server from Backup

The following process restores a server managed by Integrated Manager for
Lustre* software to production state. This is done using backup
resources created as described in the previous sections. This process is
for a single server, but can be repeated for each storage server in a
cluster. When a pair of servers must both be restored, it is recommended
to reinstall the servers one-at-a-time.

The following command line examples assume that the server configuration
has been extracted in to a directory referenced by the variable
\$BACKUP\_ROOT. It is also assumed that basic network connectivity has
been restored, sufficient to allow access to the operating system YUM
repositories, as well as the repositories of the manager server running
the Integrated Manager for Lustre* software GUI.

#### Restore Process

1.  Restore the SELinux configuration.
    ```
    cp $BACKUP_ROOT/etc/selinux/config /etc/selinux/.
    ```

1.  Restore the contents of /var/lib/chroma, which includes the SSL
    certificates and the chroma-agent configuration.
    ```
    cp -a $BACKUP_ROOT/var/lib/chroma /var/lib/.
    ```

1.  Restore the YUM repository definition:
    ```
    cp $BACKUP_ROOT/etc/yum.repos.d/Intel-Lustre-Agent.repo /etc/yum.repos.d/.
    ```

1.  Restore the network interface configuration:
    ```
    cp $BACKUP_ROOT/etc/sysconfig/network-scripts/ifcfg-* /etc/sysconfig/network-scripts/.

    cp $BACKUP_ROOT/etc/sysconfig/system-config-firewall /etc/sysconfig/.
    ```

    > Restart network interfaces, if required for the server to make the
    > connection to the IML server.

1.  Re-install the Integrated Manager for Lustre* software server packages:

    ```bash
    yum -y install --enablerepo=lustre,iml-agent,e2fsprogs \
    lustre \
    kernel-{{site.lustre_kernel_version}}_lustre.x86_64.rpm

    yum -y install --enablerepo=iml-agent \
    chroma-agent \
    chroma-agent-management \
    iml-diagnostics
    ```

1.  Restore the RSyslog configuration and NTP Configuration:
```
cp $BACKUP_ROOT/etc/rsyslog.conf $BACKUP_ROOT/etc/ntp.conf /etc/.
```

1.  Restore the LNET Configuration:
```
cp $BACKUP_ROOT/etc/modprobe.d/iml_lnet_module_parameters.conf
/etc/modprobe.d/.
```

1.  Restore the Corosync configuration:
```
cp $BACKUP_ROOT/etc/corosync/corosync.conf /etc/corosync/.
```

    > **Note**: Do not restore the Pacemaker configuration at this time.

1.  Restore the system services startup configuration (rc.sysinit run
    levels):

    `sh \$BACKUP\_ROOT/chkconfig-output-\$HOSTNAME.sh`

1.  Create the directories for the Lustre* storage mount points. For
    example, the following script extracts the directory paths for the
    Lustre* storage from the chroma-agent configuration, and creates the
    directories:

    ```bash
    for i in /var/lib/chroma/targets/\* ; do

    cat \$i | python -c 'import sys,json; obj=json.load(sys.stdin); print
    obj\["mntpt"\]';

    done | xargs mkdir -p
    ```

    > This method is not officially sanctioned because the format of the
    > JSON configuration is not part of a public API and may change over
    > time. Nevertheless, it's a convenient way to recreate mount points, if
    > they are not already in the build manifest for the server.

1.  Reboot.

1.  When the system has completed booting, verify that the server is
    running the Integrated Manager for Lustre* software Linux kernel, and that LNET
    is properly configured. For example:

    ```
    [root@ee-mds1 ~]# uname -r

    {{site.lustre_kernel_version}}_lustre.x86_64.rpm 
    
    [root@ee-mds1 ~]# modprobe -v lnet

    [root@ee-mds1 ~]# lctl network up

    LNET configured

    [root@ee-mds1 ~]# lctl list\_nids

    <10.70.73.11@tcp>
    ```

1.  Verify that the basic cluster framework is also running:

    ```
    pcs status
    ```

    a.  If the other server in the HA pair is already running, then the
        Pacemaker configuration should have been copied over when Pacemaker
        started on the node being recovered. The cluster status will show
        the resources.

    b.  If both servers in the HA pair have been re-installed, then the
        Pacemaker configuration will need to be restored from the backup as
        well. For example:

    > cibadmin --replace --xml-file
    > \$BACKUP\_ROOT/ee-cluster-cfg-\$HOSTNAME.xml
    >
    > This command will fail if a pre-existing configuration is detected. If
    > the configuration from the backup is absolutely required, then include
    > the --force flag on the command line. Be very careful that this is the
    > correct configuration before proceeding.

1.  The newly restored server may not yet be able to manage resources in
    the cluster, so clear out any historical error conditions and force
    the cluster to re-detect the current state. For example:

    ```
    [root@ee-mds1 ~]# pcs resource show

    MGS_7dec26 (ocf::chroma:Target): Started

    demo-MDT0000_ae5915 (ocf::chroma:Target): Started

    [root@ee-mds1 ~]# pcs resource cleanup MGS_7dec26

    Resource: MGS_7dec26 successfully cleaned up

    [root@ee-mds1 ~]# pcs resource cleanup demo-MDT0000_ae5915

    Resource: demo-MDT0000_ae5915 successfully cleaned up
    ```

1.  If the resources are running on their non-preferred servers (i.e.,
    on the failover hosts), then use the following commands to force a
    failback (or use Integrated Manager for Lustre* software GUI to manage the
    resources):

    ```
    pcs resource move <resource name>
    pcs resource clear <resource name>
    ```

    The resource clear command removes any constraints imposed by the
move, so that the resource can be moved back again in the event of a
subsequent failover trigger.

1.  It may be useful during the initial stages of the recovery process
    for Pacemaker to disable the constraints around the fencing agents.
    This can make it easier to restore services to a running condition
    on one server while still working to rebuild the second. However,
    we do not support Integrated Manager for Lustre* software installations that
    do not have fencing agents configured, so only use this process with
    caution, and only if required to support an emergency recovery. Once
    full service is restored, this configuration change must be
    reversed.

    ```
    pcs property set stonith-enabled=false
    ```

The cluster configuration has now been recovered to the running state
based on the last backup taken. Note that this process assumes that the
Lustre* storage for the MGT, MDTs and OSTs remains intact during the
outage and throughout the server recovery.

[Top of page](#1.0)