# <a name="1.0"></a>General Troubleshooting

[**Software Installation Guide Table of Contents**](ig_TOC.md)

Consider the following tips before contacting technical support as you
may find this information useful when debugging an issue:

-   Locate the logs in `/var/log/chroma`.

-   If an issue is encountered in the user interface and you have access
    to a JavaScript\* debug console, open the console.

-   If a command has failed, go to *Notifications &gt; Commands* and
    click on the command that failed to display a detailed message.

Troubleshooting information for known issues you may encounter is
provided below. Also, see [Getting Help](ig_ch_16_appD_getting_help.md).

**Problem: When you run chroma-config, a message is displayed that
includes the following: “*Please correct the hostname resolution.*"**

***Solution:*** Verify that hostname resolution is set up correctly
using these commands:

1.  Obtain the IP address for the network interface. The default network
    interface is eth0. Enter (on one line):

    ```bash
    # ifconfig <network\_interface\_name> | grep "inet addr" |\
    awk -F" " {'print \$2'}
    ```

    Use the output of this step in the next step.

1.  Obtain the hostname of the server by entering:

    ```bash
    # getent hosts <network\_interface\_ip\_address>
    ```
    Use the output of this step in the next step.

1.  Obtain the IP address of the server by entering:

    ```bash
    # getent hosts <hostname>
    ```

If all these commands return the same *hostname* and *IP address*, your
hostname server is set up correctly.

***Problem:*** **An error message is displayed after you have modified
the Command Center configuration file local\_settings.py.**

***Solution:*** To find the error, look for a line containing
`local\_settings.py` and check the following text for clues to the
error. In the example below, the value of the configuration setting
ALLOW\_ANONYMOUS\_READ starts with a lower case letter.

> File "/usr/share/chroma-manager/local\_settings.py", line 1, in
> &lt;module&gt;
>
> ALLOW\_ANONYMOUS\_READ=true
>
> NameError: name 'true' is not defined

The correct value True starts with an upper case letter as shown below:

> ALLOW\_ANONYMOUS\_READ=True

Python syntax rules must be followed for configuration settings. For
example, strings must be enclosed in single or double quotes (use double
quotes if the string includes a single quote). For example, the value of
the SMTP server host name defined for EMAIL\_HOST must be enclosed in
single quotes as shown below:

> EMAIL\_HOST='server1.test.com'

***Problem:*** **The time displayed in the Command Center is not
correct.**

***Solution:*** Check the time zone settings of the server and your
browser. The local time displayed in the Command Center user interface
is based on UTC and the time zone settings on both the server and the
browser host.

***Problem:*** **You are unable to manage a storage server from the
Command Center after entering a Lustre* command (such as umount/mkfs) on
the server command line.**

***Solution:*** A storage server cannot be managed using Lustre* commands
on the storage server command line. 

***Problem:* You need to take a server out of service temporarily for a
repair that may involve starting and stopping the server several
times.**

***Solution:*** When you take the server out of service in a system
configured for HA, the Command Center will failover the targets on that
server to its failover server.

After completing the repair and putting the server back in service,
force a manual failback of a target to its primary server, by completing
these steps in the Command Center Manager user interface:

1.  Go to **Configuration** &gt; **File Systems** and select the file
    system to be modified.

2.  In the entry for the target to be failed back, click **Actions**
    menu **Failback** button.

For more details about manually performing failover and failback
operations, see the Intel® Manager for Lustre* software online Help topic,
*Managing storage*.

***Problem:*** **You need to restart cleanly after a power outage to
some, or all, of your cluster.**

***Solution:*** Start the targets that lost power and monitor the alert
next to each target in the Command Center for completion of the recovery
process. Check that failover and failback operations have restored the
original cluster configuration.

***Problem:*** **The Command Center is displaying an alert *“NIDS
changed on server &lt;hostname&gt;”* and your file system won’t
start*.***

***Solution:*** File system targets use a network address or network ID
(NID) to refer to the server they are associated with. A storage server
NID may change if the network connecting the Lustre* servers and clients
is modified. If a Lustre* server NID changes, the server NID record in
the Command Center must be updated.

For a procedure to update server NIDS, see the Intel® Manager for Lustre* software
online Help topic, *Handling network address changes*.

***Problem:*** **You are unable to create or read a file from a client
and a “*Permission denied”* message is displayed.**

***Solution:*** To properly enforce Lustre* file permissions, the MDS
must have access to the same UID/GID database as the Lustre* clients. For
example, if the Lustre* clients are using LDAP to provide network-wide
user account information, the MDS must be configured to check LDAP for
user account information. If a pair of nodes has been configured as HA
peers for an MDT, then LDAP must be configured on both nodes to ensure
proper functionality in the event of a failover.

[Top of page](#1.0)