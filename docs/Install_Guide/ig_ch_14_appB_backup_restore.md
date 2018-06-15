# <a name="1.0"></a>Appendix B - Backing up and Restoring Integrated Manager for Lustre* software Server Software

[**Software Installation Guide Table of Contents**](ig_TOC.md)

**In this Chapter:**

- [Backup Overview](#backup-overview)
- [Example Backup Checklist](#example-backup-checklist)
- [Operating System](#operating-system)
- [Host Name Resolution](#host-name-resolution)
- [Package Update management environment (RPM & YUM)](#package-update-management-environment)
- [Identity configuration](#identity-configuration)
- [Security configuration](#security-configuration)
- [Integrated Manager for Lustre* software](#manager-for-lustre-software)
- [Creating a Backup Manifest for the Integrated Manager for Lustre* software Server](#creating-a-backup-manifest-for-the-manager-for-lustre-server)
- [Network Configuration Files](#network-configuration-files)
- [YUM Configuration](#yum-configuration)
- [User Configuration](#user-configuration)
- [SSH Host keys (Optional)](#ssh-host-keys-optional)
- [SSH user keys (Optional)](#ssh-user-keys-optional)
- [NTP Configuration](#ntp-configuration)
- [Integrated Manager for Lustre* software SSL Certificates](#manager-for-lustre-ssl-certificates)
- [Integrated Manager for Lustre* software Database](#manager-for-lustre-database)
- [Restoring the Integrated Manager for Lustre* software Service](#restoring-the-manager-for-lustre-service)
- [Re-install OS and Restore System Configuration](#re-install-os-and-restore-system-configuration)
- [Re-install Integrated Manager for Lustre* software](#re-install-manager-for-lustre-software)
- [Restore the NTP Configuration](#restore-the-ntp-configuration)
- [Restore the Integrated Manager for Lustre* software SSL certificates](#restore-the-manager-for-lustre-ssl-certificates)
- [Restore the PostgresSQL Database](#restore-the-postgressql-database)
- [Restart Integrated Manager for Lustre* software](#restart-manager-for-lustre-software)
- [Potential Issues](#potential-issues)


An effective system recovery strategy requires that the administrator
maintains a current backup of critical files and implements a reliable
and repeatable method for restoring the platform to working condition.

This chapter provides guidance on how to conduct a full recovery of the
Integrated Manager for Lustre* software server from a combination of the original
installation media and a backup manifest of the Integrated Manager for Lustre*
software. The manifest will describe the essential files
required in order to restore Integrated Manager for Lustre* software
(referred to herein as “manager software”) and its management of
existing file systems to the point of the last successful backup. From
these instructions, administrators can define a recovery process that is
compatible with their own environment.

This chapter discusses backup and recovery of the manager software,
including the configuration information for Lustre* file systems being
managed and/or monitored by the manager software. Backup and restoration
of data held on any Lustre* file system is not within the scope of this
document.

While no specific recommendations for backup technologies, server
provisioning tools, or infrastructure are made, system managers should
consider investment in an automated OS provisioning system for the
consistent deployment and recovery of the base operating platform for
any computer. Several options exist for server provisioning systems;
these include template-driven installations such as Kickstart (which is
used by Red Hat Enterprise Linux and derivative platforms such as CentOS
and Fedora). Systems such as Symantec Ghost and the open source PING
project install servers from a "golden" binary image. For larger
enterprises, there are comprehensive network operations management
software suites that cover management for the entire production
life-cycle of IT assets.

The processes described herein assume that the operating system can be
redeployed in a consistent and repeatable manner, so that repeated
installations have a known outcome. The following instructions assume
the server’s operating system has been fully installed. From there, this
section describes how to fully restore the manager software, including
the configuration information for Lustre* file systems being managed
and/or monitored by the manager software, from the last complete backup
made of the manager software backup manifest.

Backup Overview
---------------

Backup and recovery of the IML server software platform involves the
following components:

-   Operating system installation and configuration, to include:

    -   File system layout

    -   Core packages

    -   Boot loader

    -   Date, time and language

    -   Network configuration

    -   Name service (/etc/resolv.conf) and hosts table (/etc/hosts)

    -   Package Update management environment (RPM & YUM)

    -   Identity configuration

        -   User databases (/etc/passwd, /etc/shadow, /etc/group,
            /etc/gshadow)

        -   Name service switch (/etc/nsswitch.conf)

        -   Superuser privilege management (Sudo)

    -   Security configuration

        -   IPTables

        -   SELinux

        -   PAM

        -   SSH keys (host and user)

-   Integrated Manager for Lustre* software installation and
    configuration

    -   Additional packages required by IML (installation will attempt
        to automatically resolve package dependencies via YUM)

    -   Messaging services

    -   NTP configuration

    -   SSL Certificates

    -   Data Storage Management (PostgreSQL RDBMS)

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

The following is an example checklist of high-level tasks to perform in
executing a backup. Perform these tasks before restoring the
Integrated Manager for Lustre* software service.

-   Save the Kickstart Template from OS Installation (or create one)


-   Save OS network configuration (can be included in Kickstart
    template)

-   Save YUM configuration

-   Save user configuration

-   Save SSH host keys \[optional\]

-   Save SSH root user keys \[optional\]

-   Run IML Installer

-   Save NTP configuration

-   Save Integrated Manager for Lustre* software server SSL Certificates

-   Execute PostgreSQL Backup (execute on a regular schedule)

Operating System
----------------

The operating system that hosts the IML software must be deployed in a
consistent and repeatable manner. For Red Hat Enterprise Linux and
derivative operating systems, template-driven provisioning using
Kickstart has proven to be reliable and straightforward to audit.
RHEL-based operating systems generate a Kickstart template during the
normal, media-based installation process and this can be a very
effective starting point for developing a fully automated installation
process.

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

Operating system requirements are covered in this guide under [Manager
Server Requirements](ig_ch_03_building.md/#manager-server-requirements). The following
example Kickstart template describes a basic platform with a small set
of packages and two network interfaces: one for provisioning the OS and
connection to external infrastructure, and the other for connection to
the Integrated Manager for Lustre* software management network.

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
rootpw --iscrypted xyzzy
firewall --disabled
selinux --disabled
authconfig --enableshadow --passalgo=sha512
timezone --utc America/New\_York
bootloader --location=mbr --driveorder=vda --append="crashkernel=auto
console=ttyS0,115200 rd\_NO\_PLYMOUTH"
zerombr
clearpart --all --initlabel --drives=vda
autopart
repo --name="CentOS" --baseurl=http://10.0.1.1/CS6.8/ --cost=100
%packages
@core
@base
%end
```


Kickstart templates are flexible and powerful, and can be extended with
the addition of pre- and post-install scripts. With a modest amount of
effort, the entire operating system installation can be fully automated.

### Host Name Resolution

The hosts database /etc/hosts often contains the names and IP addresses
of all of the assets managed by the manager software; include a copy of
this file in the operating system manifest. The file /etc/resolv.conf
contains the list of DNS name servers in use on the network; include a
copy of this file in the manifest as well.

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

### Integrated Manager for Lustre* software

The Integrated Manager for Lustre* software is distributed with an
installation program that makes deployment straightforward, predictable,
and repeatable. The installer works to automatically resolve any
software package dependencies, and also initializes the platform and
configures essential services, such as the PostgreSQL database used for
recording information, and the RabbitMQ messaging system.

To support the restoration of the Integrated Manager for Lustre* software,
be sure to regularly back-up the PostgresSQL database. This
is necessary because the database persistently records Manager
for Lustre\* software configuration information.

Also, be sure to archive the SSL certificates generated during the
installation process. With these two items, along with the original
software distribution, one can reliably recover a manager server
instance to working condition after data loss, or replace an irrevocably
damaged manager server with a new platform, quickly and with minimal
disruption.

To minimize data loss due to loss of a manager server instance, database
backups must be run on a regular schedule and be captured to a
persistent storage target that is external to the Integrated Manager for
Lustre* software server itself. The interval between backups determines the
level of risk of data loss. We strongly recommend that a point-in-time
backup is taken directly after completing any major change management
activity, such as adding new servers or file systems.

Creating a Backup Manifest for the Integrated Manager for Lustre* software Server
-----------------------------------------------------------------------

This section provides a subset of the information required to rebuild a
server from the base operating system install. We do not cover OS
installation here. Instructions in this section are executed as the root
superuser on an example server configuration, for the purposes of
demonstration. Procedures for copying the resulting data off the manager
server to a reliable medium are not given, but can be achieved with a
simple secure copy (e.g., scp) from the source to a destination system
or an integrated enterprise backup platform.

### Network Configuration Files


```
mkdir -p $HOME/backup/etc/sysconfig

cp -a /etc/sysconfig/network /etc/sysconfig/network-scripts/ifcfg-* 
$HOME/backup/etc/sysconfig/.

cp -p /etc/hosts $HOME/backup/etc/.

cp -p /etc/resolv.conf $HOME/backup/etc/.

cp -p /etc/nsswitch.conf $HOME/backup/etc/.
```


### YUM Configuration


```
mkdir -p $HOME/backup/etc

cp /etc/yum.conf $HOME/backup/etc/.

cp -a /etc/yum.repos.d/* $HOME/backup/etc/.
```


### User Configuration


```
mkdir -p $HOME/backup/etc

cp -p /etc/passwd $HOME/backup/etc/.

cp -p /etc/shadow $HOME/backup/etc/.

cp -p /etc/group $HOME/backup/etc/.

cp -p /etc/gshadow $HOME/backup/etc/.

cp -p /etc/sudoers $HOME/backup/etc/.
```


### SSH Host keys (Optional)

SSH creates a set of host keys to identify computers. These are
automatically generated the first time that the OpenSSH service is
started on a computer and change every time that the operating system is
re-installed or if the original host keys, stored in the /etc/ssh
directory, are deleted. Changing the host key effectively changes the
identity of the computer and breaks any trust that has already been
established between other computers on the network. In general, this is
a desirable feature and can protect systems from server spoofing attacks
(e.g. man-in-the-middle attacks). However, when restoring a server to
production, consider restoring the original credentials of the host as
well. Keep in mind that the backup must be protected from compromise in
order to prevent the SSH key pair from being misappropriated.
Accordingly, this step is optional, but it can be useful if one wants to
re-create the original server as closely as possible.


```
mkdir -p $HOME/backup/etc/ssh

cp -p /etc/ssh/ssh_host*key* $HOME/backup/etc/ssh/.
```


### SSH user keys (Optional)

Integrated Manager for Lustre* software has several mechanisms available
for establishing trust between itself and the servers that it manages.
One of the most common mechanisms used during server discovery, is to
create a passphrase-less SSH public/private key pair for the root
super-user account and distribute the public key to the root user
account on all of the servers that will be managed by the manager
software. Loss of the private key stored on the manager server means
that the SSH key-pair will need to be regenerated and the public key
redistributed to all hosts.

For RSA keys:


```
mkdir -m 0700 -p $HOME/backup/root/.ssh

cp -p /root/.ssh/id_rsa* $HOME/backup/root/.ssh/.
```


For DSA keys:


```
mkdir -m 0700 -p $HOME/backup/root/.ssh

cp /root/.ssh/id_dsa* $HOME/backup/etc/root/.ssh/.
```


As with the SSH host keys, this practice is not generally recommended
because the backup must be protected from compromise in order to prevent
the SSH key pair from being misappropriated. In any case, be aware that
if the IML server is lost, the SSH keys will need to be either recovered
or regenerated and the public keys redistributed to all targets.

### NTP Configuration

The Integrated Manager for Lustre* software installation program will
generate an NTP configuration file. After installation completes, create
a backup of the resulting file:


```
mkdir -p $HOME/backup/etc

cp /etc/ntp.conf $HOME/backup/etc/.
```


### Integrated Manager for Lustre* software SSL Certificates

Integrated Manager for Lustre* software uses SSL certificates to
establish trusted communications between the manager server (running the
Integrated Manager for Lustre* software GUI) and the agents running
Integrated Manager for Lustre* software, including the metadata servers,
object storage servers, etc. Without these certificates, trust cannot be
established and the Integrated Manager for Lustre* software will not be
able to manage or receive monitoring telemetry from those agents.

The SSL certificates are generated by the Integrated Manager for Lustre* software
installation program and are re-generated each time the installer is
run. The SSL certificates are randomly generated, so no two sets of keys
are the same. To support successfully restoring Integrated Manager for Lustre*
software and restoring communication with the agents, create a
backup of the following certificate files located on the manager server.


```
mkdir -p $HOME/backup/var/lib/chroma

cp /var/lib/chroma/authority.crt ~/backup/var/lib/chroma/.

cp /var/lib/chroma/authority.pem ~/backup/var/lib/chroma/.

cp /var/lib/chroma/authority.srl ~/backup/var/lib/chroma/.

cp /var/lib/chroma/manager.crt ~/backup/var/lib/chroma/.

cp /var/lib/chroma/manager.pem ~/backup/var/lib/chroma/.
```

### Integrated Manager for Lustre* software Database

Integrated Manager for Lustre* software employs a PostgreSQL RDBMS to
record configuration data and file system telemetry for all Lustre
servers connected to the manager server. Data collection is continuous
and regular backups of the database are required in order to be able to
exact a point-in-time recovery of the manager server with minimal loss
of data. The interval between backups represents the potential risk in
terms of lost data.

The PostgreSQL project offers detailed information on different backup
strategies. Presented here is the simplest and in many ways most
reliable mechanism for capturing a consistent backup of the databases
managed by PostgreSQL. The approximate command, when executed as the
root superuser on a RHEL or CentOS based operating system is:


```
mkdir -p $HOME/backup

su - postgres -c "/usr/bin/pg_dumpall --clean" | /bin/gzip >
$HOME/backup/pgbackup-`date +\%Y-\%m-\%d-\%H:\%M:\%S`.sql.gz
```


Note that while the command is executed as root, the database backup
program is in fact run as the PostgreSQL superuser, called postgres. The
/bin/su command creates a sub-shell that is owned by the postgres user
and is then used to run /usr/bin/pg\_dumpall. The pg\_dumpall command
creates a complete backup of the structure and content of every
PostgreSQL database on the server and records the output as a set of SQL
commands. The resulting text file can be compressed for more efficient
storage. Note that the --clean flag supplied to the pg\_dumpall command
will add instructions to drop any existing structures in the target
PostgreSQL instance upon restore. In other words, the PostgreSQL
instance will be completely over-written during a restore of the
database from this backup.

**Caution**: It may be tempting to omit the --clean flag from the backup
process, but this will complicate the restore process and *may lead to
an inadvertent corruption of the target*. Therefore, always use the
--clean flag when taking a full backup of the Integrated Manager for 
Lustre* software database.

The above command can be added to cron so that it runs on a regular
schedule. Each backup copy will have a unique date and time stamp, down
to the resolution of one second.

Over time, the backup file can get large and may eventually exceed the
single file size limit for the underlying file system. One can work
around this limitation by feeding the output into the split command.

For other database backup strategies and discussions on the merits of
the different approaches, refer to the PostgreSQL project documentation.

Restoring the Integrated Manager for Lustre* software Service
---------------------------------------------------------

Most of the effort expended in developing a recovery strategy for IT
services is focused on the backup procedure described previously.

**Note**: It is important to identify all of the configuration items and
data sets that need to be backed up and to develop a robust
infrastructure and processes to support the backup. It is also important
to test these processes and routinely audit the methods and mechanisms
for correctness.

If all is well with the backup mechanism, then the recovery of a given
service is a relatively straightforward proposition. The easier one can
make the process of recovering a service into production, the more
effective and reliable that process is likely to be. As much as is
possible, one wants to streamline the server provisioning and recovery
steps so that manual interaction is reduced to the minimum required for
success. The goal is to reduce time required to restore, reduce
non-conformance and error, and increase reliability.

If the backup mechanism is reliable and complete, the recovery process
should be straightforward.

### Re-install OS and Restore System Configuration

This process is essentially the same as that used to originally
provision the manager server, with additional steps to recover the
database and SSL certificates. The server hardware and operating system
should conform closely to the requirements under [Manager Server
Requirements](ig_ch_03_building.md/#manager-server-requirements). Network connections,
localization, user accounts, etc., should all be established as before
the server/services failure. It is essential to ensure that the manager
server is functionally identical to the original instance. As discussed
in [Operating System](#operating-system), template-driven
automated provisioning platforms such as Kickstart are very effective
ways to implement consistent operating system deployment.

### Re-install Integrated Manager for Lustre* software

There is no automated installer for the Integrated Manager for Lustre*
software but it is fortunately straightforward to re-run the
installation program. This has the added benefit of guaranteeing that
the core infrastructure is correctly installed and configured and that
all package dependencies are appropriately satisfied. Re-running the
installation program creates a new, unpopulated, instance of the
Integrated Manager for Lustre* software. Note that it does not matter
what answer you provide to the questions asked by the installation
program; this information will be overwritten when the database backup
is restored.

When installation completes, shutdown the Integrated Manager for Lustre*
software and its related services immediately, but keep the PostgreSQL
database server running:


```
service rabbitmq-server stop

service chroma-supervisor stop

service httpd stop
```


**Caution**: Do not conduct any further configuration of
Integrated Manager for Lustre* software. Do not attempt to re-discover Manager
for Lustre\* assets or add any servers or storage to the instance until
the recovery is complete and the Integrated Manager for Lustre* software
installation is verified as working to your satisfaction.

### Restore the NTP Configuration

Restore the backup of /etc/ntp.conf and restart NTP:


```
cp $HOME/backup/etc/ntp.conf /etc/ntp.conf

service ntpd restart
```


### Restore the Integrated Manager for Lustre* software SSL certificates

The following commands must be run after the initial installation
program has been run; otherwise, the SSL certificates will be
overwritten.

/bin/cp \~/backup/var/lib/chroma/authority.crt /var/lib/chroma/.

/bin/cp \~/backup/var/lib/chroma/authority.pem /var/lib/chroma/.

/bin/cp \~/backup/var/lib/chroma/authority.srl /var/lib/chroma/.

/bin/cp \~/backup/var/lib/chroma/manager.crt /var/lib/chroma/.

/bin/cp \~/backup/var/lib/chroma/manager.pem /var/lib/chroma/.

### Restore the PostgresSQL Database

Run the restore command for PostgresSQL, assuming that the backup was
created using the `pg\_dumpall` command as described in "Creating a Backup
Manifest [– Integrated Manager for Lustre* software
Database](#manager-for-lustre-database)". Warning, this command
will erase all existing database content:

`zcat \~/backup/pgbackup-\*.sql.gz` | `su - postgres -c "psql postgres"`

The following errors, usually encountered at the beginning of the
restore output, can be ignored:

ERROR: current user cannot be dropped

...

ERROR: role "postgres" already exists

### Restart Integrated Manager for Lustre* software

When the PostgreSQL database restore has completed, restart the services
that were shut down:

```bash
service rabbitmq-server start

service httpd start

service chroma-supervisor start
```

Alternatively, reboot the Integrated Manager for Lustre* software server. The
service will restart automatically.

### Potential Issues

#### Internal Server Error Reported by Browser on Connection to the Integrated Manager for Lustre* software GUI

After the restore is complete and the services have been started, the
Integrated Manager for Lustre* software may report the following error
when an attempt is made to connect through the client browser:

> **Internal Server Error**
>
> The server encountered an internal error or misconfiguration and was
> unable to complete your request.
>
> Please contact the server administrator, root@localhost and inform
> them of the time the error occurred, and anything you might have done
> that may have caused the error.
>
> More information about this error may be available in the server error
> log.
>
> **Apache/2.2.15 (CentOS) Server at localhost Port 8001\
> **

If this occurs, log into the IML server and remove the following file:

/var/log/chroma/client\_errors.log

The browser interface should now return to normal after refreshing the
page.

#### Graph Data Missing After Restore

It has been noticed that occasionally, after a complete restore of the
Integrated Manager for Lustre* software server, some of the data points may not be
updated. One of the obvious symptoms of this is the graphs on the
Integrated Manager for Lustre* software dashboard may display as blank, without
data, even when the file system is known to be busy. Similarly, OST
capacity may be incorrectly reported.

This is caused by one or more of the Integrated Manager for Lustre* software
client agents losing contact with the manager and refusing to reconnect
after the service has been restored. To restore the connection, log into
the affected Integrated Manager for Lustre* software asset (e.g., the MDS or OSS) and
restart the client agent service as follows. This is a one-time fix.

```
service chroma-agent restart 
```

[Top of page](#1.0)