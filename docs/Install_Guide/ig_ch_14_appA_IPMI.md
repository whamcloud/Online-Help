[**Manager for Lustre\* Software Installation Guide Table of Contents**](ig_TOC.md)
# Appendix A - IPMI Checks

Procedures provided in this appendix can be used to establish a level of
confidence that your IPMI implementation is functional. Note that IPMI
implementations can be problematic, and while these procedures can
provide a level of confidence, absolute assurance from Intel® that
your particular IPMI implementation will operate error-free is not
possible.

IPMI Platform Check
-------------------

Perform the following steps:

1.  Identify the BMC model number on all servers.

2.  Identify the BMC firmware revision on all servers.

3.  Ensure that the BMC model number and firmware revision are the same
    on all servers.

4.  Using the fence\_ipmilan utility provided by the fence-agents RPM on
    Red Hat/CentOS, verify that the following commands complete
    successfully:


a.  fence\_ipmilan -a &lt;BMC ADDRESS&gt; -l &lt;BMC USERNAME&gt; -p
    &lt;BMC PASSWORD&gt; -o monitor

b.  fence\_ipmilan -a &lt;BMC ADDRESS&gt; -l &lt;BMC USERNAME&gt; -p
    &lt;BMC PASSWORD&gt; -o status

c.  fence\_ipmilan -a &lt;BMC ADDRESS&gt; -l &lt;BMC USERNAME&gt; -p
    &lt;BMC PASSWORD&gt; -o reboot

d.  fence\_ipmilan -a &lt;BMC ADDRESS&gt; -l &lt;BMC USERNAME&gt; -p
    &lt;BMC PASSWORD&gt; -o off

e.  fence\_ipmilan -a &lt;BMC ADDRESS&gt; -l &lt;BMC USERNAME&gt; -p
    &lt;BMC PASSWORD&gt; -o on

This process could run some combination of these commands over an
extended period (e.g., monitor every 30 seconds or so with periodic
power commands), for each BMC.