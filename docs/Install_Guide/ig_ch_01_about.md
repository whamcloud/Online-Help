[**Manager for Lustre\* Software Installation Guide Table of Contents**](ig_TOC.md)
# <a name="1.0"></a>About this Document

**In this Chapter:**

- [About this Document](#about-this-document)
- [Document Purpose](#document-purpose)
- [Intended Audience](#intended-audience)
- [Conventions Used](#conventions-used)
- [Related Documentation](#related-documentation)

Document Purpose
----------------

This document provides detailed instructions for installing Manager for Lustre\* software. This document:

-   Introduces Manager for Lustre\* software and its capabilities

-   Introduces Manager for Lustre\* software and its
     capabilities to configure and support real-time management of
     Lustre* file systems, using a GUI-based dashboard

-   Provides detailed instructions about how to configure the components
     to create a file system that meets the High Availability
     Configuration Specification (discussed herein). Conformance with
     this specification permits configuration, monitoring, and
     management of the Lustre* file system using the Manager for
     Lustre\* software.

-   Describes the pre-installation tasks such as configuring servers,
     establishing yum repositories, configuring LNET, and also
     discusses Linux\* kernel considerations

-   Describes how to install Manager for Lustre\*
     software

-   Describes how to configure Manager for Lustre\* software

-   Describes how to add storage servers to the Lustre* file system

-   Provides troubleshooting information

Intended Audience
-----------------

This guide is intended for partners who are designing storage solutions
based on Manager for Lustre\* software. Readers are
assumed to be full-time Linux system administrators or equivalent who
have:

-   experience administering file systems and are familiar with storage
    components such as block storage, SAN, and LVM

-   Proficiency in setting up, administering and maintaining networks.
    Knowledge of LNET is required. Knowledge of InfiniBand\* is required
    if InfiniBand is to be used.

-   Detailed knowledge of the overall configuration of the storage
    system and the ability to verify that the configuration matches the
    configuration requirements as defined in this guide.

This document is *not intended for end users* of storage solutions
implemented using the Manager for Lustre\* software.

Conventions Used
----------------

Conventions used in this document include:

-   \# preceding a command indicates the command is to be entered as
    root

-   \$ indicates a command is to be entered as a user

-   *&lt;variable\_name&gt;* indicates the placeholder text that appears
    between the angle brackets is to be replaced with an appropriate
    value

Related Documentation
---------------------

-   *Manager for Lustre\* Software, Version 4.0.0
    Release Notes*

-   *Manager for Lustre\* Software Online Help* (accessible from
    within the GUI)

-   *Manager for Lustre\* Software User Guide* (a PDF verion on
    the online Help)

-   *Lustre\* Installation and Configuration using Manager for
    Lustre\* Software and OpenZFS*

-   *Configuring LNet Routers for File Systems based on Manager for
    Lustre\* Software*

-   *Installing Hadoop, the Hadoop Adapter for Manager for Lustre\*,
    and the Job Scheduler Integration *

-   *Creating an HBase Cluster and Integrating Hive on an Manager for
    Lustre® File System*

-   *Hierarchical Storage Management Configuration Guide*

-   *Configuring SELinux for File Systems based on Manager for
    Lustre\* Software*

-   *Configuring Snapshots for File Systems based on Manager for
    Lustre\* Software*

-   *Upgrading a Lustre* file system to Manager for
    Lustre\* software (Lustre* only)*

-   *Creating a Scalable File Service for Windows Networks using Manager for Lustre\* Software*

-   *Manager for Lustre\* Hierarchical Storage Management Framework
    White Paper*

-   *Architecting a High-Performance Storage System White Paper*Title

[Top of page](#1.0)
