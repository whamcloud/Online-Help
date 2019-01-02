# How To Debug A Running Python Process

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

Sometimes it is helpful to debug a running python process. If you can restart the process, use remote-pdb. If not, use gdb.

## Using remote-pdb

### Setup

```bash
yum install -y epel-release
yum install -y python-pip socat
pip install remote-pdb
```

### Preparing remote-pdb

1. Locate the source for the service that is running. The source is most like under `/usr/lib/python2.7/site-packages/<service>`. Once located, open the file of interest and add the following lines to set a breakpoint:

   ```python
   from remote_pdb import RemotePdb
   RemotePdb('127.0.0.1', 4444).set_trace()
   ```

1. Restart the service:

   ```bash
   systemctl restart <servicename>
   ```

### Connecting To remote-pdb

When the current line of execution hits the breakpoint the service will pause and no further execution will take place. When this happens, the pdb session can be established by doing:

```bash
socat readline tcp:127.0.0.1:4444
```

Once connected, pdb can be used to control the execution of the service.

## Using gdb

### Setup gdb

```shell
yum install -y gdb
```

### Connecting To gdb

1. Find the pid of the service to debug.

1. `gdb python <PID_HERE>`

_Note_: When running you may notice some missing debuginfos in the output. You can copy paste the suggested command to install them and try debugging again.

### Reference

[Python Guide to debugging with GDB](https://wiki.python.org/moin/DebuggingWithGdb)

[Top](#how-to-debug-a-running-python-process)
