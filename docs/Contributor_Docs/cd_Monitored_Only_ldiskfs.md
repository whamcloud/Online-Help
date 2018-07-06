# Creating a Monitored Only Lustre ldiskfs Filesystem on Vagrant HPC Storage Sandbox

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![ldiskfs](md_Graphics/monitored_filesystem_sm.jpg)

## Prerequisites:

Create and setup your Vagrant cluster as described in [Installing IML on Vagrant](cd_Installing_IML_On_Vagrant.md)

## Installing Lustre on each MDS and OSS Server

Lustre can now be installed on each mds and oss node.

```bash
vagrant provision mds1 mds2 oss1 oss2 --provision-with install-lustre-ldiskfs
```

## Creating a monitored only ldiskfs based Lustre filesystem

Run the following vagrant provision script to setup the ldiskfs monitored only filesystem:

```bash
vagrant provision mds1 mds2 oss1 oss2 --provision-with create-monitored-ldiskfs-filesystem
```

After the provisioning script runs successfully, use the IML GUI to scan for the filesystem:

> Configuration -> Servers -> `Detect File Systems`. 

Click the `Select All` button to select all servers and finally, click on the `Detect File Systems` button to initiate the scan. The filesystem will be listed on the `filesystems` page when the scan completes.

## Setting up Clients

Clients can be added once the filesystem detection completes. Refer to the following document to [setup clients](cd_Setting_Up_Clients.md) on the new filesystem.

---

[Top of page](#creating-a-monitored-only-lustre-ldiskfs-filesystem-on-vagrant-hpc-storage-sandbox)
