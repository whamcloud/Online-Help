<a id="6.0"></a>
# Configuring and using Hierarchical Storage Management

[**Online Help Table of Contents**](IML_Help_TOC.md)

**In this chapter:**

- [Add an HSM Agent node](#6.1)
- [Add a Copytool to an HSM Agent node](#6.2)
- [Start the Copytool](#6.3)
- [Using HSM](#6.4)
- [Add a Robinhood Policy Engine server](#6.5)

Hierarchical Storage Management (HSM) can help provide a cost-effective storage platform that balances performance and capacity. With HSM, storage systems are organized into tiers. The high-performance, primary tier is on the shortest path to the systems where applications are running and where the most data is generated and consumed. As the high-performance tier fills, data that is not being as actively accessed is migrated to lower-cost, higher-capacity storage archive for long-term retention. Data migration is generally managed automatically and transparently to users. 

Intel® Manager for Lustre* software provides a framework for incorporating HSM into a Lustre file system. When a new file is created, a replica is made on the associated HSM archive tier, so that initially, two copies of the file exist. As changes are made to the file, these are replicated onto the archive copy as well. As the available capacity is consumed on the high-performance tier, the least-frequently-used files are deleted from that tier and each file is replaced with stub file that points to the archive copy. Applications are not aware of the locality of a file. Applications do not need to be re-written to work with data stored on an HSM system. If a system call is made to open a file that has been deleted from the high-performance tier, the HSM software automatically dispatches a request to retrieve the file from the archive and restore it to the high-performance tier.

The HSM framework included with Intel® Manager for Lustre* software includes the following components:

- **An Agent:** A Lustre* client that runs an instance of Copytool to transfer certain files between the Lustre* file system and the archive, and deletes from the Lustre* file system those files that have been archived. There can be one instance of Copytool per agent.
- **A POSIX Copytool:** This is a reference implementation included in Lustre 2.5 and later. The copytool actually performs the data transfer between the file system and the archive. 
- **The HSM Coordinator:** The HSM Coordinator gathers all archive requests and dispatches them to Agents. The HSM Coordinator thread coordinates HSM activities. (Some documents refer to this as the MDT Coordinator.)
- **The Robinhood policy engine:** Robinhood enables full automation of HSM activities. Robinhood lets an administrator create file archiving policies based on the file class, as defined by file size, path, owner, age, extended attributes (xattrs), least-recently used, and other criteria. Multiple rules can be combined with Boolean operators. After copying files to archive, automatic file system purging can be set to occur based on the amount the percentage of consumed file system capacity, file classes, etc. Robinhood can also be used to generate reports, and create packages. 

**Note:** Robinhood is *not necessary to provide basic HSM capabilities* and this HSM framework as installed does not define Robinhood policies. Note that the Robinhood policy engine server requires a supported RDBMS.

**Configure basic HSM capabilities for a Lustre* file system**

Perform these tasks to configure basic HSM capabilities for a Lustre* file system. 

- [Add an HSM Agent node](#6.1)
- Configure power control (optional): HSM Agent nodes are NOT configured for high-availability with Pacemaker and Corosync. The HSM Coordinator schedules HSM tasks with multiple copytools, and if a copytool goes offline, the HSM Coordinator will assign HSM activities to the remaining copytool(s). However, you can configure power control, so that an HSM Agent can be power-controlled from the Intel® Manager for Lustre* software GUI. You can either configure power distribution units (PDUs), or baseboard management controllers (BMCs) to control power to HSM Agent nodes. 
    - To configure PDUs, see [Add power distribution units](Creating_new_lustre_fs_3_0.md/#3.6) and [Assign PDU outlets to servers](Creating_new_lustre_fs_3_0.md/#3.7).
    - To configure IMPI/BMCs, see [Assign BMCs to servers](Creating_new_lustre_fs_3_0.md/#3.8).
- [Add a copytool to an HSM Agent node](#6.2)
- For an overview of manual HSM tasks, see [Using HSM](#6.4).

**Add a Robinhood policy engine server**

Robinhood can automate HSM activities. The section linked here discusses adding a Robinhood policy engine server, but does not discuss configuring Robinhood for HSM automation. For more information, see the related guide: *Hierarchical Storage Management Configuration*.

 - [Add a Robinhood policy engine server](#6.5)
 
[Top of page](#6.0)

## <a id="6.1"></a>Add an HSM Agent node

If you plan to enable Hierarchical Storage Management (HSM), perform the following procedures to create an HSM Agent node.

To add a copytool instance to an existing HSM Agent node, see [Add a Copytool to an HSM Agent node](#6.2).

**Add an HSM Agent node:**

1. Perform the steps under [Add one or more servers](Creating_new_lustre_fs_3_0.md/#3.4). In that procedure, when selecting the server profile, select **POSIX HSM Agent Node**. 
1. When you have added the server(s), perform the procedure in [Add a Copytool to an HSM Agent node](#6.2).
1. After the copytool has been added to the HSM Agent node, see [Using HSM](#6.4).

[Top of page](#6.0)

## <a id="6.2"></a>Add a Copytool to an HSM Agent node

1. At the menu bar, click the **Configuration** drop-down menu and click **HSM**.
1. At the bottom of the window, click **+ Add Copytool**.
1. At the Add Copytool form, set the following fields:
    
    a. **File system:** Specify file system for which this copytool will perform HSM actions.
    
    b. **Worker:** This is the POSIX HSM Agent node that you configured in [Add an HSM Agent node](#6.1). Each copytool instance has its own Agent node, so there may be several. Note that copytool is multi-threaded, so it is able to support multiple simultaneous HSM operations.
    
    c. **Path to the HSM agent binary:** The file system path to the copytool binary on the worker. For the POSIX copytool provided with Intel® Manager for Lustre* software, the path is `/usr/sbin/lhsmtool_posix`). This was installed on the agent when you configured the HSM Agent node. If another copytool has been installed, it likely resides at another location. 
    
    d. **HSM agent arguments (optional):** This is a vendor-specific list of copytool arguments. Consult your HSM vendor documentation for the applicable arguments.
    
    **Note:** Do not provide any flags that will cause the copytool process to be run in the background (e.g. --daemon); this interferes with the ability of Intel® Manager for Lustre* software to control and monitor the copytool process.
    
    e. **File system mount point:** The file system mount point on the worker node. Copytool instances require client access to their associated file system.
    
    f. **Archive number:** The storage back-end number. Change this number only if your site policies require multiple storage back-ends. If there is only one archive available for the file system, set the archive number to "1" (the default). For more information, consult the "Lustre* Operations Manual", Section 22.3.1: Archive ID, multiple back-ends.
1. To commit this configuration, click **Save**.

See [Start the Copytool](#6.3).

[Top of page](#6.0)

## <a id="6.3"></a>Start the Copytool

When a copytool is added to a Intel® Manager for Lustre* software file system configuration, it is not automatically activated. Instead, the copytool will initially be set to Unconfigured. The configuration exists inside the Intel® Manager for Lustre* software database but it has not been applied directly to the target HSM Agent.

To configure and launch the copytool on an HSM Agent:

1. Click the **Configuration** menu and select **HSM**.
1. Locate the copytool instance in the Copytools table. 
1. For the desired copytool, click the **Actions** drop down menu and select **Start**. The copytool status will change from *Unconfigured* to *Idle* and the graph will register that a new idle copytool instance has been added and is running on the file system.

As soon as copytool services are requested, the copytool worker will respond. See [HSM window](Graphical_User_Interface_9_0.md/#9.3.4) for more information.

[Top of page](#6.0)

## <a id="6.4"></a>Using HSM

After configuring the Copytool Agent node and adding Copytool to that agent, you can use HSM to manage file archiving, free-up file system storage, and improve overall file system performance. 

1. To use HSM, log into a regular Lustre* client node as the system superuser. The node is a compute client node not managed by Intel® Manager for Lustre* software. 
1. Issue `lfs` commands to initiate HSM actions (archive, restore, release, remove). 
    
    For example: 
```
root@client1234 #: lfs hsm_archive /mnt/lustre/path/to/big_file
```
1. After issuing this archive command, the superuser can monitor progress on the operation in the Intel® Manager for Lustre* software GUI. To monitor progress, click **Configuration** and click **HSM** to open the HSM window and observe copytool archive progress.
1. After the archive operation has completed, you can release command to remove the file from the Lustre* file system and free up that space. 

    For example: 
```
root@client1234 #: lfs hsm_release /mnt/lustre/path/to/big_file
```

After this command completes, the file’s data exists in the HSM archive, but the file has been moved off of Lustre* main storage. You may notice that the available space in the lustre* file system has increased (if the file is large enough and the file system small enough - otherwise the change won’t register in the graphs). 

If you want the file to be copied back to the file system, issue an `lfs` restore command (below). Alternatively, wait for the next read attempt of that file by a client, and an implicit restore will return the file back to the file system. 

The following are `lfs hsm` commands:

- ```lfs hsm_archive /mnt/lustre/<path>/<filename>
```
 Copies the file to the archive.
 - 
```lfs hsm_release /mnt/lustre/<path>/<filename>
```
Removes the file from the Lustre* file system; does not affect the archived file.
 - ```lfs hsm_restore /mnt/lustre/<path>/<filename>
```
Restores the archived file back to the Lustre* file system. 
    This is an asynchronous, non-blocking restore. A client's request to access an archived file will also restore the file back to the Lustre* file system if it has been released; this will be a synchronous and blocking restore.
- ```lfs hsm_cancel /mnt/lustre/<path>/<filename>
```
Cancels an `lfs_hsm` command that is underway.


**Displaying information about a current lfs_hsm request**

To view the progress of HSM copytool activities, click **Configuration** and click **HSM** to open the HSM window and observe copytool progress. See [Monitor HSM Copytool activities](Monitoring_lustre_fs_4_0_0.md/#4.8) for more information.

The command```
lctl get_param mdt.*.hsm
```
also requests returns information about the currently executing HSM request.

[Top of page](#6.0)

## <a id="6.5"></a>Add a Robinhood Policy Engine server

The Robinhood policy engine can be used to automate HSM activities. Each instance of Robinhood and its RDBMS supports a single file system. A single server can support multiple instances of Robinhood. The following procedure adds a Robinhood server but does not discuss policy configuration. See the implementation guide *Hierarchical Storage Management Configuration Guide* for more information.  

To add a Robinhood policy engine server, perform the steps under [Add one or more servers](Creating_new_lustre_fs_3_0.md/#3.4). In that procedure, when selecting the server profile, select **Robinhood Policy Engine** Server. For an overview, see [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0).

**Creating Policies**

Robinhood lets a superuser create file-archiving policies based on the file class, as defined by file size, path, owner, age, extended attributes (xattrs), least-recently used, and other criteria. Multiple rules can be combined with Boolean operators. After copying files to archive, automatic file system purging can be set to occur based on the percentage of consumed file system capacity, file classes, etc. Robinhood can also be used to generate reports and create packages. See the implementation guide *Hierarchical Storage Management Configuration Guide* for more information.

[Top of page](#6.0)
