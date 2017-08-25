[**Manager for Lustre\* Software Installation Guide Table of Contents**](ig_TOC.md)
# Installing Manager for Lustre\* software on Intel® Xeon Phi™ Coprocessors


**In this Chapter:**

- [Install Lustre\* client on an Intel® Xeon Phi™ Coprocessor](#install-lustre-client-on-an-intel-xeon-phi-coprocessor)
- [Configure Lustre for the Intel® Xeon Phi™ Coprocessor](#configure-lustre-for-the-intel-xeon-phi-coprocessor)


Install Lustre\* client on an Intel® Xeon Phi™ Coprocessor
----------------------------------------------------------

To install Lustre, install the following two RPMs on the Intel® Xeon
Phi™ coprocessor (not on the host).


```
# rpm –ivh lustre-client-mic-&lt;version&gt;.x86\_64.rpm

# lustre-client-mic-modules-&lt;version&gt;.x86\_64.rpm
```


In case of issues with dependencies, add the –nodeps option.

After restarting the MPSS service, the Lustre client will appear on the
coprocessor card.

Configure Lustre for the Intel® Xeon Phi™ Coprocessor
-----------------------------------------------------

Configuring Lustre for the Xeon Phi Coprocessor is easy. You only need
to specify the LNET configuration in /etc/modprobe.d/lustre.conf file.

To check configuration, enter the following commands.

\# ssh mic0

\# echo “options lnet networks=\\"o2ib0(ib0)\\"”
&gt;/etc/modprobe.d/lustre.conf

\# modprobe lustre

\# mkdir -p /mnt/lustre

\# mount.lustre &lt;MGS\_IP&gt;@o2ib0:/&lt;lustre\_FS\_name&gt;
/mnt/lustre

To make this configuration persistent across re-boots, enter the
following commands (where “X” is the card number).

\# mkdir -p /var/mpss/micX/mnt/lustrefs

\# echo 'dir /mnt/lustrefs 0755 0 0' &gt;&gt; /var/mpss/micX.filelist

\# mkdir -p /var/mpss/micX/etc/modprobe.d

\# cp /etc/modprobe.d/lustre.conf /var/mpss/micX/etc/modprobe.d/

(or just create it in /var/mpss/micX/etc/modprobe.d/)

\# echo 'file /etc/modprobe.d/lustre.conf etc/modprobe.d/lustre.conf
0644 0 0' &gt;&gt; /var/mpss/micX.filelist