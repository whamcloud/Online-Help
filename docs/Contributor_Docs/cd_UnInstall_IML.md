# Uninstalling IML

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![clustre](md_Graphics/uninstall_sm.jpg)

1.  Remove (or force remove) the agents via the GUI

    The **Remove Host Action** and **Force Remove Action** will do the following on the manager side:

    1.  Remove all manager/agent registrations including sessions and queues to prevent any future communication with the host.
    1.  Remove the hosts cerificate and revoke it's future use.
    1.  Soft delete database records for the server and related targets.

    The **Remove Host Action** makes changes to the agent side

    In the case of **ForceRemoveHostJob**, the agent side is completely untouched. This is the cause of a few problems and should be used when the communication with the agent is no longer possible.

1.  Stop the manager

    ```bash
    chroma-config stop
    ```

1.  Export the database (optional)

    ```bash
    su postgres -c 'pg_dump -f chromadb.dump chroma'
    ```

1.  Drop the database

    ```bash
    su postgres -c 'dropdb chroma'
    ```

1.  Remove the Manager

    ```bash
    chkconfig --del chroma-supervisor
    yum autoremove chroma-manager -y
    # may want if running in vagrant: yum autoremove -y fence-agents-vbox
    rm -rf /usr/share/chroma-manager/
    rm -rf /etc/yum.repos.d/chroma_support.repo
    ```

1.  Remove logs (optional)

    ```bash
    rm -rf /var/log/chroma
    ```

1.  On each agent node

    1.  Stop the agent

        ```bash
        systemctl stop chroma-agent
        ```

    1.  Remove the agent

        ```bash
        yum autoremove chroma-agent
        rm -rf /etc/yum.repos.d/Intel-Lustre-Agent.repo
        rm -rf /var/lib/chroma/
        rm -rf /var/lib/iml/
        ```

### Erase all cluster information for this server's cluster

### THIS MEANS THAT OTHER NODES IN THE CLUSTER SHOULD BE REMOVED TOO.

```shell
cibadmin -f -E
```

### Kill pacemaker and corosync

```shell
systemctl stop pacemaker
systemctl stop corosync

# --OR--

systemctl kill -s SIGKILL pacemaker corosync  # <-- Only if necessary
```

### Reset firewall setting

### Get the multicast port from the corosync setting, and used in the iptables command

```shell
grep 'mcastport' /etc/corosync/corosync.conf

rm -f /etc/corosync/corosync.conf

# Remove firewalld

systemctl status firewalld
systemctl disable firewalld

firewall-cmd --state

-- OR --

/sbin/iptables -D INPUT -m state --state new -p udp --dport MCAST-PORT -j ACCEPT
REMOVE "-A INPUT -m state --state NEW -m udp -p udp --dport MCAST-PORT -j ACCEPT" from /etc/sysconfig/iptables
REMOVE "--port=MCAST-PORT:udp" from /etc/sysconfig/system-config-firewall
```

## remove pacemaker and corosync

```shell
yum -y remove pacemaker-* corosync*
rm -f /var/lib/heartbeat/crm/* /var/lib/corosync/*
```

### unconfigure ring1 interface

```shell
ifconfig $SERVER_RING1 0.0.0.0 down
rm -f /etc/sysconfig/network-scripts/ifcfg-$SERVER_RING1
```

### unconfigure lnet

```shell
rm -f /etc/modprobe.d/iml_lnet_module_parameters.conf
```

### umount targets

```shell
umount -a -tlustre -f
```

### Reset your Linux kernel

### Check the installed kernel, if the kernel has '**lustre**' in the name, then uninstall the kernel.

```shell
rpm -qR lustre-client-modules | grep 'kernel'
```

## Use Grub to set the desired kernel

```shell
awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg
# 0 : CentOS Linux ({{site.lustre_kernel_version}}_lustre.x86_64) 7 (Core)
# 1 : CentOS Linux (3.10.0-514.6.1.el7.x86_64) 7 (Core)
# 2 : CentOS Linux (0-rescue-8018a73b69a84a48bde20d088bca3238) 7 (Core)

grub2-set-default 1

grub2-editenv list
```

Now that the non-lustre kernel has been selected, reboot the node.

### After the system reboots, remove the lustre rpm

```shell
rpm -q kernel
```

### Example Output

```shell
kernel-{{site.lustre_kernel_version}}.x86_64
kernel-{{site.lustre_kernel_version}}_lustre.x86_64

This can take a while.
yum remove kernel-{{site.lustre_kernel_version}}_lustre.x86_64
```
