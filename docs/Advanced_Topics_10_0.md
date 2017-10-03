<a id="10.0"></a>
# Advanced Topics

[**Online Help Table of Contents**](IML_Help_TOC.md)

The following procedures are provided in this chapter:

- [File system advanced settings](#10.1)
- [Configure a new management target](#10.2)
- [Add additional Metadata Targets](#10.3)


## <a id="10.1"></a>File system advanced settings

The following advanced settings are configurable for each file system. 

**Caution:** Use care when changing these parameters as they can significantly impact functionality or performance. For help with these settings, contact your storage solution provider.

To access these settings:

1. At the menu bar, click the **Configuration** drop-down menu and click **File Systems**.
1. Under *Current File Systems*, select the file system in question.
1. At the File System parameters screen, click **Update Advanced Settings**.

**Tunable Settings**

- *max_cached_mb* - The maximum amount of inactive data cached by the client. Entered in megabytes. The default is 75% of RAM present on the OSS.
- *max_read_ahead_mb* - File read-ahead is triggered when two or more sequential reads by an application fail to be satisfied by the Linux buffer cache. The initial size of the read-ahead is 1 MB. Additional read-aheads grow linearly, and increment until the read-ahead cache on the client is full at 40 MB. This tunable setting controls the maximum amount of data read-ahead permitted on a file. Files are read ahead in RPC-sized chunks (1 MB or the size of read() call, if larger) after the second sequential read on a file descriptor. Random reads are done at the size of the read() call only (no read-ahead). Reads to non-contiguous regions of the file reset the read-ahead algorithm, and read-ahead is not triggered again until there are sequential reads again. To disable read-ahead, set this tunable to 0. The default value is 40 MB. 
- *max_read_ahead_whole_mb* - This setting controls the maximum size of a file that is read in its entirety when the read-ahead algorithm regardless of the size of the read(). The default value is 2 MB. 
- *statahead_max* - Many system commands will traverse a directory sequentially. To make these commands run efficiently, the directory stat-ahead and AGL (asynchronous glimpse lock) are enabled to improve the performance of traversing. This tunable variable sets the maximum number of files that can be pre-fetched by the stat-ahead thread. The default value is 32 bytes. Set the value to 0 to disable.

**Timeout Settings**

These setting are pre-set to default values. Most of these settings are automatically adaptive so that a superuser should not need to change them. These settings are the same timeout settings discussed in the Lustre* Operations Manual.

- *at_early_margin* - Time in seconds of an advance queued request timeout at which the server sends a request to the client to extend the timeout time. The default value is 5.
- *at_extra* - Incremental time in seconds that a server requests the client to add to the timeout time when the server determines that a queued request is about to timeout. The default value is 30.
- *at_history* - Time period in seconds within which adaptive timeouts remember the slowest event that occurred. The default value is 600.
- *at_max* - Adaptive timeout upper limit in seconds. The default value is 600. Set to 0 to disable adaptive timeouts.
- *at_min* - Adaptive timeout lower limit or minimum processing time reported by a server, in seconds. Default value is 0.
- *Idlm_timeout* - Lustre* distributed lock manager timeout: Time in seconds that a server will wait for a client to reply to an initial AST (local cancellation request). The default value is 20 seconds for an OST and 6 seconds for an MDT. 
- *timeout* - Time in seconds that a client waits for a server to complete an RPC. The default value is 100.

[Top of page](#10.0)

## <a id="10.2"></a>Configure a new Management Target

The MGT is normally configured while creating the file system and doesn't need to be created separately on an MGT window. 

Perform the following steps to configure the management target:

1. At the menu bar, click the **Configuration** drop-down menu and click **MGTs** to display the MGT Configuration window.
1. Under *New MGT*, click **Select storage** and select the server for the MGT.
    **Note:** The MGT and metadata target (MDT) can be located on the same server. However, they cannot be located on the same volume on a server.
1. Click **+ Create new MGT** to create the new MGT. 

[Top of page](#10.0)

## <a id="10.3"></a>Add additional Metadata Targets

You can add additional MDTs when creating the file system and later, after the file system has been created. 

DNE stands for Distributed Namespace. DNE allows the Lustre* namespace to be divided across multiple metadata targets. This enables the size of the namespace and metadata throughput to be scaled with the size of the file system and the number of servers. The primary metadata target in a Lustre* file system is MDT0. Added MDTs are indexed as MDT1, MDT2, and so on. 

To add additional MDT(s):

1. At the top menu bar, click **Configuration > File Systems**.
1. Under **Current File Systems**, select the file system you wish to modify.
1. Under **Metadata Target**, click **+ Create MDT (DNE**).
1. At the **Create MDT** pop-up window, select the volume you wish to use as this new MDT. Click **Create**. After a moment, the new MDT will be listed on the file system window, under Metadata Target. You can create additional MDTs; simply repeat steps 3 and 4. When you have created the desired MDT(s), perform step 5.
1. Log into a client node and mount the Lustre* file system. Then at the command line, for each added MDT beyond the primary MDT, enter the following command:
```
lfs mkdir -i n <lustre_mount_point>/<parent_folder_to_contain this_MDT>
```
where the -i indicates that the following value, `n` is the MDT index. The first added MDT will be index 1.

The new MDT is installed. Users can now create subdirectories supported by each added MDT with the following command, as an example:
```
mkdir <lustre_mount_point>/<parent_folder_to_contain this_MDT>/<subdirectory_name>
```

**Note:** Any added MDT you create will be unavailable for use as an OST.

[Top of page](#10.0)