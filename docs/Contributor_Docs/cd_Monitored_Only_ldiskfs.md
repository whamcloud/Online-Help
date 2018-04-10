# <a name="Top"></a>Creating a Monitored Only Lustre ldiskfs Filesystem on Vagrant HPC Storage Sandbox

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![ldiskfs](md_Graphics/monitored_filesystem_sm.jpg)

## Prerequisites:

Please refer to [creating a virtual HPC storage cluster with vagrant](https://github.com/intel-hpdd/vagrantfiles) before attempting to install IML.

## Download IML build, create ldiskfs installer, and install ldiskfs packages:

Note: use vagrant ssh-config to get the port each server is running on. The commands below use ports that are specific to my vagrant environment.

1. Verify the following vagrant plugins are installed:
   ```
   vagrant plugin install vagrant-shell-commander
   ```
2. Download the latest IML build (tarball).
   from: [https://github.com/intel-hpdd/intel-manager-for-lustre/releases/download/4.0.0/iml-4.0.0.0.tar.gz](https://github.com/intel-hpdd/intel-manager-for-lustre/releases/download/4.0.0/iml-4.0.0.0.tar.gz)

## Installing IML:

1. Copy the IML build to the /tmp directory in your admin node:
   ```
   scp -P 2222 ~/Downloads/iml-4.0.0.0.tar.gz vagrant@127.0.0.1:/tmp/.
   # password is "vagrant"
   ```
2. ssh into the admin box and install the build:
   ```
   vagrant ssh
   [vagrant@adm ~]$ sudo su - # (or "sudo -s")
   [vagrant@adm ~]# cd /tmp
   [vagrant@adm ~]# tar xvf <buildname>.tar.gz
   [vagrant@adm ~]# cd <build folder>
   [vagrant@adm ~]# ./install --no-dbspace-check
   ```
3. Update the /etc/hosts file on your computer to include the following line:
   ```
   127.0.0.1 adm.lfs.local
   ```
4. Test that a connection can be made to IML by going to the following link in your browser:
   https://adm.lfs.local:8443

## Adding the MDS and OSS Servers

You should now be able to see IML when navigating to https://adm.lfs.local:8443. Click on the login link at the top right and log in as the admin. Next, go to the server configuration page and add the following servers using the "Monitored Server" profile:

```
mds[1,2].lfs.local,oss[1,2].lfs.local
```

This will take some time (around 5 to 10 minutes) but all four servers should add successfully.
There will be alerts and warnings about LNET. Ignore for now.

## Installing lustre on each MDS and OSS Server

Lustre\* server can now be installed on each mds and oss node since the agent software has been deployed. To do this, follow these simple steps:

1. Create the ldiskfs installer and install the necessary packages on the following servers: mds1, mds2, oss1, and oss2
   ```
       cd ~/downloads
       tar xzvf iml-4.0.0.0.tar.gz
       cd iml-4.0.0.0
       ./create_installer ldiskfs
       for i in {2200..2203}; do scp -P $i ~/Downloads/iml-4.0.0.0/lustre-ldiskfs-el7-installer.tar.gz vagrant@127.0.0.1:/tmp/.; done
       # password is "vagrant"
       vagrant sh -c 'cd /tmp; sudo tar xzvf lustre-ldiskfs-el7-installer.tar.gz; cd lustre-ldiskfs; sudo ./install;' mds1 mds2 oss1 oss2
       vagrant halt mds1 mds2 oss1 oss2
       vagrant up mds1 mds2 oss1 oss2
   ```

## Configuring each MDS and OSS Server

Each server will need to know which interface should be assigned the lustre network.
Run the following commands:

```
    vagrant sh -u root -c '
    systemctl stop firewalld; systemctl disable firewalld;
    systemctl start ntpd;
    modprobe lnet
    lnetctl lnet configure
    lnetctl net del --net tcp0 --if enp0s3
    lnetctl net add --net tcp0 --if enp0s9
    /sbin/modprobe lustre;
    genhostid' mds1 mds2 oss1 oss2
```

The IML GUI should show that the LNET and NID Configuration is updated (IP Address 10.73.20.x to use `Lustre Network 0`). All alerts are cleared.

## Creating a monitored only ldiskfs based Lustre filesystem

When setting up a lustre filesystem, each server must be formatted with the servicenode set to the appropriate nid. Start by creating a mapping of NIDS:

```
vagrant sh -c 'lctl list_nids' mds1 mds2 oss1 oss2
# Will produce output similar to:
# mds1::
# 10.73.20.11@tcp
# mds2::
# 10.73.20.12@tcp
# oss1::
# 10.73.20.21@tcp
# oss2::
# 10.73.20.22@tcp
#
# MGS_NID="10.73.20.12@tcp"
# MDS_NID="10.73.20.11@tcp"
# OSS1_NID="10.73.20.21@tcp"
# OSS2_NID="10.73.20.22@tcp"
```

### Format the MGS and mount Lustre

```
vagrant sh -u root -c 'mkfs.lustre --mgs --reformat --servicenode=10.73.20.12@tcp \
--servicenode=10.73.20.11@tcp /dev/disk/by-id/ata-VBOX_HARDDISK_MGS00000000000000000' mds2
vagrant sh -u root -c 'mkdir -p /mnt/mgs' mds1 mds2
vagrant sh -u root -c 'mount -t lustre /dev/disk/by-id/ata-VBOX_HARDDISK_MGS00000000000000000 /mnt/mgs' mds2
# verify the mount
vagrant sh -u root -c 'mount | grep lustre' mds2
```

### Format the MDS and mount Lustre

```
vagrant sh -u root -c 'mkfs.lustre --mdt --reformat --servicenode=10.73.20.12@tcp \
--servicenode=10.73.20.11@tcp --index=0 --mgsnode=10.73.20.12@tcp --fsname=fs \
/dev/disk/by-id/ata-VBOX_HARDDISK_MDT00000000000000000' mds1
vagrant sh -u root -c 'mkdir -p /mnt/mds' mds1 mds2
vagrant sh -u root -c 'mount -t lustre /dev/disk/by-id/ata-VBOX_HARDDISK_MDT00000000000000000 /mnt/mds' mds1
# verify the mount
vagrant sh -u root -c 'mount | grep lustre' mds1
```

### Format OSS1 and mount Lustre

```
vagrant sh -u root -c 'mkfs.lustre --ost --reformat --servicenode=10.73.20.21@tcp \
--servicenode=10.73.20.22@tcp --index=0 \
--mgsnode=10.73.20.12@tcp --fsname=fs \
/dev/disk/by-id/ata-VBOX_HARDDISK_OST0PORT100000000000' oss1
vagrant sh -u root -c 'mkdir -p /mnt/ost0' oss1 oss2
vagrant sh -u root -c 'mount -t lustre /dev/disk/by-id/ata-VBOX_HARDDISK_OST0PORT100000000000 /mnt/ost0' oss1
# verify the mount
vagrant sh -u root -c 'mount | grep lustre' oss1
```

### Format OSS2 and mount Lustre

```
vagrant sh -u root -c 'mkfs.lustre --ost --reformat --servicenode=10.73.20.21@tcp \
--servicenode=10.73.20.22@tcp --index=1 \
--mgsnode=10.73.20.12@tcp --fsname=fs \
/dev/disk/by-id/ata-VBOX_HARDDISK_OST1PORT200000000000' oss2
vagrant sh -u root -c 'mkdir -p /mnt/ost1' oss1 oss2
vagrant sh -u root -c 'mount -t lustre /dev/disk/by-id/ata-VBOX_HARDDISK_OST1PORT200000000000 /mnt/ost1' oss2
# verify the mount
vagrant sh -u root -c 'mount | grep lustre' oss2
```

After all the commands for each node have run successfully, use the IML GUI to scan for the filesystem:
Configuration -> Servers -> Scan for Filesystem. Use all servers.

If Successful, in the IML GUI, the filesystem will be available.

## [Setting up Clients](cd_Setting_Up_Clients.md)

---

[Top of page](#Top)
