# Creating a Managed Lustre ZFS Filesystem on a Vagrant virtual cluster

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![zfs](md_Graphics/monitored_filesystem_sm.jpg)

## Prerequisites

Create and setup your Vagrant cluster as described in [Installing IML on Vagrant](cd_Installing_IML_On_Vagrant.md)

## Setting up Power Control

[Follow these instructions to configure the Power Control.](cd_Setting_Up_Power_Control.md)

## Creating Zpools

Now that all managed servers have been added and the power control has been configured, the zpools can be created. Navigate to the volumes page and run the following provision script:

```bash
vagrant provision mds1 mds2 oss1 oss2 --provision-with create-zpools
```

Watch the volumes page and wait for the volumes associated with the targets to change. Four volumes should appear: `mgs`, `mds`, `oss1`, `oss2`.

## Creating a Filesystem

To create a filesystem, simply navigate to `Configuration->File Systems` and click the `Create` button. Make the following selections:

* Management Target / MGS -> `mgs` (512 MB)
* Metadata Target / MDS -> `mds`
* Object Storage Targets -> Select `oss1` and `oss2`

After the selections have been made, click the button to create the filesystem. If you have any issues creating the filesystem there is a good chance that the interface for 10.73.20.x is not assigned to Lustre Network 0. If this happens, stop the filesystem and update the interfaces accordingly.

## Setting up Clients

See [Setting up Clients](cd_Setting_Up_Clients.md).
