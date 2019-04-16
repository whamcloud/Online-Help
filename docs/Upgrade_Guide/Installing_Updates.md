# Installing Updates to Integrated Manager for Lustre software

[**Upgrade Guide**](ug_TOC.md)

**Note**: Perform any OS update prior to updating the Integrated Manager
for Lustre software.

**Note**: Updates are only supported for official releases. Updates
from, or to, test releases are not specifically supported.

Due to a dependency in the update process in previous releases, please
take note of the following update path. Please perform the following
update in the order listed, based on your currently installed version of
Integrated Manager for Lustre software.

Upgrading Integrated Manager for Lustre software and restarting the manager
server will overwrite any changes previously made to the
chroma-manager.conf template. Depending on the version of IML that is running,
this template will reside in one of two places:

1. Apache Config Directory: `/etc/httpd/conf.d/chroma-manager.conf`
1. Nginx Config Directory: `/etc/nginx/conf.d/chroma-manager.conf`

Make sure to backup this configuration file before performing any upgrades or restarting the manager node.

### IML 2.x.x Upgrades

1.  If your currently installed software version is 2.0.0.0 , update to
    version 2.0.1.1 first. Then perform the following consecutive
    updates in the remaining steps.

1.  If your currently installed software version is 2.0.1.1, update to
    version 2.2.0.2 first. Then perform the following consecutive
    updates in the remaining steps.

1.  If your currently installed software version is 2.2.0.2 or later,
    update directly to version {{site.version}}.

### IML 3.x.x Upgrades

1.  If your currently installed software version is between 3.0.x and 3.1.0.2, update to
    version 3.1.1 first. Then perform the following consecutive
    updates in the remaining steps.

1.  If your currently installed software version is 3.1.1,
    update directly to version {{site.version}} using [these instructions.](../Upgrade_Guide/Upgrade_EE-3.1-el7_to_LU-LTS-el7.md)

Performing a version downgrade or rollback is not supported.

To install an update of Integrated Manager for Lustre software on the manager
server and then all file system managed servers, do the following:

1.  Stop the file system. To do this, click **Configuration** &gt;
    **File Systems**. Then under **Actions**, click **Stop**.

2.  Some servers may belong to multiple file systems. This means that if
    you stop one file system, such a server is still running in support
    of the other file system(s). Be sure to stop all file systems that
    share a server with your candidate file system.

3.  Perform the installation procedure herein: [Installing Manager
    for Lustre software](../Install_Guide/ig_ch_05_install.md#installing-integrated-manager-for-lustre-software).
    The installation will detect that this is an update and install the
    appropriate files. Use that procedure to verify successful
    installation.

4.  After the updated Integrated Manager for Lustre software is installed,
    point your web browser to the Integrated Manager for Lustre software dashboard.
    Use Chrome\* or Firefox\*. Be sure to refresh the browser cache,
    i.e., force a fresh reload of the updated dashboard.

5.  With the updated release of Integrated Manager for Lustre software
    installed on the manager server, a notification is displayed on the
    Servers page that an update is available for installation on managed
    servers. On the **Servers** page, click **Install Updates**.

6.  Each server row in the table will contain a **Selected** toggle
    button in its corresponding **Select Server** column. Select all
    servers that you wish to update and click the Install Updates
    button. This completes the update process for the manager server and
    all managed servers.

7.  When all servers have been updated, restart the file system(s) that
    were stopped for this update.

[Top of page](#installing-updates-to-integrated-manager-for-lustre-software)
