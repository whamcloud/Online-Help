[**Manager for Lustre\* Software Installation Guide Table of Contents**](ig_TOC.md)
# <a name="1.0"></a>Creating a Managed Lustre* File System

**In this Chapter:**

- [Adding Storage Servers to a Lustre* File System](#adding-storage-servers-to-a-lustre-file-system)
- [Administering a Lustre* File System](#administering-a-lustre-file-system)

After Manager for Lustre\* software is installed, point your web
browser to the Manager for Lustre\* dashboard. Use Chrome\* or
Firefox\*.

For complete instructions on adding servers, configuring LNET, assigning
primary and failover servers, configuring PDUs or IPMI, and creating a
Lustre* file system, see the Manager for Lustre\* online Help.

Adding Storage Servers to a Lustre* File System
----------------------------------------------

Adding a storage server consists of identifying the server to
Manager for Lustre\* software, using either the manager GUI or the
Manager for Lustre\* command line interface. A server can be
added to an existing file system that was previously discovered and is
visible to Manager for Lustre\* software in monitor-only mode,
or a server can be added to a managed, HA file system created using
Manager for Lustre\* software.

For managed, HA file systems, when the server is identified, the
Manager for Lustre\* agent, Manager for Lustre\* software,
and specific dependencies (e.g. for Corosync and Pacemaker) are
automatically deployed to the new storage server. This simplifies
software installation and avoids possible errors.

When the above software is automatically installed on a server, the
server becomes capable of running Lustre* services for attached storage
targets like the MGT, MDT, and OSTs, thereby acting as a gateway between
these targets and the network.

The Lustre* file system on the storage servers is configured from the
Manager for Lustre\* software GUI, or the supported command
line interface.

Storage servers are typically deployed in a high availability (HA)
configuration with shared storage. When a server becomes unavailable,
Lustre* services for targets that were running on that server are started
on another server attached to the same storage (known as “failover”).

For complete instructions on adding servers, assigning primary and
failover servers, configuring PDUs or IPMI, and creating a Lustre* file
system, see the Manager for Lustre\* online Help.

**Note**: Installing Manager for Lustre\* software automatically
disables SELinux on all storage servers, because the Lustre* file system
software is not compatible with SELinux. Installation also configures
firewalls on the manager and storage servers.

Administering a Lustre* File System 
-----------------------------------

**WARNING**: To manage Lustre* file systems from the command line, you must use the Manager for Lustre\* command line interface (CLI).

**WARNING**: Modifying a file system manually from a shell on a storage
server will interfere with the ability of the Manager for
Lustre\* software to manage and monitor the file system.

Storage servers created in the manager GUI can
be managed using the manager GUI or the command line interface. For
information about using the CLI, see the Manager for Lustre\*
online Help topic*, Using the command line interface*.

[Top of page](#1.0)