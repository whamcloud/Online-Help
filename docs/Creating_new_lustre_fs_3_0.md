# <a id="3.0"></a>Creating a new Lustre\* file system

This chapter describes how to create a new Lustre* file system, to be managed from the Intel® Manager for Lustre\*, and how to mount file system clients.  

**Note:** All references herein to the manager refer to the Intel® Manager for Lustre* software.

**Note:** The procedure for creating a Lustre file system *based on ZFS zpools* is different. For that information see [Creating and Managing ZFS-based Lustre file systems](Create_and_manage_ZFS_based_LFS_8_0.md/#8.0).

1. <a href="#3.1">Prerequisites for creating an HA file system</a>
1. <a href="#3.2">Important information about reconfiguring your file system</a>
1. <a href="#3.3">High-availability file system support</a> (overview)
1. <a href="#3.4">Add one or more HA servers</a>
1. <a href="#3.5">Configure primary and failover servers</a>
1. <a href="#3.6">Add power distribution units</a> (alternate to BMC configuration)
1. <a href="#3.7">Assign PDU outlets to servers</a>
1. <a href="#3.8">Assign BMCs to servers</a> (alternate to power distribution units and outlets)
1. <a href="#3.9">Create the new Lustre file system</a>
1. <a href="#3.10">View the file system</a>
1. <a href="#3.11">Mount the Lustre file system</a>


## <a id="3.1"></a>IMPORTANT PREREQUISITES to creating an HA Lustre file system

A high-availability Lustre file system managed by Intel® Manager for Lustre* software requires that your entire storage system configuration and all  interfaces comply with a pre-defined configuration. Intel® Manager for Lustre* software performs LNet configuration assuming that each server is connected to a high-performance data network, which is the Lustre network LNet.  For detailed information, see the section *High Availability Configuration Specification* in the *Intel® Enterprise Edition for Lustre\* Software Installation Guide*. Also see the guide *Lustre\* Installation and Configuration using Intel® EE for Lustre\* Software and OpenZFS*.

**Caution:** When initially setting up your storage system, take care in selecting block device names because these cannot be changed after the file system has been created using  Intel® Manager for Lustre* software. **You should NOT make configuration changes to file system servers or their respective volumes/targets outside of Intel® Manager for Lustre\* software**. Doing so will defeat the ability of Intel® Manager for Lustre* software to monitor or manage the file system, and will make the file system unavailable to clients. Re-labeling these device names during multipath configuration will break the HA configuration established by Intel® Manager for Lustre* software.


## <a id="3.2"></a>IMPORTANT INFORMATION about reconfiguring your file system

**Caution:** When initially setting up your storage system, take care in selecting block device names because these cannot be changed after the file system has been created using  Intel® Manager for Lustre* software. **You should NOT make configuration changes to file system servers or their respective volumes/targets outside of Intel® Manager for Lustre\* software**. Doing so will defeat the ability of Intel® Manager for Lustre* software to monitor or manage the file system, and will make the file system unavailable to clients. Re-labeling these device names during multipath configuration will break the HA configuration established by Intel® Manager for Lustre* software.

**Caution:** A known issue can result in a server being made unavailable. This can happen if the server has been added to a Lustre file system, (using Intel® Manager for Lustre* software) and then the user decides to Force Remove the server from the file system. The Force Remove command should only be performed if the Remove command has been unsuccessful. Force Remove will remove the server from the Intel® Manager for Lustre* configuration, but not remove Intel® Manager for Lustre* software from the server. All targets that depend on the server will also be removed without any attempt to unconfigure them. To completely remove the Intel® Manager for Lustre* software from the server (allowing it to be added to another Lustre file system), first contact technical support.


## <a id="3.3"></a>High-availability file system support

Intel® Manager for Lustre* software includes several capabilities for configuring and managing highly-available Lustre* file systems.

Generally, high availability (HA) means that the file system is able to tolerate server hardware failure without loss of service. The key components of this solution are the software components Corosync and Pacemaker. Corosync is responsible for maintaining intra-cluster control and heartbeat communications, and Pacemaker is responsible for managing HA resources (e.g., Lustre* targets).

To support automatic server failover, each HA server must have a dedicated crossover connection to the other server that will be its HA peer. During file system creation, each HA server is designated as a primary server for one or more targets, and as a failover, peer server for its peer server's targets. This crossover connection is configured as a redundant Corosync communications interface in order to reduce the likelihood of false failover events. Intel® Manager for Lustre* software uses a managed server profile to automatically configure Corosync and Pacemaker. The managed server profile is used to configure primary and failover servers. See the following figure.

<a id="f3.1"></a>
![md_Graphics/lustre-configuration5_zoom40.png][f3.1]

Physically, HA peer servers must be cabled to provide equal access to the pool of storage targets allocated to those peers. For example: server 1 and server 2 are cabled as HA peers. Targets A and B have been configured with server 1 as their primary server and server 2 as their failover server. Targets C and D have been configured with server 2 as their primary server and server 1 as their failover server. If server 1 becomes unavailable, server 2 must have access to the block storage devices underlying targets A and B in order to mount them and make them available to Lustre clients. The end result is that server 1 is powered off and server 2 is now exporting targets A, B, C, and D to Lustre clients. 

To support HA failover, each HA server must be able to automatically power-off its peer server if a failover is required. The process of powering off a faulty server is known as "node fencing" (also called "server fencing"), and ensures that a shared storage device is not mounted by more than one server at a time. Lustre includes protection against multiple simultaneous device mounts, but automatically powering off the faulty server ensures that failover works properly. Intel® Manager for Lustre* software supports the use of remotely-operable Power Distribution Units (PDUs) for this purpose. Alternative to the configuration of PDUs, Intel® Manager for Lustre* software also supports the Intelligent Management Platform Interface (IPMI) and associating baseboard management controllers (BMCs) with servers, to support server monitoring and control.

**Note:** See the *Intel® Manager for Lustre\* Partner Installation Guide* for physical design and configuration guidelines required to support high availability. 


## <a id="3.4"></a>Add one or more HA servers

This procedure adds one or more servers. They may be storage servers, HSM agent nodes, Robinhood policy engine servers, or they may perform another function dictated by a custom server profile. Note that at least two storage servers are required for HA file systems. 

**Note:** All authentication credentials are sent to the manager server via SSL and are not saved to any disk. 

To add a server to be used for the file system:

1. At the menu bar, click the **Configuration** drop-down menu and click **Servers** to display the **Server Configuration** window.
1. Click **+ Add Servers**. 
1. In the *Hostname / Hostlist Expression* field, enter the name of the server(s) to be added. You can enter a range of names, i.e., a "hostlist expression". For example, your can enter server[00-19] to generate a list of up to twenty servers (in this case). **Note:** These are all the server names that your expression expands to and may include servers that don't exist or are not connected to the network. 
1. Select an authentication method:
    - Click **Existing Key** to use an existing SSH private key present on this server. There must be a corresponding SSH public key on each server you are adding.
    - Click **Root Password** and enter a root password for the server you are adding. This is standard password-based authentication. It is not uncommon to use the same root password for multiple servers. 
    - Click **Another Key** and enter a private key that corresponds to a public key present on the server you are adding. If the key is encrypted, enter the passphrase needed to decrypt the private key. 
1. Click **Next**. The software will attempt to verify the presence and readiness of all servers with names matching your hostname entry. Each server is represented by a square. A green square means that the server passed all readiness tests required for validation and this process can proceed for that server. A red square means that the server failed one or more readiness tests. Click on a red square to learn which tests the server failed. You can hover the pointer over the failed validation test to learn more. 
1. For a server that failed validation, log into that server and work to address the failed validation. When the issue has been resolved, the GUI will update the failed validation test in real time, from a red x to green check mark. You can add the server when all failed validations are resolved.

     **Note:** Many server names may be generated from your host list expression, and some of those servers may not exist. A red square is created for each server that doesn't exist. 
1. Assuming that all servers pass the validation tests and all boxes are green, click **Proceed** to download agent software to each server. If one or more servers failed to pass validation tests, the green **Proceed** button changes to a yellow **Override** button. Clicking **Override** displays this warning: *You are about to add one or more severs that failed validation. Adding severs that failed validation is unsupported. Click **Proceed** to continue*. 

    **Caution:** Although you can attempt to add a server that has failed validation, all of the capabilities exercised by the tests are needed for the management software and server to operate normally. The server will likely fail to operate normally if it has failed validation by this software. Adding a server that failed validation is not supported. 
1. After clicking **Proceed**, agent software is deployed to each server and a **Commands** window opens to show progress. At completion, the message *Succeeded* is displayed. Click **Close** to close this **Commands** window.
1. If you decided to override servers that failed validation tests (this is not supported), expand any failed commands in the **Commands** window. Click on any failed jobs and examine the stack trace to learn the cause of the failure. Correct the cause of the failure and close the command and server windows. If the server exists in the server table, click **Actions** and select **Deploy Agent**. Otherwise open the **Add server** dialog and enter the failed server. In either case you should now see a green square for that server and be able to add it without issue.
1. With the **Commands** window now closed, the servers you added are listed as **Unconfigured** on the **Server Configuration** window. The next task is to add a server profile to each server; this step will configure the server for its purpose. For a given server, under the **Actions** drop-down menu, click **Setup server**. 
1. At the *Add Server - Add Server Profiles* window, select the desired profile from the drop-down menu. Note that one profile type is selected for all servers you are adding in this process. The common profiles are listed next, but your software may have more server profiles. 
    - **Managed Storage Server for EL7.2:** As above, this allows the manager GUI to configure Corosync and Pacemaker, configure NTP, etc., so that the manager software can monitor and manage the server. Managed storage servers must be physically configured for high-availability/server failover. This profile is for servers running RHEL 7.2. (In our example below, none of the servers being configuring are running RHEL 7.2, so the warning **Incompatible**, is displayed.)
    - **Monitored Storage Server:** This is for servers that are not correctly configured for HA/failover (as far as this software is concerned). A monitored storage server is monitored only; the manager GUI performs no such server configuration or management. Note that ZFS file systems use this profile. However the Dashboard will still display charts showing file system operations.
    - **POSIX HSM Agent Node:** An HSM Agent node is used in hierarchical storage management to run an instance of Copytool. Copytool transfers certain files between the Lustre file system and the archive and deletes from the Lustre file system those files that have been archived. See [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0)
    - **Robinhood Policy Engine Server:** This server hosts the Robinhood policy engine, which enables automation of hierarchical storage management activities. See [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0).
1. Select the desired profile and click **Proceed**. The manager does an audit of the storage resources on each server. The manager then provisions the server by loading appropriate Lustre modules and making sure the Lustre networking layer is functioning. When all checks are completed, LNet State indicates LNet Up and each server is fully qualified as a Lustre server. Under the Status column, a green check mark is displayed for each new server. If server provisioning does not succeed, the Status will indicate a exclamation mark (!) and the LNet State may indicate Unconfigured. To learn the cause of the problem, click the exclamation mark for the failed server to see Alerts. For more information, click **Status** at the top menu bar. The *Status* window also lets you view related logs.

    **Note:** A certain profile may not be compatible with a server as the server is configured. If the profile you select is not compatible with the server(s) you specified, a warning is displayed: Incompatible. Each incompatible server is represented by a red box. To learn why a server is incompatible, click on a red box. A pop-up window reveals the problem. You can resolve the problem and the red box will change to green, indicating profile compatibility with the server. 

    **Caution:** For servers with incompatible profiles, you have the option of clicking **Override**, however, this is not encouraged or supported. Each server's configuration must be compatible with the selected profile, or the server will likely not function as required for the selected profile. The four available default server profiles are described above. For more information about the POSIX HSM Agent Node and Robinhood Policy Engine Server profiles, see <a href="Config_and_using_HSM_6_0.md/#1.0">Configuring and using Hierarchical Storage Management</a> herein.
1. Click **Close**. This process is complete. For HA file systems, proceed to <a href="#3.5">Configure primary and failover servers</a>. 


## <a id="3.5"></a>Assign primary and failover servers to storage volumes

This section establishes the primary and failover storage servers for each volume, to support-high availability.

**Caution:** Configuring primary and failover servers on the Volumes window does not by itself enable high-availability. Automated failover also requires power management support by PDUs and outlet assignments or by assigning BMCs to servers. See <a href="#3.6">Add power distribution units</a> or <a href="#3.8">Assign BMCs to servers</a>. It is important to remember these server/volume configurations for when configuring power distribution units (PDUs) and outlet-server assignments.

**Note:** This section is for configuring managed storage servers, as previously set up in Add storage servers. This section does not apply to servers that are monitor-only. 
To view the volumes that were discovered and make adjustments to volume configurations, complete these steps: 

1. At the menu bar, click the **Configuration** drop-down menu and click **Volumes** to display the *Volume Configuration* window. A list of available volumes is displayed (if a volume does not contain unused block devices, it will not appear on this list). 
1. The *Volume Configuration* window displays the current primary and failover servers for each volume. If required, you can change these primary and failover server assignments. To do so, for a given volume select the volume's *Primary Server* from the drop-down list. Then select the *Failover Server* from the drop-down list. Changes you make to volume/server configuration appear in blue, indicating that you have selected to change this setting, but have not applied it yet. To undo a change in-process, click the **x**. 
1. Repeat step 2 for each volume that has a primary and failover server. 
1. Click **Apply**. Then click **Confirm**.
    
Changes you select to make on this Volumes Configuration window will be updated and displayed after clicking **Apply** and **Confirm**. Other users viewing this file system's *Volume Configuration* window will see these updated changes after you apply and confirm them. To cancel all changes you have selected (but not yet applied), click **Cancel**. 
    
**Note:** There is currently no lock-out of one user's changes versus changes made by another user. The most-recently applied setting is the one in-force.

Next, proceed to <a href="#3.7">Add power distribution units</a> or <a href="#3.8">Assign BMCs to servers</a>. It is important to remember these server/volume configurations for when configuring power distribution units (PDUs) and outlet-server assignments.


## <a id="3.6"></a>Add power distribution units

This section configures power distribution units (PDUs) and assigns PDU outlets to servers to support high availability (HA).

**Note:** A server cannot be associated with both a BMC and PDU outlets. Use PDUs or IPMI/BMCs to support failover.

**Note:** This section is for configuring managed storage servers, as previously set up in <a href="#3.4">Add storage servers</a>. You should configure PDUs based on <a href="#3.5">primary and failover server configuration</a>, per volume. This section (Add power distribution units) does not apply to servers that are monitor-only. 

**Issues Regarding Power Loss to the BMC or PDU**

Regarding failover, if the method of power control is not functioning (e.g., loss of power to the fencing device, misconfiguration, etc.), then HA will be unable to fail the targets from the failed server to its failover server. This is because in order to complete failover, the failover server needs to be able to guarantee that the failed server can no longer access targets running on it. The only way to be sure of this is to power-down the failed server. Thus, the failover server needs to be able to communicate with the fencing device of the failed server for failover to occur successfully.

With IPMI, the power for each HA server and its fencing device is coupled together. This means there are more scenarios where both may lose power at once (chassis power failure, motherboard failure, etc.). In such a case, if a server suffers chassis power failure such that the BMC is no longer able to operate, HA will be unable to fail the targets over. To remedy this situation, restore power to the chassis of the failed server to restore the functionality of your file system. If HA coverage for the scenarios just described is important to you, we strongly recommend using smart PDUs, rather than IPMI as your fencing device.

For a PDU, power loss to the PDU will mean that HA will be unable to fail the targets over. As in the above situation, the remedy is to restore power to the PDU to restore the functionality of your file system. We recommend redundant PDUs if availability is critical. This approach is a necessary limit of HA to protect the integrity of the targets being failed over.

At the PDUs window you can add PDUs and then assign specific PDU outlets to specific servers. You should have at least two PDUs to support failover. 

To add PDUs:

1. At the menu bar, click the **Configuration** drop-down menu and click **Power Control**.
1. With no power distribution units recognized, this window will read: *No power distribution units are configured*. Click **+ Add PDU**.
1. At the *Add PDU* dialogue window, select the PDU device type from the drop-down list.
1. Enter a name for this PDU. (If not entered, this field will default to the IP address.)
1. Enter the IP address for the PDU. If not known, enter a DNS-resolvable hostname. The address is stored as an IPv4 address. **Note:** This address is always stored as an IPv4 address, so if the mapping from hostname to IPv4 address later changes in DNS, it will need to be updated here as well. 
1. Enter the port number. This port number must be unique to this PDU.
1. Enter your Management user name.
1. Enter your Management password. Then click **Save**.

Proceed to <a href="#3.7">Assign PDU outlets to servers. 


## <a id="3.7"></a>Assign PDU outlets to servers

**Note:** Be sure that electrical connection between a given power distribution unit (PDU) outlet and a specific server is performed by a qualified technician before PDUs are configured and assigned by this software.

**Note:** This section is for configuring managed storage servers, as previously set up in Add storage servers. This section does not apply to servers that are monitor-only.

**Note:** A server cannot be associated with both baseboard management controller (BMC) outlets and power distribution unit (PDU) outlets. Use PDUs or IPMI/BMCs to support failover. 

Before assigning PDU outlets to servers, make note of the primary and failover server configurations for each volume on the Volumes window. Be sure to assign failover outlets from different PDUs than the primary outlets. When you associate PDU failover outlets with servers using this tool, STONITH is automatically configured. 

To assign PDU outlets to servers:

1. At the menu bar, click the **Configuration** drop-down menu and click **Power Control**. The PDUs you already added should be displayed. If no PDUs are present, see <a href="#3.6">Add power distribution units</a>. 
1. The left column shows all servers used in all file systems that you're currently managing. Each column to the right of the Server column shows outlet assignments for one PDU. If you have four PDUs configured, then there are four PDU columns. Each row represents an outlet-to-server assignment. To assign PDU outlets to servers:
    
    a) Pick a server row for which you want to assign outlets. 
    
    b) Mouse over to the PDU column and click within the drop-down box to expose the outlets available from this PDU. Now select the desired outlet. (You can also use the tab key to move to the desired server/PDU. Then begin to enter the outlet name. This field auto-fills. Tab or press **Enter** to confirm this selection.)
    
    c) Move to the next server and assign outlets in the same way. Note that as an outlet is assigned to a server, it becomes unavailable for reassignment.
    
    d) To remove an outlet from a server, click the **X** next to the outlet name. It now becomes available to reassign.


