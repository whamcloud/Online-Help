<a id="12.0"></a>
# Errors and troubleshooting

[**Online Help Table of Contents**](IML_Help_TOC.md)

The following topics are discussed in this chapter:

- [Unexpected file system events](#12.1)
- [Running Intel® Manager for Lustre* software diagnostics](#12.2)


## <a id="12.1"></a>Unexpected file system events

This section discusses several unwanted file system events and how Intel® Manager for Lustre* software responds to them.

<table border="1">
    <thead>
        <tr>
        <th colspan="2">A server’s connection to a storage target is lost</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>Lustre clients will block if they have requested a file from an unavailable OST. The block will continue until connection to the OST is restored and the
OST is again fully online. For OSTs that are still connected to their
servers, client access continues unaffected</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>No automatic failover. No alerts.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>Repair the connection to the target. In the meantime, the superuser may
manually fail the target over to the peer server. </td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">A server’s connection to LNet is lost</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>Lustre clients will block waiting for the connection to be re-established. Those portions of the file system that are presented by the affected server are unavailable until then.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>No automatic failover. No alerts.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>Repair the server’s connection to LNet. In the meantime, the superuser may manually fail the target over to the peer server.</td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">Manager software connection to a server (via the management network, ring0) is lost</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>No direct file system impact; the file system remains operational. However, Manger for Lustre* software can no longer manage or monitor the server.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>Alerts to administer regarding loss of network connection to server. </td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>Re-establish the management network connection to the server. </td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">A Lustre server loses connectivity with the power control device for its peer server (IPMI or PDU)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>None. The file system continues to operate normally. In the event of a peer server failure, the server that has lost connectivity to power control will be unable to power off the failed server and assume responsibility for its resources.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>No response to the loss of connectivity if the file system is operating normally. In the event of a server failure, automatic failover of Lustre targets from the failed server may be disabled.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>Repair the network link to power control (IPMI or PDU).</td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">The Intel® Manager for Lustre* software loses connection with a server’s power control device (IPMI or PDU)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>The software's ability to shut down the server is lost.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>Alerts to administer regarding loss of connection to power control device.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>Restore the connection between the Manager software server and affected server’s power control device. </td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">A crossover cable between servers is disconnected or the network is down</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>This is the loss of the ring1 network link, but the ring0 link (the management network) provides complete redundancy. The file system is not affected.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>No automatic failover. No alerts.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>Replace/reconnect the cross-over cable, restore the network.</td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">A primary server’s OS kernel crashes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>Each server is used as both a primary and secondary server. Temporarily delayed access to served storage as failover occurs.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>Peer server performs STONITH, failover occurs</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>None needed by Admin. Successful STONITH causes the server to be rebooted. </td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">LBUG, a Lustre crash on a server</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>This will also crash Linux on the affected server. Temporarily delayed access to served storage as failover occurs.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>Peer server performs STONITH, failover occurs.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>No Admin action needed.</td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">The primary server spontaneously reboots</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>Temporarily delayed access to served storage as failover occurs.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>Peer server performs STONITH, failover occurs.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>No Admin action needed.</td>
        </tr>
    </tbody>
</table>

<table border="1">
    <thead>
        <tr>
        <th colspan="2">The management network (ring0) and a peer crossover network (ring1) are both down</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Immediate file system consequences:</td>
            <td>The file system is not directly affected and client operations may continue. Affected peer servers may attempt STONITH.</td>
        </tr>
        <tr>
            <td>Manager software / Peer server response:</td>
            <td>Peer server performs STONITH and failover occurs. However, each affected server may attempt STONITH on its peer.</td>
        </tr>
        <tr>
            <td>Suggested remedies:</td>
            <td>This condition is unlikely and unstable. The superuser needs to restore network connections for the management network and the cross-over link between affected servers.</td>
        </tr>
    </tbody>
</table>

[Top of page](#12.0)

## <a id="12.2"></a>Running Intel® Manager for Lustre* software diagnostics

If Intel® Manager for Lustre* software is not operating normally and you require support from Intel® customer support, you may be asked to run chroma-diagnostics on any servers that are suspected of having problems, and/or on the server hosting the Intel® Manager for Lustre* software dashboard. The results of running the diagnostics should be attached to the ticket you are filing describing the problem. These diagnostics are described next.

**Run diagnostics**

1. Log into the server in question. Admin login is required in order to collect all desired data.
1. Enter the following command at the prompt:
```
#chroma-diagnostics
```


This command generates a compressed tar.lzma file that you can email to Intel® customer support. The following are sample displayed results of running this command. (The resulting tar.lzma file will have a different file name.)


```
Collecting diagnostic files

Detected devices
Devices monitored
Listed installed packages
Listed cibadmin --query
Listed: pcs config show
Listed: crm_mon -1r
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
Size: 16K  /var/log/diagnostics_20150623T160338_lotus-4vm15.iml.intel.com.tar.lzma

The diagnostic report tar.lzma file can be sent to Intel® Manager for Lustre* software Support for analysis.
```

You can also decompress the file and examine the results. To unpack and extract the files, use this command:

```
tar --lzma -xvpf <file_name>.tar.lzma
```

**Help for chroma-diagnostics**

Generally, if requested you should run this command without options, as this will generate the needed data. Enter 
```
chroma-diagnostics -h
```
 to see help for this command, as follows:

```
# chroma-diagnostics -h
usage: chroma-diagnostics [-h] [--verbose] [--days-back DAYS_BACK]
Run this to save a tar-file collection of logs and diagnostic output.
The tar-file created is compressed with lzma.
Sample output: /var/log/diagnostics_<date>_<fqdn>.tar.lzma
optional arguments:
 -h, --help   show this help message and exit
 --verbose, -v   More output for troubleshooting.
 --days-back DAYS_BACK, -d DAYS_BACK
Number of days back to collect logs. default is 1. 0 would mean today's logs only.
```
[Top of page](#12.0)
