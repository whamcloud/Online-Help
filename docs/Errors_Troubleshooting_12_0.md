<a id="12.0"></a>
# Errors and troubleshooting

[**Online Help Table of Contents**](IML_Help_TOC.md)

The following topics are discussed in this chapter:

- [Unexpected file system events](#12.1)
- [Running Integrated Manager for Lustre* software diagnostics](#12.2)


## <a id="12.1"></a>Unexpected file system events

This section discusses several unwanted file system events and how Integrated Manager for Lustre* software responds to them.

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
        <th colspan="2">The Integrated Manager for Lustre* software loses connection with a server’s power control device (IPMI or PDU)</th>
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

## <a id="12.2"></a>Running Integrated Manager for Lustre* software diagnostics

If Integrated Manager for Lustre* software is not operating normally and you require support, you may be asked to run iml-diagnostics on any servers that are suspected of having problems, and/or on the server hosting the Integrated Manager for Lustre* software dashboard. The results of running the diagnostics should be attached to the ticket you are filing describing the problem. These diagnostics are described next.

**Run diagnostics**

1. Log into the server in question. Admin login is required in order to collect all desired data.
1. Enter the following command at the prompt:
    ```
    #iml-diagnostics
    ```

    This command generates a compressed tar.xz file that you can email to customer support. The following are sample displayed results of running this command. (The resulting tar.xz file will have a different file name.)


    ```
    sosreport (version 3.4)

    This command will collect diagnostic and configuration information from
    this CentOS Linux system and installed applications.

    An archive containing the collected information will be generated in
    /var/tmp/sos.p3Djuo and may be provided to a CentOS support
    representative.

    Any information provided to CentOS will be treated in accordance with
    the published support policies at:

    https://wiki.centos.org/

    The generated archive may contain data considered sensitive and its
    content should be reviewed by the originating organization before being
    passed to any third party.

    No changes will be made to system configuration.


    Setting up archive ...
    Setting up plugins ...
    Running plugins. Please wait ...

    Running 1/10: block...
    Running 2/10: filesys...
    Running 3/10: iml...
    Running 4/10: kernel...
    Running 5/10: logs...
    Running 6/10: memory...
    Running 7/10: pacemaker...
    Running 8/10: pci...
    Running 9/10: processor...
    Running 10/10: yum...

    Creating compressed archive...

    Your sosreport has been generated and saved in:
    /var/tmp/sosreport-iml.dev-20171017003954.tar.xz

    The checksum is: f018ba301df835862e559aa98465e9fc

    Please send this file to your support representative.
    ```

You can also decompress the file and examine the results. To unpack and extract the files, use this command:

```
tar --xz -xvpf <file_name>.tar.xz
```

**Help for iml-diagnostics**

Generally, if requested you should run this command without options, as this will generate the needed data. Enter 
```
iml-diagnostics -h
```

 to see help for this command, as follows:

```
# iml-diagnostics -h
Usage: sosreport [options]

Options:
  -h, --help            show this help message and exit
  -l, --list-plugins    list plugins and available plugin options
  -n NOPLUGINS, --skip-plugins=NOPLUGINS
                        disable these plugins
  --experimental        enable experimental plugins
  -e ENABLEPLUGINS, --enable-plugins=ENABLEPLUGINS
                        enable these plugins
  -o ONLYPLUGINS, --only-plugins=ONLYPLUGINS
                        enable these plugins only
  -k PLUGOPTS, --plugin-option=PLUGOPTS
                        plugin options in plugname.option=value format (see
                        -l)
  --log-size=LOG_SIZE   set a limit on the size of collected logs (in MiB)
  -a, --alloptions      enable all options for loaded plugins
  --all-logs            collect all available logs regardless of size
  --batch               batch mode - do not prompt interactively
  --build               preserve the temporary directory and do not package
                        results
  -v, --verbose         increase verbosity
  --verify              perform data verification during collection
  --quiet               only print fatal errors
  --debug               enable interactive debugging using the python debugger
  --ticket-number=CASE_ID
                        specify ticket number
  --case-id=CASE_ID     specify case identifier
  -p PROFILES, --profile=PROFILES
                        enable plugins selected by the given profiles
  --list-profiles       display a list of available profiles and plugins that
                        they include
  --name=CUSTOMER_NAME  specify report name
  --config-file=CONFIG_FILE
                        specify alternate configuration file
  --tmp-dir=TMP_DIR     specify alternate temporary directory
  --no-report           disable HTML/XML reporting
  -s SYSROOT, --sysroot=SYSROOT
                        system root directory path (default='/')
  -c CHROOT, --chroot=CHROOT
                        chroot executed commands to SYSROOT [auto, always,
                        never] (default=auto)
  -z COMPRESSION_TYPE, --compression-type=COMPRESSION_TYPE
                        compression technology to use [auto, gzip, bzip2, xz]
                        (default=auto)

Some examples:

 enable dlm plugin only and collect dlm lockdumps:
   # sosreport -o dlm -k dlm.lockdump

 disable memory and samba plugins, turn off rpm -Va collection:
   # sosreport -n memory,samba -k rpm.rpmva=off
```

[Top of page](#12.0)
