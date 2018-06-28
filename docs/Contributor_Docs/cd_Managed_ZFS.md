# Creating a Managed Lustre ZFS Filesystem on a Vagrant virtual cluster

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![zfs](md_Graphics/monitored_filesystem_sm.jpg)

## Prerequisites

Create and setup your Vagrant cluster as described in [Installing IML on Vagrant](cd_Installing_IML_On_Vagrant.md)

## Creating Zpools

Now that all managed servers have been added and the power control has been configured, the zpools can be created.

1. ssh into `mds1` and switch to the root account with `sudo -i`.
1. In the GUI, navigate to *Configuration->Volumes*. Setup your web browser and console next to each other such that the result of running commands in your console can be viewed on the browser in real time.
1. Create the MGS. On the volumes page, look for the mds with a file size of 512MB. This should be easy to spot as the other mds has a capacity of 5GB. Notice the numbers that come after `VBOX_HARDDISK`. This is the diskSerial. Enter the following command:

    ```bash
    root@mds1 by-id]# zpool create mgs -o cachefile=none -o multihost=on /dev/disk/by-id/ata-VBOX_HARDDISK_MGS00000000000000000
    ```

1. Create the MDS. On the volumes page, look for the mds with a file size of 5GB. This should be the only mds left. Take note of the diskSerial for this mds and enter the following command:

    ```bash
    [root@mds1 by-id]# zpool create mds -o cachefile=none -o multihost=on /dev/disk/by-id/ata-VBOX_HARDDISK_MDT00000000000000000
    ```

1. Create OSS1. Exit out of `mds1` and ssh into `oss1`. On the volumes page, look for all occurrences of `oss1` and take note of their diskSerial's. Enter the following command:

    ```bash
    [root@oss1 ~]# zpool create oss1 -o cachefile=none -o multihost=on raidz2 /dev/disk/by-id/ata-VBOX_HARDDISK_OST0PORT100000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST2PORT300000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST4PORT500000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST6PORT700000000000
    ```

1. Create OSS2. On the volumes page, look for all occurrences of `oss2` and take note of their diskSerial's. Enter the following command:

    ```bash
    [root@oss1 ~]# zpool create oss2 -o cachefile=none -o multihost=on raidz2 /dev/disk/by-id/ata-VBOX_HARDDISK_OST1PORT200000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST3PORT400000000000  /dev/disk/by-id/ata-VBOX_HARDDISK_OST5PORT600000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST7PORT800000000000
    ```

Watch the volumes page and wait for the volumes associated with the targets to change. You should see four resultant volumes: `mgs`, `mds`, `oss1`, `oss2`.

## Creating a Filesystem

To create a filesystem, simply navigate to `Configuration->File Systems` and click the `Create` button. Make the following selections:

* Management Target / MGS -> `mgs` (512 MB)
* Metadata Target / MDS -> `mds`
* Object Storage Targets -> Select `oss1` and `oss2`

After the selections have been made, click the button to create the filesystem. If you have any issues creating the filesystem there is a good chance that the interface for 10.73.20.x is not assigned to Lustre Network 0. If this happens, stop the filesystem and update the interfaces accordingly.

## Setting up Clients

See [Setting up Clients](cd_Setting_Up_Clients.md).
