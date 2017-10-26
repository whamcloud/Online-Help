# <a name="Top"></a>Setting up Power Control

Power control can be configured once all of the managed servers have been added successfully and the network interfaces have been updated. To do this, install `fence-agents-vbox` on the `adm` node and on all of the server nodes:

```
vagrant sh -c "sudo yum install -y fence-agents-vbox" adm oss1 oss2 mds1 mds2
```

Next, ssh into the `adm` node and install the "fake" IPMI hardware:


```bash
cd /usr/share/chroma-manager
python scripts/fake_ipmi_vbox.py
    # Enter "10.0.2.2" for the IP
    # Enter your computer username
    # Enter your computer password
```

**Note** There is currently a bug that causes the fake_ipmi_vbox.py script to fail on the first run; the process will hang indefinitely. 

To fix this, hit `ctrl+Z` to suspend the process. 

Next, run `ps aux | grep "fake_ipmi"` to get the process number and kill the process by executing, `kill -9 <processId>`. 

Once the process has been destroyed,

Navigate to `Configuration->Power Control`. Add the following entries for each server:

|Server|	PDU |
|--------|-------|
| mds1.lfs.local|mds1 |
| mds2.lfs.local|mds2 |
| oss1.lfs.local|oss1 |
| oss2.lfs.local|oss2 |

Initially, each entry will highlight with a light orange background. Wait for 30 seconds and refresh the page; each entry will now be green. Your power control is now setup.

---
[Top of page](#Top)