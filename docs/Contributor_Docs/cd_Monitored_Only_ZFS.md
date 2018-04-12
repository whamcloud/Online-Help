# <a name="Top"></a>Creating a Monitored Only Lustre zfs Filesystem on Vagrant HPC Storage Sandbox

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![zfs](md_Graphics/monitored_filesystem_sm.jpg)

## Prerequisites:

Please refer to https://github.com/intel-hpdd/vagrantfiles on how to create a virtual HPC storage cluster with vagrant before attempting to install IML.

## Download IML build, create zfs installer, and install zfs packages:

Note: use vagrant ssh-config to get the port each server is running on. The commands below use ports that are specific to my vagrant environment.

1.  Verify the following vagrant plugins are installed:
    ```
    vagrant plugin install vagrant-shell-commander
    ```
2.  Download the latest IML build (tarball).
    from: [https://github.com/intel-hpdd/intel-manager-for-lustre/releases/download/{{site.version}}/{{site.package_name}}.tar.gz](https://github.com/intel-hpdd/intel-manager-for-lustre/releases/download/{{site.version}}/{{site.package_name}}.tar.gz)

## Installing IML:

1.  Copy the IML build to the /tmp directory in your admin node:
    ```
    scp -P 2222 ~/Downloads/{{site.package_name}}.tar.gz vagrant@127.0.0.1:/tmp/.
    # password is "vagrant"
    ```
2.  ssh into the admin box and install the build:
    ```
    vagrant ssh
    [vagrant@adm ~]$ sudo su - # (or "sudo -s")
    [vagrant@adm ~]# cd /tmp
    [vagrant@adm ~]# tar xvf <buildname>.tar.gz
    [vagrant@adm ~]# cd <build folder>
    [vagrant@adm ~]# ./install --no-dbspace-check
    ```
3.  Update the /etc/hosts file on your computer to include the following line:
    ```
    127.0.0.1 adm.lfs.local
    ```
4.  Test that a connection can be made to IML by going to the following link in your browser:
    https://adm.lfs.local:8443

## Adding and Configuring Servers

You should now be able to see IML when navigating to https://adm.lfs.local:8443. Click on the login link at the top right and log in as the admin. Next, go to the server configuration page and add the following servers:

```
mds[1,2].lfs.local,oss[1,2].lfs.local
# Make sure to select "Monitored Server Profile" for the servers profile
```

This will take some time (around 5 to 10 minutes) but all four servers should add successfully.
There will be alerts and warnings about LNET. Ignore for now.

## Installing lustre on each MDS and OSS Server

ZFS can now be installed on each mds and oss node since the agent software has been deployed. To do this, follow these simple steps:

1.  Create the zfs installer and install the necessary packages on the following servers: mds1, mds2, oss1, and oss2

    ```
        cd ~/downloads
        tar xzvf {{site.package_name}}.tar.gz
        cd {{site.package_name}}.0
        ./create_installer zfs
        for i in {2200..2203}; do scp -P $i ~/Downloads/{{site.package_name}}.0/lustre-zfs-el7-installer.tar.gz vagrant@127.0.0.1:/tmp/.; done
        # password is "vagrant"
        vagrant sh -c 'cd /tmp; sudo tar xzvf lustre-zfs-el7-installer.tar.gz; cd lustre-zfs; sudo ./install' mds1 mds2 oss1 oss2
    ```

## Configuring each MDS and OSS server

Each server will need to know which interface should be assigned the lustre network.
Run the following commands:

```
   vagrant sh -c '
   systemctl stop firewalld; systemctl disable firewalld;
   systemctl start ntpd;
   modprobe lnet
   lnetctl lnet configure
   lnetctl net add --net tcp0 --if enp0s9
   /sbin/modprobe zfs;
   genhostid' mds1 mds2 oss1 oss2
```

The IML GUI should show that the LNET and NID Configuration is updated (IP Address 10.73.20.x to use `Lustre Network 0`). All alerts are cleared.

## Creating a monitored only zfs based Lustre filesystem

The lustre filesystem will be created from the command line on zpools and IML GUI will be used to scan for the filesytem.
Note that VM Disks (ata-VBOX_HARDDISK...) will be mapped as /dev/sd devices.

* Management Target:

```
    vagrant ssh mds1
    sudo -i
    zpool create mgs -o cachefile=none /dev/disk/by-id/ata-VBOX_HARDDISK_MGS00000000000000000
    mkfs.lustre --failover 10.73.20.12@tcp --mgs --backfstype=zfs mgs/mgt
    zpool export mgs
```

At this point you should wait until the volume disappears from the volumes page and the dataset appears on both the primary and secondary nodes. Then:

```
zpool import mgs
mkdir -p /lustre/mgs
mount -t lustre mgs/mgt /lustre/mgs
```

* Metadata Target:

```
    vagrant ssh mds2
    sudo -i
    zpool create mds -o cachefile=none /dev/disk/by-id/ata-VBOX_HARDDISK_MDT00000000000000000
    mkfs.lustre --failover 10.73.20.11@tcp --mdt --backfstype=zfs --fsname=zfsmo --index=0 --mgsnode=10.73.20.11@tcp mds/mdt0
    zpool export mds
```

At this point you should wait until the volume disappears from the volumes page and the dataset appears on both the primary and secondary nodes. Then:

```
    zpool import mds
    mkdir -p /lustre/zfsmo/mdt0
    mount -t lustre mds/mdt0 /lustre/zfsmo/mdt0
```

* Object Storage Targets:

```
    vagrant ssh oss1
    sudo -i
    zpool create oss1 -o cachefile=none raidz2 /dev/disk/by-id/ata-VBOX_HARDDISK_OST1PORT200000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST3PORT400000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST5PORT600000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST7PORT800000000000
    mkfs.lustre --failover 10.73.20.22@tcp --ost --backfstype=zfs --fsname=zfsmo --index=0 --mgsnode=10.73.20.11@tcp oss1/ost00
    zfs compression=on oss1
    zpool export oss1
```

At this point you should wait until the volume disappears from the volumes page and the dataset appears on both the primary and secondary nodes. Then:

```
    zpool import oss1
    mkdir -p /lustre/zfsmo/ost00
    mount -t lustre oss1/ost00 /lustre/zfsmo/ost00
```

```
    vagrant ssh oss2
    sudo -i
    zpool create oss2 -o cachefile=none raidz2 /dev/disk/by-id/ata-VBOX_HARDDISK_OST0PORT100000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST2PORT300000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST4PORT500000000000 /dev/disk/by-id/ata-VBOX_HARDDISK_OST6PORT700000000000
    mkfs.lustre --failover  10.73.20.21@tcp --ost --backfstype=zfs --fsname=zfsmo --index=1 --mgsnode=10.73.20.11@tcp oss2/ost01
    zfs compression=on oss2
    zpool export oss2
```

At this point you should wait until the volume disappears from the volumes page and the dataset appears on both the primary and secondary nodes. Then:

```
    zpool import oss2
    mkdir -p /lustre/zfsmo/ost01
    mount -t lustre oss2/ost01 /lustre/zfsmo/ost01
```

After all the commands for each node had run successfully, use the IML GUI to scan for the filesystem:
Configuration -> Servers -> Scan for Filesystem. Use all servers

If Successful, in the IML GUI, the filesystem will be available.

## [Setting up Clients](cd_Setting_Up_Clients.md)

---

[Top of page](#Top)