## <a id="3.8"></a>Assign PDU outlets to servers

This section uses the Intelligent Management Platform Interface (IPMI) and associates baseboard management controllers (BMCs) with servers to support high availability.

**Note:** This section is for configuring managed storage servers, as previously set up in Add storage servers. This section does not apply to servers that are monitor-only.

**Note:** A server cannot be associated with both a BMC and PDU outlets. Use PDUs or BMCs to support failover.

**Issues Regarding Power Loss to the BMC or PDU**

Regarding failover, if the method of power control is not functioning (e.g., loss of power to the fencing device, misconfiguration, etc.), HA will be unable to fail the targets from the failed server to its failover server. This is because in order to complete failover, the failover server must be able to guarantee that the failed server can no longer access targets running on it. The only way to be sure this is true is to remove power from the failed server. Thus, the failover server must be able to communicate with the fencing device of the failed server for failover to occur successfully.

With IPMI, the power for each HA server and its fencing device is coupled together. Accordingly, there are more scenarios where both may lose power at once (chassis power failure, motherboard failure, etc.). If a server suffers chassis power failure such that the BMC is not operational, HA will be unable to fail the targets over. The remedy in this situation is to restore power to the chassis of the failed server to restore the functionality of your file system. *If HA coverage for the scenarios just described is important to you, we strongly recommend using smart PDUs, rather than IPMI as your fencing device*.

