[**Intel® Manager for Lustre\* Online Help Main Table of Contents**](../README.md)
# <a id="8.0"></a>Creating and Managing ZFS-based Lustre file systems

Intel® Manager for Lustre* software is able to create and manage Lustre file systems that are based on OpenZFS object storage device (OSD) volumes. The software installs the necessary packages, formats Lustre targets from ZFS pools, and creates the high-availability software framework for managing availability for Lustre + ZFS servers.  The following topics are covered:

- <a href="#8.1">Create a ZFS-based Lustre file system</a>
- <a href="#8.2">Importing and exporting ZFS pools in a shared-storage high-availability cluster</a>
- <a href="#8.3">Removing a ZFS-based Lustre file system</a>
- <a href="#8.4">Destroy an individual zpool</a>
- <a href="#8.5">Destroy all of the ZFS pools in a shared-storage</a>



## <a id="8.1"></a>Create a ZFS-based Lustre file system

The procedures in this section assume that you have first assembled and configured the physical hardware: servers, storage devices, network interfaces, etc., and installed Intel® Manager for Lustre* software as instructed in the *Intel® Enterprise Edition for Lustre\* Software Installation Guide*.  

To create and manage an OpenZFS-based Lustre file system that is highly-available and managed by Intel® Manager for Lustre* software, perform these steps:

