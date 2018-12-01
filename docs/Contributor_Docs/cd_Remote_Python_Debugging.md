# How To Debug A Running Python Process

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

Sometimes it is helpful to remotely debug a running python process. To perform remote debugging, you will need to perform the following steps:

## Setup

```bash
yum install -y epel-release
yum install -y python-pip telnet
pip install remote-pdb
```

## Preparing The Service

1. Locate the source for the service that is running. The source is most like under `/usr/lib/python2.7/site-packages/<service>`. Once located, open the file of interest and add the following lines to set a breakpoint:

   ```python
   from remote_pdb import RemotePdb
   RemotePdb('127.0.0.1', 4444).set_trace()
   ```

1. Restart the service:

   ```bash
   systemctl restart <servicename>
   ```

## Connecting To The Service

When the current line of execution hits the breakpoint the service will pause and no further execution will take place. When this happens, the pdb session can be established by doing:

```bash
telnet 127.0.0.1 4444
```

Once connected, pdb can be used to control the execution of the service.

[Top](#how-to-debug-a-running-python-process)
