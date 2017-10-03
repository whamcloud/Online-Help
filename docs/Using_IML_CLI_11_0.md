<a id="11.0"></a>
# Using the Intel® Manager for Lustre* software command line interface

[**Online Help Table of Contents**](IML_Help_TOC.md)

Intel® Manager for Lustre* software includes a command line interface (CLI) which can be used instead of the GUI to communicate with the Representational State Transfer (REST)-based API underlying the software GUI. The CLI is intended to be used in shell scripts by superusers and power users.

**WARNING**: For Lustre* file systems created and managed by Intel® Manager for Lustre* software, the only supported command line interface is the CLI provided byIntel® Manager for Lustre* software. Modifying such a Lustre* file system manually from a UNIX shell will interfere with the ability of the Intel® Manager for Lustre* software to manage and monitor the file system.

This chapter provides the following procedures and information:

- [Accessing the command line interface](#11.1)
- [Creating a configuration file with login information](#11.2)
- [Getting help for CLI commands](#11.3)
- [CLI command examples](#11.4)


## <a id="11.1"></a>Accessing the command line interface

To access the Intel® Manager for Lustre* software CLI:

1. Use SSH to log into the manager server as the UNIX superuser. Log in using your superuser account. 
1. Enter CLI commands on the UNIX command line.

**WARNING**: To manage Lustre* file systems from the command line, you must use the Intel® Manager for Lustre* software command line interface. Modifying a file system manually from a shell on a storage server will interfere with the ability of Intel® Manager for Lustre* software to manage and monitor the file system.

[Top of page](#11.0)


## <a id="11.2"></a>Creating a configuration file with login information

Although a superuser can enter a login name and password on the command line each time the Intel® Manager for Lustre* software CLI is used, accessing login information in a configuration file is more convenient and more secure. 

To set up an optional configuration file, complete these steps:

1. Create a configuration file $HOME/.chroma on the server hosting Intel® Manager for Lustre* software.
1. Edit the file to include content as shown below:
```
[chroma]
username = <user name of file system administrator>
password = <password>
```

**Note**: To minimize security risks, modify the permissions of the .chroma file to allow only the file owner to read from and write to it, using:
```
$ chmod 0600 ~/.chroma
```
[Top of page](#11.0)

## <a id="11.3"></a>Getting help for CLI commands

To access documentation for the CLI commands, use the chroma –h command shown next:

```
# chroma –-help
usage: chroma [--api_url API_URL] [--username USERNAME] 
 [--password PASSWORD]
 [--output {human,json,xls,yaml,csv,tsv,html,xlsx,ods}]
 [--nowait] [--help]
 
 {volume,fs,target,tgt,vol,cfg,oss,mgt,ost,nid,server,
 mgs,srv,filesystem,mds,configuration,mdt}
```

 ...

CLI
positional arguments:
 
```
{volume,fs,target,tgt,vol,cfg,oss,mgt,ost,nid,server,mgs,srv,
 filesystem,mds,configuration,mdt}
 configuration (cfg)
 dump, load
 filesystem (fs) list, show, add, remove, start, stop, 
 detect, mountspec
 nid update, relearn
 server (srv, mgs, mds, oss)
 show, list, add, remove
 target (tgt, mgt, mdt, ost)
 list, show, add, remove, start, stop
 volume (vol) list, show

```

optional arguments:

```
 --api_url API_URL Entry URL for Chroma API
 --username USERNAME Chroma username
 --password PASSWORD Chroma password
 --output, -o {human,json,xls,yaml,csv,tsv,html,xlsx,ods}
 Output format
 --nowait, -n Don't wait for jobs to complete
 --help, -h Show this help message and exit
```


To view the command options available specific to a file system, enter:

```
# chroma filesystem --help
usage: chroma filesystem [-h]
 
 {detect,show,list,stop,remove,start,add,
 context,mountspec}
```

positional arguments:

```
 {detect,show,list,stop,remove,start,add,context,mountspec}
 list list all file systems
 show show a filesystem
 add add a filesystem
 remove remove a filesystem
 start start a filesystem
 stop stop a filesystem
 detect detect all file systems
 mountspec mountspec for filesystem
 context filesystem_name action (e.g. ost-list, 
 vol-list, etc.)
```


optional arguments:

```
 -h, --help show this help message and exit

To show help for the server argument, enter:
# chroma server-show --help
usage: chroma server show [-h] server
```


positional arguments:

```
 server
```


optional arguments:

```
 -h, --help show this help message and exit
```
[Top of page](#11.0)

## <a id="11.4"></a>CLI command examples

This section includes examples of common operations executed using the CLI.

**Note**: Operations that modify the file system configuration can only be executed by a file system superuser. For a convenient way to access login information in a configuration file, see [Creating a configuration file containing login information](#11.2). If a configuration file containing the superuser’s login information does not exist, include the --username and --password parameters in the CLI command.

To add the file system jovian to Intel® Manager for Lustre* software, enter:

```
# chroma fs-add jovian --mgt autonoe:/dev/mapper/LustreVG-mgs --mdt autonoe:/dev/mapper/
LustreVG-mdt --ost thyone:/dev/mapper/LustreVG-ost0 --ost thyone:/dev/mapper/LustreVG-ost1 --ost thyone:/dev/mapper/
LustreVG-ost2 --ost thyone:/dev/mapper/LustreVG-ost3
```


To add a new server to be monitored and managed:

```
# chroma server-add thyone.jovian.private --server_profile base_managed
Setting up host thyone.jovian.private: Finished
```


To add a new server to be monitored only:

```
# chroma server-add thyone.jovian.private --server_profile base_monitored
Setting up host thyone.jovian.private: Finished
```


To list known servers:

```
# chroma server-list
| id | fqdn | state | nids | last_contact |
| 4 | autonoe.jovian.private | lnet_up | 10.141.255.2@tcp0 | 20:10:46 |
| 5 | thyone.jovian.private | lnet_up | 10.141.255.3@tcp0 | 20:10:46 |
```


To list known OSTs:

```
# chroma ost-list
| id | name | state | primary_path |
| 3 | jovian-OST0002 | mounted | thyone.jovian.private:/dev/mapper/LustreVG-ost0 |
| 4 | jovian-OST0001 | mounted | thyone.jovian.private:/dev/mapper/LustreVG-ost1 |
| 5 | jovian-OST0000 | mounted | thyone.jovian.private:/dev/mapper/LustreVG-ost2 |
| 6 | jovian-OST0003 | mounted | thyone.jovian.private:/dev/mapper/LustreVG-ost3 |
```

To list targets on a given server, limiting to primary targets:

```
# chroma server autonoe target-list --primary
| id | name | state | primary_path |
| 1 | MGS | mounted | autonoe.jovian.private:/dev/mapper/LustreVG-mgs |
| 2 | jovian-MDT0000 | mounted | autonoe.jovian.private:/dev/mapper/LustreVG-mdt |
```
To obtain client mount information:

```
# chroma filesystem-mountspec jovian
10.141.255.2@tcp0:/jovian
```


To detect existing (non-managed) Lustre* file systems on servers that have been added to the Command Center, enter: 

```
# chroma filesystem-detect
```
[Top of page](#11.0)