1. Add all of the physical servers that will comprise your ZFS-based Lustre file system. To do this, perform the steps in [Add one or more HA servers](Creating_new_lustre_fs_3_0.md/#3.4). Add each server as a *Managed Storage Server*.
    
    **Note:**  Steps 2 and 3 below are performed automatically by Intel® Manager for Lustre\* software and do not need to be performed.  They are included here for topic coverage only. Continue with Step 4.

1. Having added the servers, you now need to ensure that the server hostids are set before creating any zpools. Each server requires a unique hostid to be configured. Setting the hostid on each server will allow ZFS to apply an attribute on each zpool indicating which host currently has the pool imported. This provides some protection in ZFS against multiple simultaneous imports of zpools when the storage is connected to more than one server. To set the hostid, run the genhostid command on each host and reboot. In the document *Lustre\* Installation and Configuration using Intel® EE for Lustre\* Software and OpenZFS*, see the section *Protecting File System Volumes from Concurrent Access* for more information.

1. As a further protection against “double-importing” ZFS pools, and to prevent conflicts with the Pacemaker resource management software, disable the ZFS Systemd target by entering the following command:
	
	```
	systemctl disable zfs.target
	```
    
    This will stop the operating system from attempting to auto-import ZFS storage pools during system boot. Disabling the ZFS target affect all ZFS storage pools, including any that are not being used for Lustre.

1. ZFS pool configuration is executed directly on each of the Lustre server HA pairs using the command line tools supplied with the ZFS software. The storage devices for each ZFS pool must be connected to, and accessible from, each Lustre server in the HA pair. For each ZFS pool, it is easiest to nominate a primary server and use that host to create the zpool. Log into each primary host and use this zpool command to create each storage pool.  The general syntax for creating a zpool is as follows:
	
	```
	zpool create [-f] -O canmount=off \
	-O mountpoint=none \
	[ -o <option> ] \
	-o cachefile=none \
	-o failmode=panic \
	<zpool name> <zpool specification>
	```
    ZFS is highly configurable and there are a wide range of optional parameters that can be applied to a ZFS pool, to improve performance or to modify functionality. The most important of these are as follows:
    - cachefile=none: ZFS uses the cachefile to identify pools it can automatically import, but this does not make consideration for shared storage cluster environments. To prevent a ZFS pool from being added to the default cachefile and automatically imported at system boot, it is essential that all ZFS pools that are held on shared storage have the cachefile set to the special value “none”. This, in conjunction with setting the hostid provides a lightweight impediment against double-importing the pool.
    - failmode=panic: zpools should have the "failmode" parameter set to "panic". This will cause a host that has lost connectivity to the underlying storage devices, or has experienced too many device failures, to shut down immediately. The node is thus prevented from issuing undesired writes to a zpool after catastrophic failures, including host disconnection from the zpool. When ZFS pools are operating within an HA cluster framework, panicking a node will also trigger a failover event in the cluster, allowing the zpools to be imported to a standby node, and services to continue operation.
    - ashift: used to override ZFS auto-detection of the physical vdev storage sector size. Advanced format drives are known to cause issues by incorrectly reporting the native sector size. Setting the ashift property forces ZFS to use a specific sector size, and can yield improved performance. The value of ashift is an exponent to power of 2. Typically used to set 4KB sector size, (ashift=12).

    In addition to zpool properties, there are also properties that can be applied to the ZFS datasets in a pool.  ZFS dataset properties are set in the zpool command using a capital letter -O, rather than the lower case letter -o flag used for the cachefile and ashift settings. The -O flag is used to set properties to the root file system data set in the pool, rather than for properties of the pool itself. Two ZFS dataset properties of particular importance are highlighted here:
    
    - canmount=off: prevent the dataset from being mounted using the standard zfs mount command. Essential for Lustre OSDs, which must be mounted and unmounted using the mount.lustre (or mount -t lustre) command.
    - recordsize: this sets a suggested block size for the file system. The block size cannot exceed this value. The default value, 128KB, is fine for MGT and MDT OSDs. For OSTs, where large block IO is the dominant workload, set the recordsize=1M, which is the maximum currently allowed in ZFS on Linux version 0.6.5. Future versions of ZFS are expected to be able to further increase this value.
    - mountpoint=none: in monitored mode, the management software requires that ZfsDatasets have the following property values to prevent undesired automatic mounting.

    For more details, refer to the section ZFS OSDs, in the guide titled Lustre* Installation and Configuration using Intel® EE for Lustre* Software and OpenZFS, as well as the system man pages for zfs(8) and zpool(8).

    Following are three examples of typical pool configurations, one each for MGT, MDT and OST respectively:
    
  - ZFS pool for MGT (typically a simple mirror):

	```
	zpool create -O canmount=off \
	-O mountpoint=none \
	-o cachefile=none \
	-o failmode=panic \
	mgspool mirror <dev A> <dev B>
  	```
    
  - ZFS pool for MDT (typically a stripe of mirrors to maximize performance):

	```
	zpool create -O canmount=off \
	-O mountpoint=none \
	-o cachefile=none \
	-o failmode=panic \
	<fsname>-mdt<n>pool \
	mirror <dev A> <dev B> [ mirror <dev C> <dev D> ] ...
	```
	
	**Note:** The naming convention for the pool name is intended to reflect the Lustre file system name name (\<fsname\>) and the MDT index number (\<n\> usually 0, unless DNE is used). The number of mirrors used for the MDT depends on the requirements of the installation and can be scaled up accordingly.
    
   - ZFS pool for OST (typically a RAIDZ2 pool, balancing reliability against optimal capacity):
   
   	```
	zpool create -O canmount=off \
	-O recordsize=1M \
	-O mountpoint=none \
	-o failmode=panic \
	-o cachefile=none \
	[ -o ashift=12 ] \
	<fsname>-ost<n>pool \
	raidz2 <dev A> <dev B> \
	<dev C> <dev D>  <dev E> <dev F> ...
	```

**Note:** See the document *Lustre\* Installation and Configuration using Intel® EE for Lustre\* Software and OpenZFS* for descriptions of the ashift and recordsize properties. RAIDZ2 is the preferred vdev configuration for OSTs, and we recommend an arrangement of at least 11 disks (9+2) per RAIDZ2 vdev for best performance. The pool naming convention is based on the Lustre file system name and OST index number, starting at 0 (zero).

   The remainder of this procedure is performed at the Intel® Manager for Lustre\* software GUI. 
1. For high-availability, configure your servers as primary and fail-over servers for each zpool.  Perform the steps in [Configure primary and fail-over servers<](Creating_new_lustre_fs_3_0.md/#3.5).
1. If you are using power distribution units (PDUs) for power control, then for each server, perform the steps in [Add power distribution units](Creating_new_lustre_fs_3_0.md/#3.6).  Then perform the steps in [Assign PDU outlets to servers](Creating_new_lustre_fs_3_0.md/#3.7) for each server.
1. If you are using Baseboard Management Controllers (BMCs) for power control, then perform the steps in [Assign BMCs to servers](Creating_new_lustre_fs_3_0.md/#3.8)for each server.  
1. Perform the steps in [Create the new Lustre file system](Creating_new_lustre_fs_3_0.md/#3.0), using the zpools you created in step 4 above as object storage targets (volumes), rather than direct block devices.  Each ZFS pool that you created will appear as a target, with the Type identified as a **ZfsPool**.

<a href="#8.0">Top of page</a>

<a id="8.2"></a>
## Importing and exporting ZFS pools in a shared-storage high-availability cluster

ZFS file system datasets are always members of a pool, and the pool must be imported to a host before any action can be taken to alter its content. In a shared-storage, high-availability cluster, some pools may be imported on different hosts. This is a common and recommended practice that balances distribution of Lustre OSDs equitably across the HA cluster nodes. 

One must always manage ZFS pools and their contents from the host where the pool is imported, but it is easy to overlook and miss ZFS pools that are exported. Use the combined output of ```zpool list``` and ```zpool import``` to gain a complete list of all storage pools available to a host, and import any pools that require administration.

1. List the currently imported ZFS pools:
	```
	zpool list
	```
2. If any of the pools that are expected to be on this host are missing, it may be that the pools have been exported, or are imported on a different host. Use the ```zpool import``` command to identify these pools. For example:
	
	```
	[root@rh7z-oss1 ~]# zpool import
   pool: demo-ost0pool
     id: 12622396723776112603
     state: ONLINE
     action: The pool can be imported using its name or numeric identifier.
     config:

	demo-ost0pool  ONLINE
	  raidz2-0  ONLINE
	    sda     ONLINE
	    sdb     ONLINE
	    sdc     ONLINE
	    sdd     ONLINE
	    sde     ONLINE
	    sdf     ONLINE

   pool: demo-ost1pool
     id: 617459513944251623
     state: ONLINE
     status: The pool was last accessed by another system.
     action: The pool can be imported using its name or numeric identifier 
     and the '-f' flag.
   see: http://zfsonlinux.org/msg/ZFS-8000-EY
   config:

	demo-ost1pool                             ONLINE
	  raidz2-0                                ONLINE
	    scsi-0QEMU_QEMU_HARDDISK_IEELOST0001  ONLINE
	    scsi-0QEMU_QEMU_HARDDISK_IEELOST0007  ONLINE
	    scsi-0QEMU_QEMU_HARDDISK_IEELOST0011  ONLINE
	    scsi-0QEMU_QEMU_HARDDISK_IEELOST0010  ONLINE
	    scsi-0QEMU_QEMU_HARDDISK_IEELOST0009  ONLINE
	    scsi-0QEMU_QEMU_HARDDISK_IEELOST0008  ONLINE
	```
In the example, there are two exported pools. Note that the second pool in the list has a status attribute that is not displayed in the first pool, and that the action attribute indicates that the pool can only be imported by force (indicated by the '-f' flag). This means that the pool has been imported on a different host. Do not import pools that are in this condition unless it can be absolutely determined that the other host is offline or does not have this pool running (this is commonly the case when a server crashes or loses power in an unclean shutdown).
1. Use the ```zpool import``` command, along with the pool name, to import a pool onto the host:
	```
	zpool import [-f] <pool name>
	```
	For example:
	```
	[root@rh7z-oss1 ~]# zpool import demo-ost0pool
	```
	A simple approach to managing all of the pools of an HA cluster as a batch, is to export all of the pools from each host connected to common shared storage, and then import all of the pools into a single host, as follows:

1. Export all of the pools on a host:
	```
	zpool export –a
	```
	Repeat this on every host in the HA framework
2. On one host, import all of the zpools:
	```
	zpool import -a
	```
<a href="#8.0">Top of page</a>

<a id="8.3"></a>
## Removing a ZFS-based Lustre file system

When removing a Lustre file system, the Intel® Manager for Lustre\* software does not destroy the data content held on Lustre OSDs. This allows the operator an opportunity to recover data from the OSDs if the file system was removed from IML accidentally. As a consequence, after the file system is removed from the manager, the OSD volumes may need to be cleaned up as a separate operation before they are ready to be re-used.

LDISKFS volumes do not require any special treatment; they can simply be reformatted, either by hand or by re-adding the volumes into a new Lustre file system via  Intel® Manager for Lustre\* software. The manager software will detect the pre-existing Lustre data, and ask the user to confirm that the volume is to be re-used.
ZFS OSDs require some additional work. ZFS OSDs are file system datasets inside zpools. After a file system is removed using Intel® Manager for Lustre\* software, any ZFS OSDs from that file system will still be present in the ZFS storage pools (zpools), and cannot be re-used directly. To reuse the storage in a zpool, the existing OSD datasets must first be removed, using the zfs destroy command.  This is described in these sections:

- <a href="#8.4">Destroy an individual zpool</a>
- <a href="#8.5">Destroy all of the ZFS pools in a shared-storage high-availability cluster

<a href="#8.0">Top of page</a>

<a id="8.4"></a>
## Destroy an individual zpool

Perform the following steps.

1. Run the zpool list command to display a list of zpools currently imported on the host.

1. If a pool is missing from the output, it may be imported on a different host or it may be in the exported state. Use the zpool import command to identify ZFS pools  that have been created, but are not imported on the current host:
	```
	zpool import
	```
If a zpool has a status field that says the pool was last accessed by another system, this pool may still be active on a different host connected to the same shared storage. The output will include fields similar to the following:
```
...
status: The pool was last accessed by another system.
action: The pool can be imported using its name or numeric identifier 
and the '-f' flag.
...
```
Don't force an import of a pool in this state unless you are certain that the other host is offline. If possible, either export the zpool from the other host so that it can be imported, or log into the other host to perform the required work.
1. If necessary, use the zpool import command, along with the pool name, to import a pool onto the host:
```
zpool import <pool name>
```
1. Run the command: 
```
zpool destroy  [-f] <zpool name>
```
For example:
```
zpool destroy demo-ost0pool
```
1. Confirm that the pool has been removed with zpool list.

<a href="#8.0">Top of page</a>

<a id="8.5"></a>
## Destroy an individual zpool

Perform the following steps.

1. Log into each server in the cluster framework that is connected to the same shared storage and export all of the ZFS pools:
```
zpool export –a
```
1. On one host, import all of the zpools:
```
zpool import –a
```
1. List the zpools:
```
zpool list
```
1. For each pool, run the zpool destroy command:
```
zpool destroy [-f] <pool name>
```
The ‘-f’ flag will force the destruction of the pool, unmounting any active datasets that may be present.

