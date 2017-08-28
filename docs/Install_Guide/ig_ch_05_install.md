[**Manager for Lustre\* Software Installation Guide Table of Contents**](ig_TOC.md)
# Manager for Lustre\* Software Installation

**In this Chapter:**

- [Installing Manager for Lustre\* software](#installing-intel-ee-for-lustre-software)
- [Manager for Lustre\* Software Configuration Settings](#intel-manager-for-lustre-software-configuration-settings)
- [Editing Manager for Lustre\* Software Configuration Settings](#editing-intel-manager-for-lustre-software-configuration-settings)


This section describes how to install the Manager for Lustre\*
software and the Manager for Lustre\* software on the *manager
server.*

After Manager for Lustre\* and Manager for Lustre\* software is
installed, point your web browser to the Manager for Lustre\*
dashboard. Use Chrome\* or Firefox\*. A display monitor with a minimum
resolution of 1024 X 768 pixels is recommended, to adequately display
the Manager for Lustre\* software GUI.

**Note**: Later, when adding storage servers to your Lustre file system,
the Manager for Lustre\* agent, Manager for Lustre\*
software, and specific dependencies (e.g.: for Corosync and Pacemaker)
are automatically deployed to the storage server. This avoids the need
to manually install the Manager for Lustre\* software on storage
servers and avoids possible errors.

**Note**: Some installations may opt to deploy and configure a Lustre
file system manually, without Manager for Lustre\* software.
Other installations may opt to deploy and configure a Lustre file system
and then later install Manager for Lustre\* software to be used
in Monitor-only mode. The overall release tarball is iml-4.0.0.0.tar.gz.
To deploy and configure Lustre manually, see [Installing and Configuring
Lustre Manually](ig_ch_07_configure_clients.md/#installing-and-configuring-lustre-manually).

For information regarding installing and configuring Lustre, see Part II
of the *Lustre Operations Manual*. This information is available at the
following URL. If this page does not load, copy and paste it into your
browser.

https://build.hpdd.intel.com/job/lustre-manual/lastSuccessfulBuild/artifact/lustre_manual.xhtml#part.installconfig

Installing Manager for Lustre\* software
--------------------------------------------

You will need the following information to perform this installation:

-   The name, email address, and password you wish to use for the first Manager for Lustre\* software superuser. The email address must use an FQDN.
- (Optional) The fully qualified domain name (FQDN) of the NTP server (internal or external) used for your site. If no NTP server is set, the Manager for Lustre\* server's clock will act as the time source for the entire storage cluster.

To install the software, complete these steps:

1.  Download the installation archive to a directory on the manager server (e.g. /tmp).
1. Unpack the installation archive using tar: iml-4.0.0.0.tar.gz:
```
# cd /tmp; mkdir install
# tar –C install –xzf iml-4.0.0.0.tar.gz
```


1. To install the Manager for Lustre\* software, run:
```
# cd /tmp/install/iml-4.0.0.0.tar.gz
# ./install
```


1. When the following prompts appear, enter your parameters for the first superuser of Manager for Lustre\*:

   **Username:** *&lt;Enter the name of the superuser&gt;*
   
   **Password:** *&lt;Enter a password&gt;*
   
   **Confirm password:** *&lt;Enter the password again&gt;*

   **Email:** *&lt;Enter an email address for the superuser&gt;*

   **Note**: Additional Manager for Lustre\* software superusers as well as file system administrators and users can be created in the manager GUI.

   When configuration is complete, a message is displayed indicating the installation was successful.

1.  When the prompt **NTP Server \[localhost\]** appears, respond with **one of these options**:

    -   *Option 1:* To designate the NTP server (internal or external) used for your site, enter the FQDN or IP address of the NTP server and press the **&lt;Enter&gt;** key.

    -   *Option 2:* To use the Manager for Lustre\* software server’s clock as the time source, press the **&lt;Enter&gt;** key.

1.  Using ifconfig, obtain the IP address of the administrative network interface for the server hosting Manager for Lustre\* software. The default network interface for Manager for Lustre\* software is eth0.

2.  Open a web browser and access the Manager for Lustre\* software GUI using the server IP address obtained in the previous step. Enter in the address field of your browser:

https://&lt;command_center_server_IP_address&gt;

**Note**: If the IP address of the server has an associated FQDN, you can connect to the Manager for Lustre\* GUI user interface using:

https://&lt;command_center_server_fqdn&gt;



**Note**: The GUI uses a self-signed SSL certificate to secure
communications between the browser and the server. You will need to
accept this certificate in order to connect to the Intel® Manager for
Lustre\* GUI. A certificate can be downloaded from (example only):

https://&lt;manager-addr&gt;/certificate/

After Manager for Lustre\* software is installed, point your web
browser to the Manager for Lustre\* dashboard. Use Chrome\* or
Firefox\*.

Manager for Lustre\* Software Configuration Settings
-------------------------------------------------------------

The following Manager for Lustre\* software configuration
settings can be modified. See the instructions for modifying these
settings following the descriptions.

**ALLOW_ANONYMOUS_READ**
    
**Default:** True (Uppercase first letter required.)
    
**Description:** Allows anonymous (unauthenticated) users to view statistics, logs and status of a system in the Manager for Lustre\* GUI but not to make any changes. If set to False, anonymous users will be presented with a login prompt and no data.

**DISABLE_POWER_CONTROL_DEVICE_MONITORING**

**Default:** False (Uppercase first letter required.)

**Description:** The default state is False, allowing automatic monitoring of power control devices. When set to True, this setting disables the manager software’s monitoring of your power control devices (eg, BMC, PDU outlets, etc.) This is necessary for sites where the manager server does not have access to the power control devices itself. However, Manager for Lustre\* software will then NO LONGER REPORT ANY FAILURE IN ANY POWER CONTROL DEVICES. If power control becomes non-operational, automatic failover will not occur on failure, and manual intervention will be required to restore service to your file system. If you chose to make this setting to True, we recommend implementing an alternate mechanism to monitor of power control devices, outside of Manager for Lustre\* software.

**Other Settings**:

|Setting|Default|Description|
|---|---|---|
|**```EMAIL\_HOST```**|None|SMTP server hostname (Example: 'server1.test.com')|
|**```EMAIL\_PORT```**|25|SMTP server port number.|
|**```EMAIL\_HOST\_USER```**|' '|SMTP server username (or ' ').|
|**```EMAIL\_HOST\_PASSWORD```**|' '|SMTP server username (or ' ').|
|**```EMAIL\_USE\_TLS```**|False (Uppercase first letter required.)|True indicates that TLS/SSL is to be used. False indicates it is not to be used.|
|**```EMAIL\_SENDER```**|'noreply\@\<command_center server_fqdn>'|The address that appears in the *From* field on alert emails.

### Editing Manager for Lustre\* Software Configuration Settings

To change these configuration settings:

1.  Use a text editor to create or modify a file ```local_settings.py
```in the directory ``` /usr/share/chroma-manager/```

    For example, add the following setting to the ```local_settings.py```
 file to restrict view of system statistics, logs, and status to only users who are logged in:
```
ALLOW_ANONYMOUS_READ=False
```
In this example, the first letter of False must be capitalized.

   **Note**: Entries must follow Python\* syntax rules. For example, all strings must be enclosed in single or double quotes (double quotes must be used if the string includes a single quote). For example, EMAIL\_HOST=server1.test.com will result in an error, while EMAIL\_HOST='server1.test.com' is a valid entry.

   **Warning**: If you edit the file settings.py instead of creating a local\_settings.py file, your changes will be overwritten without warning when the Manager for Lustre\* software is updated.

1.  To configure email alerts, complete one of the options below. By default, email alerts from the Manager for Lustre\* software are disabled (EMAIL\_HOST set to None).

    -   *Option 1: Set up an external mail server.* Create or modify the file\
    /usr/share/chroma-manager/local\_settings.py to provide appropriate values for these settings:

        a.  Set EMAIL\_SENDER to an address suitable for your site.

        b.  Modify EMAIL\_HOST (and other server settings if necessary) to point to an existing SMTP server on your network.

    -   *Option 2: Use a local mail server.* If a suitable SMTP server is not available, you can configure the Manager for Lustre\* software server to act as an SMTP server:

        a.  Set EMAIL\_SENDER to an address suitable for your site.

        b.  Set up a local mail daemon using standard procedures for Red Hat Enterprise Linux or CentOS such as those described in the Red Hat documentation at:
        https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Deployment_Guide/>

        c.  Set EMAIL\_HOST to 'localhost'


1. Run the chroma configuration tool
    in order to effect changes made to ```local_settings.py```.
```
# chroma-config restart
```


For configuring user accounts, see the online Help in the Intel®
Manager for Lustre\* software. The online Help also provides
instructions for creating, monitoring, and managing your Lustre
file systems.