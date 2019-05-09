# Upgrading Integrated Manager for Lustre 4.0.10.0 to Lustre {{site.lustre_version}} and Integrated Manager for Lustre {{site.version}}

[**Upgrade Guide**](ug_TOC.md)

## Upgrade Integrated Manager for Lustre

The first component in the environment to upgrade is the Integrated Manager for Lustre server and software. The manager server upgrade can be conducted without any impact to the Lustre file system services.

1. Download the latest Integrated Manager for Lustre release repo:

   ```sh
   yum-config-manager --add-repo=https://raw.githubusercontent.com/whamcloud/integrated-manager-for-lustre/v5.0.0/chroma_support.repo
   ```

1. Install the updated manager via `yum`:

   ```sh
   yum install python2-iml-manager
   ```

1. Run `chroma-config setup` to complete the installation.

1. Perform a hard refresh on the browser and verify that IML loads correctly

## Upgrade the Lustre Servers

Lustre server upgrades can be coordinated as either an online roll-out, leveraging the failover HA mechanism to migrate services between nodes and minimize disruption, or as an offline service outage, which has the advantage of usually being faster to deploy overall, with generally lower risk.

The upgrade procedure documented here describes the faster and more reliable approach, which requires that the filesystem be stopped. It assumes that the Lustre servers have been installed in pairs, where each server pair forms an independent high-availability cluster built on Pacemaker and Corosync. Integrated Manager for Lustre deploys these configurations and includes its own resource agent for managing Lustre assets, called `ocf:chroma:Target`. Integrated Manager for Lustre can also configure STONITH agents to provide node fencing in the event of a cluster partition or loss of quorum.

## Stopping the filesystem

IML requires that the filesystem(s) associated with each node to be upgraded must be stopped. Follow these steps:

1. Navigate to _Configuration->Filesystems_
1. For each filesystem listed:

   1. Click the filesystem's `Actions` button
   1. Select _Stop_

## Upgrade the OS on each server node

In order to upgrade, make sure yum is configured on each server node to pull down CentOS 7.6 packages. Next, begin the upgrade.

```bash
yum -y upgrade --exclude=python2-iml*
```

## Run the updates

Next, navigate to the server page and proceed to update each of the servers:

1. Navigate to _Configuration->Servers_
1. Each storage server should report "Updates are ready for server X"
1. Click the _Install Updates_ button
1. Select all storage servers for upgrade and begin the upgrade.

## Setting up HA

1. Once the upgrade completes, migrate the storage server to the new HA setup. Run the following on each storage server:

   ```sh
   chroma-agent convert_targets
   ```

## Summary

The filesystem(s) should now be started. Connect a client and verify that it is able to access files on the filesystem.

[top](#upgrading-integrated-manager-for-lustre-40100-to-lustre-2121-and-integrated-manager-for-lustre-5000)
