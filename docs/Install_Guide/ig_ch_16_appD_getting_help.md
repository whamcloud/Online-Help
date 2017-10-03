# <a name="1.0"></a>Getting Help

[**Software Installation Guide Table of Contents**](ig_TOC.md)

*For partners*: If you encounter a problem with Intel® Manager for Lustre* software or storage, and you
require support from your Intel® technical support representative, then
to help expedite resolution of the problem, please do the following:

1.  [Run chroma diagnostics](#run-chroma-diagnostics).

2.  [Submit a ticket](#submit-a-ticket).

Run chroma diagnostics
----------------------

Run chroma-diagnostics on any of the servers that you suspect may be
having problems, and on the server hosting the Intel® Manager for Lustre*
software dashboard. Chroma-Diagnostics generates a compressed
tar.lzma file that you should attach to your JIRA ticket.
To run chroma-diagnostics:

1.  Log into the server in question as Admin. Admin login is required in
    order to collect all desired data.

2.  Enter the following command at the prompt:

    ```
# chroma-diagnostics
```
The following results are displayed after running this command. (The resulting tar.lzma file will have a different file name.)
```
Collecting diagnostic files
Detected devices
Devices monitored
Listed installed packages
Listed cibadmin --query
Listed: pcs config show
Listed: crm\_mon -1r
Finger printed Intel® Manager for Lustre* software installation
Listed running processes
listed PCI devices
listed file system disk space.
listed cat /proc/cpuinfo
listed cat /proc/meminfo
listed cat /proc/mounts
listed cat /proc/partitions
Listed hosts
Copied 1 log files.
Compressing diagnostics into LZMA (archive)
Diagnostic collection is completed.
Size: 16K
/var/log/diagnostics\_20151006T160338\_lotus-4vm15.iml.intel.com.tar.lzma
```


1.  You can also decompress the file and examine the results. To unpack
    and extract the files, use this command:

    ```
# tar --lzma -xvpf <file_name>.tar.lzma
```


1.  If desired, the following command returns help for chroma
    diagnostics:

    ```
# chroma-diagnostics -h
```


Submit a ticket
---------------

You can submit a ticket using the Jira issue tracking system. Attach the
chroma diagnostics log report to the ticket.

1.  Log in to the Jira dashboard at:
    <https://jira.hpdd.intel.com/secure/Dashboard.jspa>

2.  In the upper right corner, select **+ Create Issue**.

3.  Select the project that was issued by your Intel® account manager.

For any other issues, contact your product manager or sales
representative.

*For end-users*: For assistance with this product, contact your storage
solution provider.

[Top of page](#1.0)