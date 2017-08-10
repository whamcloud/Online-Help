[**Intel® Enterprise Edition for Lustre\* Software Installation Guide Table of Contents**](ig_TOC.md)
# Installing Lustre on SUSE Linux Enterprise Server

Intel® EE for Lustre\* software may be installed on file system servers
and clients running SUSE Linux Enterprise version 11 with SP4, and on
clients only running SLES12 with SP1. Note that for SLES, the Intel®
Manager for Lustre\* software *is not supported or installed*. Automatic
configuration or monitoring of Lustre file systems using the Intel®
Manager for Lustre\* dashboard is not supported.

The overall release tarball is ee-contrib-3.1.1.0.tar.gz. To install
Lustre manually on SUSE Linux Enterprise, use these packages:

-   SLES e2fsprogs packages: ee-contrib-3.1.1.0/sles11/
    sles11-e2fsprogs-1.42.13.wc5-bundle.tar.gz

-   SLES Lustre server packages:
    ee-contrib-3.1.1.0/sles11/sles11-lustre-server-2.7.19.10-bundle.tar.gz

-   SLES Lustre client packages: ee-contrib-3.1.1.0/sles11/
    sles11-lustre-client-2.7.19.10-bundle.tar.gz

To install Lustre manually on clients, running SLES version 12, install
this package:

-   SLES Lustre client packages:
    ee-contrib-3.1.1.0/sles12/sles12-lustre-client-2.7.19.10-bundle.tar.gz

For information regarding installing and configuring Lustre, see Part II
of the Lustre Operations Manual. This is available at the following URL.
If this page does not load, copy and paste it into your browser.

https://build.hpdd.intel.com/job/lustre-manual/lastSuccessfulBuild/artifact/lustre_manual.xhtml#part.installconfig