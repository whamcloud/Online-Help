# <a name="1.0"></a>Introducing the Integrated Manager for Lustre software

[**Software Installation Guide Table of Contents**](ig_TOC.md)

**In this Chapter:**

- [What is Integrated Manager for Lustre software?](#what-is-manager-for-lustre-software)
- [What is Management Mode?](#what-is-management-mode)
- [What is Monitor-only Mode?](#what-is-monitor-only-mode)
- [The Configuration Page in Monitor-only mode](#the-configuration-page-in-monitor-only-mode)
- [Building a Lustre Storage Solution over a ZFS File System](#building-a-lustre-storage-solution-over-a-zfs-file-system)

Integrated Manager for Lustre software, when integrated with
Linux, aggregates a range of storage hardware into a single Lustre
file system that is well proven for delivering fast IO to applications
across high-speed network fabrics, such as InfiniBand\* and Ethernet.

Lustre is a global, single-namespace file system architecture that
allows parallel access by many clients to all the data in the file
system across many servers and storage devices. Designed to take
advantage of the reliability features of enterprise-class storage
hardware, Integrated Manager for Lustre software provides high availability
features including redundant servers with storage failover. Metadata and
data are stored on separate servers to allow each system to be optimized
for different workloads.

A high-availability Lustre file system managed by Integrated Manager for Lustre 
software requires that your entire storage system configuration
and all interfaces comply with the High Availability Configuration
Specification presented in this guide.

If you are creating a Lustre file system that will use OpenZFS as the
backend, see the guide *Lustre Installation and Configuration using
Integrated Manager for Lustre software and OpenZFS*.

What is Integrated Manager for Lustre software Software?
-----------------------------------------------------

Integrated Manager for Lustre software greatly simplifies configuring, creating,
monitoring, and managing one or more Lustre file systems from either the
manager GUI, or the associated command line interface (CLI).

RestAPI plugins can further extend the functionality of ML. Such
plugins might include real-time storage monitoring that let you track
Lustre file system usage, performance metrics, events, and errors at the
Lustre level.

What is Management Mode?
------------------------

The Integrated Manager for Lustre software lets you create and manage
new high-availability (HA) Lustre file systems from its GUI. For each HA
file system, the GUI and dashboard let you create, monitor, and manage
all servers and their respective targets. The software lets you define
failover servers to support HA. RAID-based fault tolerance for storage
devices is implemented independent of Integrated Manager for Lustre software. 
Software RAID (MDRAID) disk discovery is not supported.

To provide robust HA support, Integrated Manager for Lustre software
automatically configures Corosync and Pacemaker, and takes advantage of
IPMI or PDUs to support server failover. Note that Logical Volume
Manager (LVM) is not supported in [Management
mode](#what-is-management-mode), but is supported in [Monitor
mode](#what-is-monitor-only-mode).

**Note**: Managed HA support *requires* that your entire storage system
configuration and all interfaces be compliant with a *known
configuration*. See the [High Availability Configuration
Specification](ig_ch_03_building.md) for more information.

What is Monitor-only Mode?
--------------------------

Monitor-only mode allows you to “discover” a working Lustre file system.
Using Integrated Manager for Lustre software, you can then monitor the
file system at the Integrated Manager for Lustre software dashboard. All of the
charts presented on the manager dashboard to monitor performance and
statistics, are also available in monitor-only mode.

Monitor-only mode is for file systems that do not fully conform to the
High Availability Configuration Specification. In this situation, the
Corosync and Pacemaker configuration modules provided with
Integrated Manager for Lustre software are not automatically deployed. This means
that Integrated Manager for Lustre software cannot configure the file
system for server failover. Note that Logical Volume Manager (LVM) is
not supported in [Management mode](#what-is-management-mode), but is
supported in [Monitor mode](#what-is-monitor-only-mode).

### The Configuration Page in Monitor-only mode

The Configuration page presented by Integrated Manager for Lustre software
is designed primarily to enable designers to create Lustre file
systems with server failover capability, but this capability is not
supported in monitor-only mode. However, many of the features provided
on the Configuration page are also directly useful for monitor-only file
systems.

Building a Lustre Storage Solution over a ZFS File System
---------------------------------------------------------

If your intent is to build a high-availability, Lustre storage solution
over an existing ZFS, Integrated Manager for Lustre software supports this
configuration. However, the installation and configuration of such a
system is not described in this guide. Please see the document:
*Lustre Installation and Configuration using
Integrated Manager for Lustre software and OpenZFS*.

[Top of page](#1.0)