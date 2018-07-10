# <a name="Top"></a>Setting up Power Control

Power control can be configured once all of the managed servers have been added successfully and the network interfaces have been updated. To do this, ensure `/usr/local/bin` is added to the PATH environment variable on the admin / host node. This can be added to a shell initialization script that will be sourced when a new session is created (such as ~/.bash_profile):

```bash
 export PATH="$PATH:/usr/local/bin"
```

Next, install `fence-agents-vbox` on the `adm` node and on all of the server nodes:

```bash
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

Once completed, navigate to `Configuration->Power Control`. Add the following entries for each server:

|Server|	PDU |
|--------|-------|
| mds1.lfs.local|mds1 |
| mds2.lfs.local|mds2 |
| oss1.lfs.local|oss1 |
| oss2.lfs.local|oss2 |

Initially, each entry will highlight with a light orange background. Wait for 30 seconds and refresh the page; each entry will now be green. Your power control is now setup.

---
[Top of page](#Top)