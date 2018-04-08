# <a name="Top"></a>Uninstalling IML

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![clustre](md_Graphics/uninstall_sm.jpg)

## **Step 1**: Uninstall the IML Manager

### Stop the manager

```bash
chroma-config stop
```

### Export the database (optional)

```bash
su - postgres
pg_dump -f chromadb.dump chroma
logout
```

### Drop the database (optional)

```bash
su - postgres
dropdb chroma
logout
```

### Remove the Manager

```bash
chkconfig --del chroma-supervisor
yum clean all --enablerepo=*
yum autoremove -y chroma-manager
# may want if running in vagrant: yum autoremove -y fence-agents-vbox
rm -rf  /usr/lib/iml-*
rm -rf /usr/share/chroma-manager/
rm -rf /usr/lib/python2.7/site-packages/chroma*
rm -rf /var/cache/yum/x86_64/7/chroma-manager
rm -rf /var/cache/yum/x86_64/7/managerforlustre-manager-for-lustre
rm -rf /etc/yum.repos.d/chroma_support.repo
```

### Optionally, Remove logs

```shell
rm -rf /var/log/chroma
```

---

# **Step 2**: Uninstall the IML Agent

### **Remove Host Action** and **Force Remove Action** will do the following on the manager side:
1. Remove all manager/agent registrations including sessions and queues to prevent any future communication with the host.
1. Remove the hosts cerificate and revoke it's future use.
1. Remove database records for the server and related targets.

### The **Remove Host Action** makes changes to the agent server side. 

In the case of **ForceRemoveHostJob**, the agent side is completely untouched. This is the cause of a few problems and should be used when the communication with the agent is no longer possible. If you do use it, this script can be used to clean up the agent side. You will need to get a shell to the agent machine and issue these commands.

### Note also that although the Remove Host Action will remove IML from the agent, it doesn't do a complete job.

### There are some installed artifacts that are not removed. This script can be used to make sure the server is completely uninstalled.

### Some of the actions below are optional.  If you plan on reinstalling the agent, you may choose not to do the optional items.

### Stop and deregister server
```
service chroma-agent stop
/sbin/chkconfig --del chroma-agent

```

### Remove agent software
```
yum remove -y chroma-agent chroma-agent-management iml_sos_plugin iml-device-scanner python2-iml-common* lustre-iokit lustre-osd-ldiskfs-mount lustre-osd-zfs-mount
rm -rf /etc/yum.repos.d/Intel-Lustre-Agent.repo
rm -rf /var/lib/chroma/
rm -rf /var/lib/iml/
rm -rf /etc/yum.repos.d/Intel-Lustre-Agent.repo
rm -rf /usr/lib/python2.7/site-packages/chroma_agent*
```

### Unconfigure NTP
```
mv -f /etc/ntp.conf.pre-chroma /etc/ntp.conf
```

### Erase all cluster information for this server's cluster
### THIS MEANS THAT OTHER NODES IN THE CLUSTER SHOULD BE REMOVED TOO.
```
cibadmin -f -E
```

### Kill pacemaker and corosync
```
systemctl stop pacemaker
systemctl stop corosync

# --OR--  

killall -9 pacemaker\; killall -9 corosync  # <-- Only if necessary
```

### Reset firewall setting
### Get the multicast port from the corosync setting, and used in the iptables command
```
grep 'mcastport' /etc/corosync/corosync.conf

rm -f /etc/corosync/corosync.conf

Remove firewalld

systemctl status firewalld
systemctl disable firewalld

firewall-cmd --state

-- OR --

/sbin/iptables -D INPUT -m state --state new -p udp --dport MCAST-PORT -j ACCEPT
REMOVE "-A INPUT -m state --state NEW -m udp -p udp --dport MCAST-PORT -j ACCEPT" from /etc/sysconfig/iptables
REMOVE "--port=MCAST-PORT:udp" from /etc/sysconfig/system-config-firewall
```

## remove pacemaker and corosync
```
yum -y remove pacemaker-* corosync* 
rm -f /var/lib/heartbeat/crm/* /var/lib/corosync/*
```

### unconfigure ring1 interface
```
ifconfig $SERVER_RING1 0.0.0.0 down
rm -f /etc/sysconfig/network-scripts/ifcfg-$SERVER_RING1
```

### unconfigure lnet
```
rm -f /etc/modprobe.d/iml_lnet_module_parameters.conf
```

### umount targets
```
umount -a -tlustre -f
```

### Reset your Linux kernel
### Check the installed kernel, if the kernel has '**lustre**' in the name, then uninstall the kernel.
```
rpm -qR lustre-client-modules | grep 'kernel'
```

# Use Grub to set the desired kernel
```
awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg
# 0 : CentOS Linux ({{site.lustre_kernel_version}}_lustre.x86_64) 7 (Core)
# 1 : CentOS Linux (3.10.0-514.6.1.el7.x86_64) 7 (Core)
# 2 : CentOS Linux (0-rescue-8018a73b69a84a48bde20d088bca3238) 7 (Core)

grub2-set-default 1

grub2-editenv list
```

Now that the non-lustre kernel has been selected, reboot the node.

### After the system reboots, remove the lustre rpm
```
rpm -q kernel
```

### Example Output:
```
kernel-{{site.lustre_kernel_version}}.x86_64
kernel-{{site.lustre_kernel_version}}_lustre.x86_64

This can take a while.
yum remove kernel-{{site.lustre_kernel_version}}_lustre.x86_64
```

---
[Top of page](#Top)
