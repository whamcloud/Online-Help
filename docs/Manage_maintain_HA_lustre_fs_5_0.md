# <a id="5.0"></a>Managing and Maintaining HA Lustre file systems

**Warning:** After you have created a Lustre file system using Intel® Manager for Lustre* software, you should not make any configuration changes outside of Intel® Manager for Lustre* software, to file system servers, their respective targets, or network connectivity. Doing so will likely defeat the ability of Intel® Manager for Lustre* software to monitor or manage the file system, and will make all or portions of the file system unavailable to clients.

Before performing any upgrades or maintenance on a primary HA server, all file system targets attached to that server must be manually failed over to the secondary server, using the Intel® for Manager Lustre* software. DO NOT independently shut the server down. 

In addition to the links below, see [Advanced topics](Advanced_Topics_10_0.md/#10.0).

- <a href="#5.1">Increase a file system's storage capacity</a>
- <a href="#5.2">Add an object storage target to a managed file system</a>
- <a href="#5.3">Start, stop, or remove a file system</a>
- <a href="#5.4">Start or stop an MGT, MDT, or OST</a>
- <a href="#5.5">Remove an OST from the file system</a>
- <a href="#5.6">Perform a single target failover from primary to secondary server</a>
- <a href="#5.7">Perform a single target failback from secondary to primary server</a>
- <a href="#5.8">Failover all targets from a primary to a secondary server</a>
- <a href="#5.9">Handling network address changes (updating NIDs)</a>
- <a href="#5.10">Reboot, power-off, or remove a server</a>
- <a href="#5.11">Reconfiguring Corosync and Pacemaker for a server</a>
- <a href="#5.12">Reconfiguring NIDs for a server</a>
- <a href="#5.13">Decommission a server for an MGT, MDT, or OST</a>
- <a href="#5.14">Removing an unwanted server profile</a>


## <a id="5.1"></a>Increase a file system's storage capacity

Perform the following procedures to increase a file system's storage capacity. This section applies to managed, high-availability file systems. For instructions on increasing the capacity a monitored file system, see [Detect and monitor existing Lustre file systems](Detect_and_monitor_existing_LFS_7_0.md/#7.0).

**Add a storage server**

Adding another storage server may not be necessary if storage servers already present can accept additional OSTs. Remember that in HA systems, each OST is served by a primary and a failover server.

Perform the following procedures to add a storage server. 

- Configure a storage server
- Configure primary and failover servers (required for HA)
- Add power distribution units (required for HA)
- Assign PDU outlets to servers (required for HA)

**Add an Object Storage Target**

See <a href="#5.2">Add an Object Storage Target</a> for instructions to add targets/volumes. Each target must already be connected to its server (or two servers in HA configurations).


## <a id="5.2"></a>Add an object storage target to a managed file system

To add another object storage target:

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. In the file system table displayed, *click on the file system name* to display the file system window.
1. Under *Object Storage Targets*, click **+ Create new OST**.
1. Each available target device is displayed, with its Capacity, Type, HA-status, and server pair, if configured. Select the OST or OSTs to be added and click **OK**. The new OSTs will be displayed in the table of OSTs for the file system. 
**Note:** Intel® Manager for Lustre* software will automatically assign OST indices in a distributed fashion across servers to permit striping. 


## <a id="5.3"></a>Start, stop, or remove a file system

**To start a file system: **

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**. 
1. In the table entry for the file system, on the far right, click the **Actions** drop-down menu and click **Start**. The metadata and object store targets are started, enabling the file system to be mounted by clients.

**To stop a file system:**

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**. 
1. In the table entry for the file system, on the far right, click the **Actions** drop-down menu and click **Stop** to stop the metadata and object store targets. This action makes the file system unavailable to clients. Click **Confirm** to complete this action. 

**To remove a file system from the manager:**

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**. 
1. To remove a file system, in the table entry for the file system, click the **Actions** drop-down menu and click **Remove**. File system contents will remain intact until volumes are re-used in another file system. Click **Confirm** to complete this action. 



## <a id="5.4"></a>Start or stop an MGT, MDT, or OST

To start or stop a target: 

1. At the menu bar, click the Configuration drop-down menu and click File Systems.
1. In the File System column, click the name of the file system in which the target is located. The file system window is displayed.
1. Under Management Target, Metadata Target or Object Storage Targets, locate the target name in the first column. 
1. At the far right, click the Actions drop-down menu and click Start or Stop for that target. Note that Stop is only available if the server is running; Start is only available if the server is stopped. Click Confirm to complete this action. 

**Notes:**

- When an MGT is stopped, clients are unable to make new connections to file systems using the MGT, but the MDT and OSTs stay up if they are currently running.
- When an MDT is stopped, the file system becomes inoperable until the MDT is started again.
- When an OST is stopped, clients are unable to access the files stored on this OST. Other OSTs on other servers are not affected.


## <a id="5.5"></a>Remove an OST from a file system

To remove an OST from a file system: 

**Caution:** 
Upon removing an OST from a file system, the OST is no longer visible in the manager GUI. **When an OST is removed, files stored on the OST are no longer accessible**. To preserve data, manually create a copy of the data elsewhere before removing the OST.

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. In the *File System* column, click the name of the file system in which the target is located. The file system window is displayed.
1. Under *Object Storage Targets*, locate the target name in the first column. 
1. At the far right, click the **Actions** drop-down menu and click **Remove**. Click **Confirm** to complete this action.


## <a id="5.6"></a>Perform a single target failover from primary to secondary server

To force a manual failover of a storage target from its primary server to its secondary server, perform these steps: 

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. Select the file system to be modified.
1. In the entry for the target to be failed over, click the **Actions** drop-down menu and select **Failover**. 

**Note:** The Failover button will be displayed only for targets that are configured for failover.

To initiate failover of a target from its primary server to its secondary server using the command line interface (CLI), enter:
```
$ chroma target-failover <target name, e.g. lustre-OST0000>
```


## <a id="5.7"></a>Perform a single target failback from secondary to primary server

To force a manual failback of a target to its primary server, perform these steps: 

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. Select the file system to be modified.
1. In the entry for the target to be failed back, click the **Actions** drop-down menu and select **Failback**.

**Note:** The Failback button will be displayed only for targets that are configured for failover and have failed over from a primary server.

To initiate failback of a target using the CLI, enter:

```
$ chroma target-failback <target name, e.g. lustre-OST0000>
```


## <a id="5.8"></a>Intentionally failover of all targets from a primary to a secondary server

**Warning:** After you have created a Lustre* file system using Intel® Manager for Lustre* software, you should not normally make any configuration changes outside of Intel® Manager for Lustre* software, to file system servers, their respective targets, or network connectivity. Doing so will diminish or defeat the ability of Intel® Manager for Lustre* software to monitor or manage the file system, and will make all or portions of the file system unavailable to clients. 

The following process is recommended only if the affected server has become unresponsive to commands and must be powered down or power cycled in order to perform recovery. This requires that you first failover all connected targets from the affected server to the secondary server.  

Under normal circumstances, where the server is otherwise responsive, use the method described in the previous section (<a href="#5.7">Perform a single target failback from secondary to primary server</a>) to failover the targets before removing power from the host.

To manually failover all targets from a primary to secondary server, perform these steps: 

1. At the menu bar, click the **Configuration** drop-down menu and click **Servers**.
1. For the primary server on which you want to perform maintenance, click the **Actions** drop-down and select **Power-Off**. Note that this action is visible only if PDUs have been added and outlets assigned to servers. This action will switch power off for this server. Any targets running on the primary server will be failed-over to the secondary server. Non-HA-capable targets (targets not supported by a secondary server) will be unavailable until power for the server is switched on again. 


## <a id="5.9"></a>Handling network address changes

File system targets use a network address or network ID (NID) to refer to the server with which they are associated. A storage server NID may change if the network connecting the storage servers and clients is modified. If a server NID changes, the server NID record in the manager must be updated.

**Note:** The manager software detects and displays an alert “NIDs changed on server %s” for each server on which the NID has changed. 

**Caution:** This procedure stops the file system and erases the configuration logs so that they will be regenerated when the servers are restarted.

To prompt the manager software to detect new NIDs and update file system targets:

1. At the menu bar, click the **Configuration** drop-down menu and click **Servers**.
1. Click **Re-write target configuration**.
1. A new column appears on the far right: *Select Server*. All servers are selected by default. Select the servers for which you want to rewrite NIDs. Then click **Re-write Target Configuration**.
1. The manager queries the network interfaces on the storage servers. Each target is updated with the current NID for the server with which it is associated. To check that the manager has detected the correct NID for a server, click the *Hostname* of the server to display a detailed view of the server. Scroll down to the NID Configuration section to view the network interface, IP Address, driver, and network for each NID.

You can also directly edit the NID configuration for a server, but to do this, the server cannot belong to an existing Lustre file system. See [NID Configuration](Graphical_User_Interface_9_0.md/#9.3.1.1).

**WARNING:** For Lustre* file systems created and managed by Intel® Manager for Lustre* software, the only supported command line interface is the CLI provided by Intel® Manager for Lustre* software. Modifying such a Lustre file system manually from a UNIX shell will interfere with the ability of Intel® Manager for Lustre* software to manage and monitor the file system. 

Lustre commands can, however, be used to manage metadata or object storage servers in an existing Lustre storage system that has been set up outside the manager and is being monitored, *but not managed*, by Intel® Manager for Lustre* software. 


## <a id="5.10"></a>Reboot, power-off, or remove a server

The **Actions** menu on the Server Configuration window let you perform the following commands for any single server. Some commands shown here may not be listed, depending on the state of the server.

- **Reboot**
- **Shutdown**
- **Power off**
- **Power cycle**
- **Remove**
- **Force Remove**

To perform any of these commands:

1. On the Dashboard, click **Configuration > Servers**.
1. For the desired server, at the **Actions** drop-down menu at the right, click the desired command.
1. After clicking on a command, a *Commands* window pops up to reveal the jobs that are run to perform this command, and the command Status shows pending. When each job completes, the command Status then shows *Succeeded*. 


## <a id="5.11"></a>Reconfiguring Corosync and Pacemaker for a server

Pacemaker and Corosync configuration is required for each server if you are creating or expanding a high-availability file system.  Intel® Manager for Lustre* software automatically configures Corosync and Pacemaker for each managed HA server that you add, so that manual configuration of Pacemaker and Corosync should not normally be required. See [Add one or more HA servers](Creating_new_lustre_fs_3_0.md/#3.4). 

An administrator may need to reset or configure Pacemaker or Corosync when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with those services.  See [Pacemaker configuration](Graphical_User_Interface_9_0.md/#9.3.1.1) and [Corosync configuration](Graphical_User_Interface_9_0.md/#9.3.1.1) for more information.


## <a id="5.12"></a>Reconfiguring NIDs for a server

Intel® Manager for Lustre* software automatically configures NIDs for each managed server that you add, so that manual NID configuration should not normally be required. However, an administrator may need to reconfigure NIDs for a server when performing maintenance on a server, altering the server's configuration, or troubleshooting problems network interfaces.  See [NID Configuration](Graphical_User_Interface_9_0.md/#9.3.1.1).


## <a id="5.13"></a>Decommission a server for an MGT, MDT, or OST

**Caution:** When a server for an MGT, MDT or OST, is removed (decommissioned), any file systems or targets that rely on this server will also be removed.

To remove (decommission) a server for an OST:

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. In the *File System* column, click the name of the file system in which the target is located. The file system window is displayed.
1. Under *Object Storage Targets*, locate the target you want to decommission. Click the corresponding *Primary server* or *Failover server* that you want to decommission. 
1. In the dialogue window that opens, click the **Actions** drop-down menu for that server and click **Remove** to remove the server from the file system. Click **Confirm** to perform this action.
1. Click the **Actions** drop-down menu and click **Stop LNet** to shut down the LNet networking layer and stop any targets running on this server. 
1. Click the **Actions** drop-down menu and click **Unload LNet** to stop LNet, if it is running, and unload the LNet kernel module to ensure that it will be reloaded before any targets are started again. (Clicking **Start LNet** will reload the LNet kernel module and start the LNet networking layer again.)

**Note:** To remove the record for the server from the manager without attempting to contact the server, click the **Actions** drop-down menu and click **Force Remove**. Any targets that depend on this server will also be removed without any attempt to unconfigure them. **This action should only be used if the server is permanently unavailable**. 

**Warning:** The **Force Remove** command will remove the server from the Intel® Manager for Lustre* configuration, but not remove Intel® Manager for Lustre* software from the server. All targets that depend on the server will also be removed without any attempt to unconfigure them. To completely remove the Intel® Manager for Lustre* software from the server (allowing it to be added to another Lustre file system), first contact technical support.

**Note:** Each server is also separately listed at **Configuration > Servers**, however the server configuration regarding which file system, target, and HA status is not shown on the *Servers* window.


## <a id="5.14"></a>Removing an unwanted server profile

You may want to remove a custom server profile that is no longer needed. Enter the following commands at the command line interface. Dollar sign prompts have been removed to allow copying and pasting.


```
chroma-config stop
chroma server_profile list  # Pick up the profile name you want to remove
chroma-config profile delete <profile name>
chroma server profile list  # Verify profile is now removed
chroma-config start
```