Power loss to a PDU will mean that HA will be unable to fail the targets over. As in the above situation, the remedy is to restore power to the PDU to restore the functionality of your file system. *We recommend redundant PDUs if availability is critical*. 

This approach is a necessary limit of HA to protect the integrity of the targets being failed over.

To associate BMCs with servers: 

1. At the menu bar, click the **Configuration** drop-down menu and click **Power Control**.
1. Click **+ Configure IPMI**.
1. At the *Configure IPMI* dialogue window, enter your *Management username* and *Management password*. Click **Save**.
1. Each row is one server. For the desired server, under IPMI, click **+ Add BMC**. 
1. In the *New BMC* window, enter an IP address or hostname for this BMC. **Note:** This address is always stored as an IPv4 address, so if the mapping from hostname to IPv4 address later changes in DNS, it will need to be updated here as well. 
1. Click **Save**.


## <a id="3.9"></a>Create the new Lustre file system

This section is the last procedure to create the Lustre file system, after performing the previous configuration tasks outlined in this chapter. In this section, you will select servers. 

To create the file system:

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems** to display the *File Systems* window.
1. Click **Create File System** to display *New File System Configuration*.
1. In the *File system name* field, enter the name of the new file system. The name can be no more than eight characters long and should conform to standard Linux naming conventions.
1. If this file system is to utilize Hierarchical Storage Management, click the check-box **Enable HSM**. 
1. At step 2, Choose a management target (MGT). Intel® Manager for Lustre* software does not support an MGT larger than 10 gigabytes. *If a management target has been created previously*, the following options will be available. Use one of these options to select the MGT:
    - If the MGT is to be installed on an existing server in the file system, you can select the target to be used from the *Use existing MGT* drop-down list.
    - If a new MGT is to be created, click **Select Storage** to display a list of available servers and then click the server to be used. 

    **Note:** The MGT and MDT can be located on the same server. However, they cannot be located on the same volume/target  on a server.
