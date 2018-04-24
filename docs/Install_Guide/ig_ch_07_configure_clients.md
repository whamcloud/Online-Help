# <a name="1.0"></a>Configuring Clients 

[**Software Installation Guide Table of Contents**](ig_TOC.md)

**In this Chapter:**

- [Client Requirements](#client-requirements)
- [Installing Intel® Manager for Lustre* software on Clients Running RHEL or CentOS](#installing-manager-for-lustre-software-on-clients-running-rhel-or-centos)


A client (compute node) accessing a storage appliance must be running
Intel® Manager for Lustre* software {{site.version}} client software. The Lustre* file system
must first be created or discovered at the Intel® Manager for Lustre* software
dashboard (see the Intel® Manager for Lustre* software Online Help to do this).
The Lustre* client software must be installed on the client, and then the
Lustre* file system can be mounted on the client as described in the
Online Help.

Client Requirements 
--------------------

Each file system client must be running Red Hat Enterprise Linux (RHEL)
or CentOS Linux, version {{site.centos_version}}.

**Notes**:

-   Before using the Red Hat or RHEL software referenced herein, please refer to Red Hat’s website for more information, including without limitation, information regarding the mitigation of potential security vulnerabilities in the Red Hat software.

LNET provides the client network infrastructure required by the Lustre*
file system and LNET must be configured for each client. See [LNET Configuration](ig_ch_04_pre_install.md/#lnet-configuration).

Installing Intel® Manager for Lustre* software on Clients Running RHEL or CentOS
--------------------------------------------------------------------------------

The following instructions detail how to install and configure client
software.

The following Lustre* packages are installed on clients:

|Package|Description|
|---|---|
|`lustre-client-modules-<ver>`|Lustre* module RPM for clients.|
|`lustre-client-<ver>`|Lustre* utilities for clients.|

**To configure a Lustre* client running RHEL or CentOS version {{site.centos_version}},
perform these steps:**

1.  For clients running RHEL or CentOS version {{site.centos_version}}, add a client
    repository with the following command.

    ```
        # yum-config-manager --add-repo=
        https://<command_center_server>/client/7
    ```


2.  This will create a file in /etc/yum.repos.d named ```<\server.fqdn>_client.repo```(e.g. foo.bar.baz_client.repo)

3.  Edit the generated file <server.fqdn>\_client.repo and add the
    following lines at the end of the file:

    ```
        sslverify = 0
        gpgcheck = 0
    ```

    Then save and close.

4.  Install the required Lustre* packages on each client:

    a.  Enter (on one line):

    ```
    # yum install lustre-client-modules-{{site.lustre_version}}.<arch>.rpm
    ```

    b.  Update the bootloader (grub.conf or lilo.conf) configuration file as
    needed.

    **Note**: Verify that the bootloader configuration file has been updated with an entry for the new kernel. Before you can boot to a  kernel, an entry for it must be included in the bootloader configuration file. Often it is added automatically when the kernel RPM is installed.

1.  Launch Intel® Manager for Lustre* software and login as
    administrator. Go to the manager GUI to obtain mount point
    information:


    a.  Go to **Configuration > File Systems.**

    b.  In the table listing available file systems, click the name of the
    file system to be accessed by the client. A page showing file system
    details will be displayed.

    c.  Click **View Client Mount Information**. The mount command to be
    used to mount the file system will be displayed as shown in this
    *example*:


    ```
mount -t lustre 10.214.13.245@tcp0:/test /mnt/test
```


1.  On the client, enter the mount command provided.

[Top of page](#1.0)