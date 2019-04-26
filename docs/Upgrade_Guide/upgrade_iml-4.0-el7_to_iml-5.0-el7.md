# Upgrading Integrated Manager for Lustre 4.0.10.0 to Lustre {{site.lustre_version}} and Integrated Manager for Lustre {{site.version}}

## Upgrade Integrated Manager for Lustre

The first component in the environment to upgrade is the Integrated Manager for Lustre server and software. The manager server upgrade can be conducted without any impact to the Lustre file system services.

1. Download the latest Integrated Manager for Lustre release repo:

   ```sh
      yum-config-manager --add-repo=yum-config-manager --add-repo=https://raw.githubusercontent.com/whamcloud/integrated-manager-for-lustre/v5.0.0/chroma_support.repo
   ```

1. Install the updated manager via `yum`:

   ```sh
   yum install python2-iml-manager
   ```

1. Run `chroma-config setup` to complete the installation.

## Upgrade the Lustre Servers

Lustre server upgrades can be coordinated as either an online roll-out, leveraging the failover HA mechanism to migrate services between nodes and minimize disruption, or as an offline service outage, which has the advantage of usually being faster to deploy overall, with generally lower risk.

The upgrade procedure documented here shows how to execute the upgrade while the file system is online. It assumes that the Lustre servers have been installed in pairs, where each server pair forms an independent high-availability cluster built on Pacemaker and Corosync. Integrated Manager for Lustre deploys these configurations and includes its own resource agent for managing Lustre assets, called `ocf:chroma:Target`. Integrated Manager for Lustre can also configure STONITH agents to provide node fencing in the event of a cluster partition or loss of quorum.

This documentation will demonstrate how to upgrade a singleLustre server HA pair. The process needs to be repeated for all servers in the cluster. It is possible to execute this upgrade while services are still online, with only minor disruption during critical phases. Nevertheless, where possible it is recommended that the upgrade operation is conducted during a planned maintenance window with the file system stopped.

In the procedure, "Node 1" or "first node" will be used to refer to the first server in each HA cluster to upgrade, and "Node 2" or "second node" will be used to refer to the second server in each HA cluster pair.

Upgrade one server at a time in each cluster pair, starting with Node 1, and make sure the upgrade is complete on one server before moving on to the second server in the pair.

The software upgrade process requires super-user privileges to run. Login as the `root` user or use `sudo` to elevate privileges as required to complete tasks.

**Note:** It is recommended that Lustre clients are quiesced prior to executing the upgrade. This reduces the risk of disruption to the upgrade process itself. It is not usually necessary to unmount the Lustre clients, although this is a sensible precaution.

1. Load up the IML GUI
1. Stop all filesystems via the IML GUI
1. Each storage server should report "Updates are ready" on the servers page
1. Select all storage servers for upgrade and begin the upgrade.
1. Once the upgrade completes we need to migrate the storage server to the new HA setup. On each storage server:

   ```sh
   chroma-agent convert_targets
   ```

1. Start the filesystem back up