1. At step 3, choose a primary metadata target (MDT) by clicking **Select Storage**. Then at the drop-down menu, select the target to be used. 
1. Notice the check-box labeled **Add Additional MDTs (DNE)**. After selecting the primary MDT, you can also add additional MDTs. DNE stands for Distributed Namespace. DNE allows the Lustre namespace to be divided across multiple metadata servers. This enables the size of the namespace and metadata throughput to be scaled with the number of servers. The primary metadata target in a Lustre file system is MDT 0, and added MDTs are consecutively indexed as MDT 1, MDT 2, and so on.
    
    To add an additional MDT, click the check-box. Then at the drop-down menu, select the additional MDT target or targets to be used. At the end of this process, after creating the file system, you will enter a command to configure this MDT. 
    
    **Note:** You can also add additional MDTs after the file system has been created; see <a href="Advanced_Topics_10_0.md/#10.3">Add additional Metadata Targets</a>. Any added MDT you create will be unavailable for use as an OST.
1. At step 4, choose the object storage targets (OSTs) for the file system by checking the boxes next to the targets to be included in the system. 
1. Click **Create File System** now to create the file system. 
1. To follow the process as the file system is created, click on **Status** on the top menu bar and select **Commands**. After the file system creation has completed successfully, perform the remaining steps if applicable.
1. If you selected to add additional MDT(s), then log into a client node and mount the Lustre file system. Then at the command line, for each added MDT beyond the primary MDT, enter the following command:    
```
lfs mkdir -i n <lustre_mount_point>/<parent_folder_to_contain_
this_MDT>
```
    where the -i indicates that the following value, n is the MDT index. The first added MDT will be index 1. 
