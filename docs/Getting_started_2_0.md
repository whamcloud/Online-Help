[**Intel® Manager for Lustre\* Online Help Main Table of Contents**](../README.md)
# Getting started<a id="2.0"></a>

**In this section:**

- <a href="#2.1">Creating user accounts</a>
- <a href="#2.2">Setting up email notifications of alerts</a>

A high-availability Lustre file system managed by Intel® Manager for Lustre* software requires that your entire storage system configuration and all  interfaces comply with a pre-defined configuration.  For detailed information, see the section High Availability Configuration Specification in the *Intel® Enterprise Edition for Lustre\* Software Installation Guide*. Also see the guide *Lustre\* Installation and Configuration using Intel® EE for Lustre\* Software and OpenZFS*.

**Note:** All references herein to the "manager" refer to the Intel® Manager for Lustre* software.
The Intel® Manager for Lustre* software can be used to:
Create, monitor and manage high-availability Lustre* file systems, including systems running Open ZFS as the back-end.
Monitor existing Lustre* file systems that have not been configured from the manager GUI.

See the following information to get started:

- For procedures for installing the Intel® Enterprise Edition for Lustre* software, including Intel® Manager for Lustre* software, and for completing initial configuration steps, see the documentation provided by your storage solution provider. 
- To set up superuser and user accounts on Intel® Manager for Lustre* software see: <a href="#2.1">Creating user accounts</a>.
- Also see: <a href="#2.2">Setting up email notifications of alerts</a>.
- To create a new Lustre file system using Intel® Manager for Lustre* software, see: [Creating a new Lustre* file system](Creating_new_lustre_fs_3_0.md/#3.0).
- To detect and monitor an existing Lustre file system using Intel® Manager for Lustre* software, see: [Detect and monitor existing Lustre* file systems](Detect_and_monitor_existing_LFS_7_0.md/#7.0).

**WARNING:** For Lustre* file systems created and managed by Intel® Manager for Lustre* software, the only supported command line interface is the CLI provided by Intel® Manager for Lustre* software. Modifying such a Lustre file system manually from a UNIX shell will interfere with the ability of the Intel® Manager for Lustre* software to manage and monitor the file system. 

<a herf="#2.0">Top of page</a>

## Creating user accounts<a id="2.1"></a>

**Note:** Before creating user accounts, see the documentation provided by your storage solution provider for the initial setup procedure to be completed. The first superuser is created as part of that initial setup procedure.
To create user accounts:

1. At the menu bar, click the **Configuration** drop-down menu and click **Users**.
1. Click **+ Create user**. 
1. At the Create user dialogue window, select the new user's role:  
    
    a) **File system user -** A file system user has access to the full GUI, except for the Configuration drop-down menu, which is not displayed. A  user cannot create or manage a file system, but can monitor all file systems using the Dashboard, and the Alerts and Logs windows. Users log in by clicking **Login** in the upper-right corner of the screen, and log out by clicking **Logout**. 

    b) **Superuser -** A superuser has full access to the application, including the Configuration drop-down menu and all sub-menus. A superuser can create, monitor, manage, and remove file system and their components. A superuser create, modify (change passwords), and delete users. A superuser cannot delete their own account, but a superuser can create or delete another superuser. 
    
1. Fill out the remainder of the *Create user* dialogue window and click **Create**.
1. To set up email notifications of alerts for a user, see <a href="#2.2">Setting up email notifications of alerts</a>.

**More about roles**

A superuser must be logged in to perform any actions that modify the system, such as starting a file system or adding a server.

After logging in, a user can modify their own account by clicking Account near the upper-right corner of the screen. A user can set these options:

- **Details -** Username, email address, and first and last name can be changed.
- **Password -** Password can be changed and confirmed.
- **Email Notifications -** The types of events for which this account will receive emailed notifications can be selected from a checklist. If no notifications are selected, email notifications will be sent for all alerts except “Host contact alerts”. See <a href="#2.2">Setting up Email Notifications</a>.

**Note:** Unauthenticated users can access the static HTML content present on the Intel® Manager for Lustre* GUI, but the display will not be populated with current system information unless the user is authenticated. See the documentation provided by your storage solution provider for how to configure Intel® Manager for Lustre* software to require all users to log in to see any data.


## Setting up email notifications of alerts<a id="2.2"></a>

This feature lets a superuser selectively turn on and turn off email notifications of specific classes of alerts for individual users. Users can also configure this capability. The alert email has specific information as to which component is affected. 

**Note:** A mail handler needs to be established to forward alert emails before this feature will work. See *Enabling Email Notifications* in the *Intel® EE for Lustre\* Software Installation Guide*.

To set up email notifications:

1. As the user, click **Account** in the upper right corner. Then click **Email Notifications**. 
1. At the menu bar, click the **Configuration** drop-down menu and click **Users**. For the desired user, click **Edit**. Then click **Email Notifications**. 
1. At the Email Notifications window, select the alert types for which you want to turn on notifications. Alert classes are listed here:

    - **Host contact alert -** Host lost contact with a server.
    - **LNet offline alert -** LNet is offline for a server.
    - **LNet NIDs changed alert -** See [Handling Network Address Changes](Manage_maintain_HA_lustre_fs_5_0.md/#5.0).
    - **LNet NIDs changed on server <server name> -** See [Handling Network Address Changes](Manage_maintain_HA_lustre_fs_5_0.md/#5.0).
    - **Target offline alert -** A target has gone offline.
    - **Target failover alert -** A target is currently running on its secondary server.
    - **Target recovery alert -** A target is in recovery.
    - **Storage resource offline -** A monitored storage controller is offline or otherwise out of contact with chroma manager, monitoring data are not being received.
    - **Storage resource alert -** A storage plug-in has raised an alert. This alert does not reveal the exact message generated by the storage plug-in. 
1. With your selections made, click **Save Changes**. Clicking **Reset Form** returns the selections to their last saved state.

 <a herf="#2.0">Top of page</a> 

