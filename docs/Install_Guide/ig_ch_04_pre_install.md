# <a name="1.0"></a>Pre-Installation Tasks

[**Software Installation Guide Table of Contents**](ig_TOC.md)

**In this Chapter:**

* [What Not to Do](#what-not-to-do)
* [LNET Configuration](#lnet-configuration)
* [Server Configuration](#server-configuration)
* [Client Requirements](#client-requirements)
* [Linux\* Kernel Rebuilds and Patches](#linux-kernel-rebuilds-and-patches)
* [Firewall Considerations](#firewall-considerations)

## What Not to Do

Please do _not_ perform the following tasks, as these tasks (among
others) are performed automatically, or will conflict with the software:

* Do **not** configure IP addresses for the crossover cable interfaces (server to target).
* Do **not** install or configure Lustre, Corosync, or Pacemaker. Install Integrated Manager for Lustre software only as described in this guide.
* Do **not** configure NTP on storage servers.
* Do **not** install CMAN (Cluster Manager) or other packages that use the Red Hat fence agents. Integrated Manager for Lustre software will have package conflicts. Remove all such packages from all systems.

## LNET Configuration

LNET provides the client network infrastructure required by the Lustre
file system. It supports many commonly used network types such as
InfiniBand and Ethernet.

Basic LNET configuration can be performed using the Integrated Manager for Lustre software GUI.
This is done before creating the Lustre file system. In
this early version of GUI-based LNET configuration, it is intended that
the file system will exist on a _single_ LNET and that all servers and
clients are on this LNET. In this case, you can perform LNET
configuration from the GUI and the configuration information is saved in
a reserved file called
/etc/modprobe.d/iml_lnet_module_parameters.conf. Do not manually edit
this file. Simply follow the instructions in the Integrated Manager for Lustre software Help.

If you wish to configure more advanced features (such as routes and IP
networks), then you should do this manually, in a separate file
contained in the /etc/modprobe.d directory. Please see the configuration
guide _Configuring LNet Routers for File Systems based on Integrated Manager for Lustre_ software*
and also see the Lustre Operations Manual, Chapter 9

* Configuring Lustre Networking*:
  [https://build.hpdd.intel.com/job/lustre-manual/lastSuccessfulBuild/artifact/lustre_manual.xhtml#dbdoclet.50438216_15201](https://build.hpdd.intel.com/job/lustre-manual/lastSuccessfulBuild/artifact/lustre_manual.xhtml#dbdoclet.50438216_15201)

## Server Configuration

The following are pre-installation configuration requirements for
servers. These requirements apply to ALL servers unless specifically
noted.

**Note**: If you are installing Lustre on servers that have been
previously configured as ZFS file system servers, first re-provision all
servers with the correct, supported operating system. Then install
Lustre as described herein. _Any existing file system data will be
lost_.

1.  Red Hat Enterprise Linux or CentOS Linux version {{site.centos_version}} must be
    installed. All servers should be running the same OS and version.

    * Do **not** install CMAN (Cluster Manager) or other packages that use
      the Red Hat fence agents. Integrated Manager for Lustre software will
      have package conflicts. Remove all such packages from all systems.

1.  For servers running Red Hat Linux, each server must be registered
    with RHN (Red Hat Network) and have the optional channel installed.
    Following is one example of how to accomplish this. Please reference
    your site instructions for more information.

    ```bash
    subscription-manager register --autosubscribe\
    --username=\$redhat\_register\_user\
    --password=\$redhat\_register\_password
    yum -y install yum-utils
    yum-config-manager --enable rhel-7-server-optional-rpms
    ```

1)  Next, you will need to configure hostname resolution of all Lustre
    nodes, on each Lustre node. Dynamic hostname resolution (DNS) can be
    used to perform this step. If DNS is not being used, you can perform
    this manually as follows:

    a. Set useful hostnames and ensure you have a functioning `/etc/hosts`
    file. Give each server a unique name, such as manager, mds1, mds2,
    oss1 and oss2. You should be able to `ping <hostname>` and ssh
    freely between systems (dependent on a functional `/etc/hosts` file).
    b. An `/etc/hosts` file might have something like this in it when
    complete:


    ```
    10.0.0.101 manager
    10.0.0.102 ost1
    10.0.0.103 mds1
    10.0.0.104 mds2
    10.0.0.105 ost2
    ```

1.  Copy your `/etc/hosts` file to all servers.

1.  Use ssh-copy-id to copy your ssh public key to each server so that
    your servers are able to ssh into each other without having to enter
    a password.

1.  Yum needs to be functional, with any needed proxies, and default yum
    repositories must be fully configured. Run `yum update` to verify that
    yum updates occur successfully. `yum search vim` will reveal if you
    cannot connect to your configured repositories.

1.  Ensure that NTP is not running on any system. Integrated Manager for Lustre software
    will manage NTP.

1.  Ensure that ssh root access `ssh -l root <hostname>` works
    from the server that will be hosting the Integrated Manager for Lustre software
    dashboard, to all other file system servers.

1.  Properly configure the firewall to allow access to your
    distribution’s yum repositories and any external NTP service. You
    should also be able to ssh between the Lustre servers and the
    manager server without having to enter a password.

**Note**: If a storage node (a Lustre
server) is to be used as a metadata server (MDS), to properly enforce
Lustre file permissions, the MDS _must have access_ to the same UID/GID
database as the Lustre clients. For example, if the Lustre clients are
using LDAP to provide network-wide user account information, the MDS
must be configured to check LDAP for user account information. If a pair
of nodes has been configured as HA peers for an MDT, LDAP must be
configured on both nodes to ensure proper functionality in the event of
a failover.

**Note**: Non-root users should be prevented from logging into storage
nodes.

## Client Requirements

A client accessing your Lustre file system (created with Manager
for Lustre software) must be running Integrated Manager for Lustre software {{site.version}}
client software. See [Configuring Clients](ig_ch_07_configure_clients.md) for
instructions on installing software and configuring clients.

LNET provides the client network infrastructure required by the Lustre
file system and LNET must be configured for each client. See [LNET
Configuration](#lnet-configuration).

## Linux\* Kernel Rebuilds and Patches

The installation of Integrated Manager for Lustre software will replace your
existing Linux\* kernel on all servers.

## Firewall Considerations

Integrated Manager for Lustre software runs on
servers running RHEL or CentOS, version {{site.centos_version}}. The *firewalled* package
needs to be installed and configured for *all file system servers
before* installing Integrated Manager for Lustre software. The Integrated Manager for
Lustre software installation process will then modify the firewall
configuration as needed for Integrated Manager for Lustre software to operate.

[Top of page](#1.0)
