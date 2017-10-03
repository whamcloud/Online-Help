# <a name="1.0"></a>About this Document

[**Software Installation Guide Table of Contents**](ig_TOC.md)

**In this Chapter:**

- [About this Document](#about-this-document)
- [Document Purpose](#document-purpose)
- [Intended Audience](#intended-audience)
- [Conventions Used](#conventions-used)
- [Related Documentation](#related-documentation)

Document Purpose
----------------

This document provides detailed instructions for installing Intel® Manager for Lustre* software. This document:

-   Introduces Intel® Manager for Lustre* software and its capabilities

-   Introduces Intel® Manager for Lustre* software and its
     capabilities to configure and support real-time management of
     Lustre* file systems, using a GUI-based dashboard

-   Provides detailed instructions about how to configure the components
     to create a file system that meets the High Availability
     Configuration Specification (discussed herein). Conformance with
     this specification permits configuration, monitoring, and
     management of the Lustre* file system using the Intel® Manager for Lustre* software.

-   Describes the pre-installation tasks such as configuring servers,
     establishing yum repositories, configuring LNET, and also
     discusses Linux\* kernel considerations

-   Describes how to install Intel® Manager for Lustre* software

-   Describes how to configure Intel® Manager for Lustre* software

-   Describes how to add storage servers to the Lustre* file system

-   Provides troubleshooting information

Intended Audience
-----------------

This guide is intended for partners who are designing storage solutions
based on Intel® Manager for Lustre* software. Readers are
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
implemented using the Intel® Manager for Lustre* software.

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

-   *Intel® Manager for Lustre* software, Version 4.0.0
    Release Notes*

-   *Intel® Manager for Lustre* software Online Help* (accessible from
    within the GUI)

-   *Intel® Manager for Lustre* software User Guide* (a PDF verion on
    the online Help)

-   *Lustre\* Installation and Configuration using Intel® Manager for Lustre* software and OpenZFS*

-   *Configuring LNet Routers for File Systems based on Intel® Manager for Lustre* software*

-   *Installing Hadoop, the Hadoop Adapter for Intel® Manager for Lustre* software,
    and the Job Scheduler Integration *

-   *Creating an HBase Cluster and Integrating Hive on an Intel® Manager for Lustre* software File System*

-   *Hierarchical Storage Management Configuration Guide*

-   *Configuring SELinux for File Systems based on Intel® Manager for Lustre* software*

-   *Configuring Snapshots for File Systems based on Intel® Manager for Lustre* software*

-   *Upgrading a Lustre* file system to Intel® Manager for Lustre* software (Lustre* only)*

-   *Creating a Scalable File Service for Windows Networks using Intel® Manager for Lustre* software*

-   *Intel® Manager for Lustre* software Hierarchical Storage Management Framework
    White Paper*

-   *Architecting a High-Performance Storage System White Paper*Title

[Top of page](#1.0)