1. Users can now create subdirectories supported by this MDT with the following command, as an example: 
    
    
```
mkdir <lustre_mount_point>/<parent_folder_to_contain_
this_MDT>/<subdirectory_name>
```

**Note:** Intel® Manager for Lustre* software will automatically assign OST indices in a distributed fashion across servers to permit striping.

**Note:** If you plan to enable HSM for this file system, see the chapter [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0) to setup HSM.


## <a id="3.10"></a>View the new file system

To view the file system configuration:

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**. 
1. At the *File Systems* window, select the name of the file system from the table displayed.
1. To view the dashboard metrics for the file system, at the menu bar, click **Dashboard** window and select **File Systems**. Select the file system in the fields displayed at the top of the window.

**Note:** For a new file system, some of the dashboard charts may appear blank until the file system has been running long enough to collect performance data.


## <a id="3.11"></a>Mount the Lustre file system

A compute client must mount the Lustre* file system to be able to access data in the file system. Before attempting to mount the file system on your Lustre clients, make sure the Intel® Enterprise Edition for Lustre* client software has been installed on each client. For instructions, see the documentation provided by your storage solution provider. 

A client can mount the entire file system, or mount a file system sub-directory.

- <a href="#3.11.1">Mount the entire file system</a>
- <a href="#3.11.2">Mount a file system sub-directory</a>


### <a id="3.11.1"></a>Mount the entire file system

To obtain the command to use to mount an entire file system:

1. At the Dashboard menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. Each Lustre file system created using Intel® Manager for Lustre* is listed. Select the file system to be mounted. A window opens showing information for that file system.
1. On the file system window, click **View Client Mount Information**. The mount command to be used to mount the file system is displayed. Following is an example only:
```
    mount -t lustre 10.214.13.245@tcp0:/test /mnt/test
```
1. On the client server, enter the actual command.


### <a id="3.11.2"></a>Mount a file system sub-directory

To mount a file system, at the client computer, enter the following command at the command line.  This syntax is generic and there are other options not described here.


```
mount -t lustre <mgsnid>[:<mgsnid>]:/<fsname>/<subdir path> <mount point>
```



[f3.1]: md_Graphics/lustre-configuration5_zoom40.png
