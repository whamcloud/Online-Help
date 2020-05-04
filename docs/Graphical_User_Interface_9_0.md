# Graphical User Interface

[**Online Help Table of Contents**](IML_Help_TOC.md)

This help page details the graphical user interface for the Integrated Manager for Lustre software embedded in EXAScaler. Click a desired topic.

- [Dashboard](#9.1)
  - [Login](#10.1.1)
  - [Management menu](#10.1.2)
  - [Breadcrumb navigation](#9.8)
- [Servers](#10.2)
  - [Server actions](#10.2.1)
  - [Server volumes](#10.2.2)
  - [Server dashboard](#10.2.3)
- [Filesystems](#10.3)
  - [Filesystem actions](#10.3.1)
  - [Filesystem details](#10.3.2)
  - [Filesystem dashboard](#10.3.3)
  - [MGT dashboard](#10.3.4)
  - [MDT dashboard](#10.3.5)
  - [OST dashboard](#10.3.6)
- [Users](#9.3.6)
- [Logs](#9.5)
- [Activities](#9.6)

## <a id="9.1"></a>Dashboard

Dashboard is the first view that you see on starting a new session in the GUI. You can also navigate to this view from any other view by clicking **Dashboard** at the top or on the breadcrumbs trail.

<a id="f11.1"></a>
![md_Graphics/dashboard.png][f11.1]

You will see a portable, "sandwich" view for all browser windows less than 1024 pixels in width.

<a id="f11.1.1"></a>
![md_Graphics/dashboard-sandwich.png][f11.1.1]

The Dashboard view displays four charts with usage and performance data aggregated at several levels for monitored or managed filesystems:

- **Filesystem Space Usage**: Used vs available space across all filesystems.
- **I/O Performance**: Throughput and IOPS with day, 2 days, and week scaling.
- **OST Balance**: Percentage points interpreting space usage on each OST in the cluster.
- **LNet Performance**: Filesystem network speed with day, 2 days, and week scaling.

Note that monitored filesystems do not support failover of their targets through the GUI.

[Top of page](#Graphical-User-Interface)

### <a id="10.1.1"></a>Login

If you are a filesystem administrator, log in to see a list of resources and the Management menu, as well as logs for the filesystem cluster. When you log in, besides seeing the default Dashboard view, you can select to monitor and manage individual filesystems and servers.

<a id="f11.1.2"></a>
![md_Graphics/dashboard-login.png][f11.1.2]

[Top of page](#Graphical-User-Interface)

### <a id="10.1.2"></a>Management menu

The Management menu appears at the top of the GUI page after [login](#10.1.1). From there, you can click a resource to jump to its details and do the various management actions on the resource. The list of resources on the left, which also appears after login, mirrors most of the Management menu and makes it easy to drill to a particular resource.

<a id="f11.1.3"></a>
![md_Graphics/mgmt-menu.png][f11.1.3]

[Top of page](#Graphical-User-Interface)

### <a id="9.8"></a>Breadcrumb navigation

Breadcrumb navigation lets you see where in the hierarchy of the GUI you currently are.

![md_Graphics/breadcrumbs.png][f9.27]

Breadcrumbs display a path outlining the steps taken to arrive at the current page, up from your starting point.

You can click a breadcrumb to jump directly to the corresponding previous step. For consecutive navigation, use the Back and Forward buttons of the browser.

If you create a cycle by clicking an item already seen and listed in breadcrumbs, the breadcrumbs automatically slice up to the current location, preventing an unnecessary build-up of items. If you drill down to an item and then refresh the page, the item becomes the only one in the breadcrumb list. Breadcrumb navigation is also reset if you click the Dashboard link at the top of the page.

[Top of page](#Graphical-User-Interface)

## <a id="10.2"></a>Servers

To see filesystem servers, log in to the GUI, and then on the left click **Servers** or click **Management > Servers** on the top.

<a id="f11.2"></a>
![md_Graphics/servers.png][f11.2]

You can identify the listed filesystem servers by:

- **Host**: Server's clickable host name. Click it to jump to a detailed server view.
- **Boot time**: Last time the server was started.
- **Profile**: Currently either EXAScaler managed or monitored storage server. You define the profile when you add a server to the filesystem.
- **LNet**: Current Lustre networking service status, either Up, Down, or Unloaded.

[Top of page](#Graphical-User-Interface)

### <a id="10.2.1"></a>Server actions

There are several actions that you can perform on servers and related LNet in Servers view.

For any listed server, you can do:

- **Reboot**: Initiate a server reboot.
- **Shutdown**: Initiate an orderly server shutdown.
  - Note that with both reboot or shutdown, until the server is back online, HA capable filesystem targets fail over to a peer server or, if they are non HA capable, become unavailable.
- **Remove**: Remove the server, including dependent filesystem targets.
- **Force Remove**: (only if the remove command was unsuccessful) Remove the server record from the configuration database without contacting the server. This also removes all dependent filesystem targets without any attempt to unconfigure them.
  - Note that after a forced removal, you cannot add the server to another filesystem until removing the management software from the server. To do this, contact technical support.

You can additionally control the Lustre networking service:

- **Stop LNet**: Shut down the service and stop any targets running on the server.
- **Unload LNet**: If the service is up, stop it and unload its kernel module to ensure that it is reloaded before any targets are started again.
- **Load LNet**: Load the service's kernel module on the server.
- **Start LNet**: Start the service on the server.

There is also a linked host name for each server. Click it, and you will jump to a server-specific view with the same server and LNet actions. Alternatively, expand the list of servers on the left and click a server. Remember that you must be logged in to do this.

<a id="f11.2.1"></a>
![md_Graphics/server-details.png][f11.2.1]

[Top of page](#Graphical-User-Interface)

### <a id="10.2.2"></a>Server volumes

To see all volumes, for all servers, log in to the management interface, and then click **Management > Servers** on the top:

<a id="f11.2.2"></a>
![md_Graphics/server-volumes.png][f11.2.2]

Alternatively, expand the list of volumes for a server on the left:

<a id="f11.2.3"></a>
![md_Graphics/server-volumes-alt.png][f11.2.3]

If there are a lot of volumes, the list is paginated.

Volumes, also called LUNs or block devices, are the underlying units of storage used to create filesystems. Each filesystem target corresponds to a single volume.

Currently, you can only see the volumes that are in use as filesystem targets. If a volume's server, also called host, is configured for HA, you can also see the volume's peer servers. You can see that a volume may be accessible on one or more servers via different device paths, such as _/dev/disk/by-id/scsi-360001ff0e06680000000002a880d000b_, and that a volume may also be accessible via multiple device paths on the same server. In a future version of the management interface, you will be able to set or change the volume's primary and peer servers.

[Top of page](#Graphical-User-Interface)

### <a id="10.2.3"></a>Server dashboard

Each server has a dashboard with four charts, which you can see if you log in to the management interface, expand the list of servers on the left, and click a chart icon next to a server's name.

<a id="f11.2.4"></a>
![md_Graphics/server-dashboard.png][f11.2.4]

The server dashboard displays the following charts:

- [**Read/Write Bandwidth**](#10.2.3.1)
- [**CPU Usage**](#10.2.3.2)
- [**Memory Usage**](#10.2.3.3)
- [**LNet Usage**](#10.2.3.4)

#### <a id="10.2.3.1"></a>Server's read/write bandwidth

The Read/Write Bandwidth chart on the server's dashboard shows the read and write activity over time for the filesystem(s) that the server hosts.

- Read operations appear above the center line. Write operations appear below the center line. Zero read or write operations are across the center line.
- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.5"></a>
![md_Graphics/server-bandwidth-chart.png][f11.2.5]

#### <a id="10.2.3.2"></a>Server's CPU usage

The CPU Usage chart on the server's dashboard shows the percentage of CPU activity over time, measured individually for user processes, system processes, and processes in an IO Wait state.

- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.6"></a>
![md_Graphics/server-cpu-chart.png][f11.2.6]

#### <a id="10.2.3.3"></a>Server's memory usage

The Memory Usage chart on the server's dashboard shows total vs used RAM and total vs used swap space.

- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.7"></a>
![md_Graphics/server-memory-chart.png][f11.2.7]

#### <a id="10.2.3.4"></a>Server's LNet usage

The LNet Usage chart on the server's dashboard shows packets received vs sent over each Lustre Network Identifier on the server, such as _172.18.0.1@o2ib_.

- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.8"></a>
![md_Graphics/server-lnet-chart.png][f11.2.8]

[Top of page](#Graphical-User-Interface)

## <a id="10.3"></a>Filesystems

You can list filesystems in the cluster if you log in to the management interface, and then click **Filesystems** on the left or instead click **Management > Filesystems** on the top.

<a id="f11.3"></a>
![md_Graphics/filesystems.png][f11.3]

Each filesystem listed in Filesystems view is identified by:

- **Filesystem**: Filesystem's name. Click it to jump to a detailed filesystem view.
- **Primary MGS**: Filesystem's primary management server name. Click it to jump to a detailed server view.
- **MDT Count**: Total of metadata targets available to the filesystem.
- **Connected Clients**: Total of clients currently using the filesystem.
- **Space Used / Total**: Used vs total filesystem capacity.

[Top of page](#Graphical-User-Interface)

### <a id="10.3.1"></a>Filesystem actions

There are several actions that you can perform on filesystems in Filesystems view:

- **Stop**: Stop the filesystem's metadata and storage targets (MDTs and OSTs), which makes the filesystem unavailable to clients.
- **Forget**: Remove the filesystem. The filesystem becomes unavailable to clients but you can reuse the volumes, and the contents, in another filesystem.

[Top of page](#Graphical-User-Interface)

### <a id="10.3.2"></a>Filesystem details

To see filesystem details, click the name of a filesystem in Filesystems view or, alternatively, expand the list of filesystems on the left and click the name of a filesystem. Remember that you must be logged in to do this.

<a id="f11.3.1"></a>
![md_Graphics/filesystem-details.png][f11.3.1]

You can scroll up and down the details, and additionally expand the list of filesystem resources on the left to use it for navigation.

<a id="f11.3.2"></a>
![md_Graphics/filesystem-details-nav.png][f11.3.2]

On the details view, you see filesystem details as well as details for filesystem resources, such as MGS, MDTs, OSTs, and OST pools.

The following details identify the filesystem in addition to the name:

- **Space Used / Total**: Used vs total filesystem capacity.
- **Files Created / Maximum**: Used vs total inodes.
- **State**: Filesystem state, either available (started) or unavailable (stopped) to clients.
- **MGS**: Filesystem's primary management server name. Click it to jump to a detailed server view.
- **Number of MDTs**: Total of metadata targets available to the filesystem.
- **Number of OSTs**: Total of object storage targets available to the filesystem.
- **Number of Connected Clients**: Total of clients currently using the filesystem.
- **Status**: Alerts for the filesystem.
- **Client Mount Command**: Command to mount the filesystem for clients.

The following details identify MGTs, MDTs, and OSTs in addition to the name:

- **Started On**: The server on which the target is currently running.
- **Primary Server**: The primary server for the target to run on.
- **Failover Server**: The peer server for the target to run on if the target is HA configured and the primary server becomes unavailable.
- **Volume**: The [volume](#10.2.2) for the target.

Here is how the details may look like for a metadata target:

<a id="f11.3.3"></a>
![md_Graphics/target-details.png][f11.3.3]

If you drill down the list of filesystem resources to OST pools, you will see the OSTs of a pool, and can click any target to display the details as above.

<a id="f11.3.4"></a>
![md_Graphics/pool-details.png][f11.3.4]

You can perform actions on each target (MGT, MDT, or OST) that you view:

- **Stop**: Stop the target. When an MGT is stopped, clients are unable to make new connections to the filesystems using this MGT. However, the MDT and OST(s) stay up if they were started before this MGT was stopped, and can be stopped and restarted while this MGT is stopped.
- **Failover**: Forcibly migrate the target to its failover server. Clients attempting to access data on the target while the migration is in process may experience delays until the migration completes. If this action is not displayed, then it is either the MGT has already failed over, and you will see the Failback action instead, or a failover, secondary server has not been configured.
- **Failback**: Migrate the target back to its primary server. Clients attempting to access data on the target while the migration is in process may experience delays until the migration completes. This action is displayed only after a target has failed over.
- **Remove**: (for OSTs only) Remove the target, for example, if you need to replace it.

[Top of page](#Graphical-User-Interface)

### <a id="10.3.3"></a>Filesystem dashboard

Each filesystem has a dashboard with the charts:

- **Filesystem Space Usage**: Used vs available space on the filesystem.
- **Filesystem Usage**: Percentage of used space, OST inodes, and MDT inodes over time, with day, 2 days, and week scaling.
- **OST Balance**: Percentage points interpreting space usage on each OST.
- **MDT Usage**: getattr and statfs operations over time, with day, 2 days, and week scaling.

To see the dashboard, log in to the GUI, expand the list of filesystems on the left, and then click the chart icon for a filesystem:

<a id="f11.3.5"></a>
![md_Graphics/filesystem-dashboard.png][f11.3.5]

[Top of page](#Graphical-User-Interface)

### <a id="10.3.4"></a>MGT dashboard

Each filesystem's management target has a dashboard with the charts:

- **Metadata Operations**: Number of metadata operations through this target over time.
- **Space Usage**: Percentage of space used in operations through this target over time.
- **File Usage**: Percentage of file used in operations through this target over time.

To see the dashboard, log in to the GUI, navigate to a filesystem listed on the left, expand the list of MGTs, and click the chart icon for a target:

<a id="f11.3.6"></a>
![md_Graphics/mgt-dashboard.png][f11.3.6]

[Top of page](#Graphical-User-Interface)

### <a id="10.3.5"></a>MDT dashboard

Each filesystem's metadata target has a dashboard with the charts:

- **Metadata Operations**: Number of metadata operations through this target over time.
- **Space Usage**: Percentage of space used in operations through this target over time.
- **File Usage**: Percentage of file used in operations through this target over time.

To see the dashboard, log in to the GUI, navigate to a filesystem listed on the left, expand the list of MDTs, and click the chart icon for a target:

<a id="f11.3.7"></a>
![md_Graphics/mdt-dashboard.png][f11.3.7]

[Top of page](#Graphical-User-Interface)

### <a id="10.3.6"></a>OST dashboard

Each filesystem's object storage target has a dashboard with the charts:

- **I/O Performance**: Number of metadata operations through this target over time.
- **Space Usage**: Percentage of space used in operations through this target over time.
- **File Usage**: Percentage of file used in operations through this target over time.

To see the dashboard, log in to the GUI, navigate to a filesystem listed on the left, expand the list of OSTs, and click the chart icon for a target:

<a id="f11.3.8"></a>
![md_Graphics/ost-dashboard.png][f11.3.8]

[Top of page](#Graphical-User-Interface)

## <a id="9.3.6"></a>Users

If you are a superuser, you can view, create, and manage users by clicking **Management > Users** at the top of the page.

![md_Graphics/config_users.png][f9.20]

The following types of users exist:

- **Filesystem user** - Filesystem users have full GUI access except for the Management menu, which is hidden from view. The logged-in users cannot create or manage a filesystem, but can use Dashboard and Activity views to monitor filesystems.
- **Superuser** - Superusers, such as filesystem administrators, have full access to the application, including the Management menu. The logged-in users can create, monitor, manage, and remove filesystems and their components. <!-- The users can also create, modify (change passwords), and delete other users, including superusers, but cannot delete its own account. For more information, see [Creating User Accounts](Getting_started_2_0.md/#2.1). -->

Superusers also have these options by clicking a user's account:

- **Details** - View and change the username, email, first and last names.
- **Password** - (Coming soon) Change the password.
- **Email Notifications** - (Coming soon) Select events for email notifications. <!-- If nothing is selected, all events except for "Host contact alerts" are included. For more information, see [Setting up Email Notifications](Getting_started_2_0.md/#2.2). -->

[Top of page](#Graphical-User-Interface)

## <a id="9.5"></a>Logs

To view logs, log in to the management interface, and then click **Logs** on the right. The view will expand and display a paginated list of logged events.

![md_Graphics/logs.png][f9.23]

<!-- You can filter logs by date range, host, service, and messages from Lustre or all sources. You can also use auto-completion for search and host name links to jump to host information. -->

You can identify each logged event by time, service, message, and host.

As an example of logged events, consider what happens if a failover takes place:

- A browser-level notification appears briefly to notify you of related unresolved warnings.
- In the Activity view, another alert appears saying that the server has failed over. Other related alerts are also displayed.
- In filesystem details, an alert is displayed and the server, on which the target is now running, is shown in the Started On column for that target.
- The superuser receives a configured email alert.

An event is logged for each case above, and you can see it displayed in **Logs**.

[Top of page](#Graphical-User-Interface)

## <a id="9.6"></a>Activities

Activity messages provide information about the functioning and health of a managed filesystem. You do not need to be logged in to view activity messages.

To view activity messages, click **Activity** on the right of the page. The view will expand and display a paginated list of all filesystem activities, listing most recent messages first.

![md_Graphics/activities.png][f9.24]

The counter next to the activity icon reflects the number of active issues with the cluster. The color of the icon will change between green, yellow, and red according to the severity of the highest active issue.

There are five types of activity messages:

- **Command running**: Marked with gray color, these messages inform you of commands currently in progress.<!-- These are the commands that you have entered into the manager GUI.-->
- **Command successful**: Marked with green color, these messages identify successfully completed commands. To learn about the underlying commands and their syntax, click **Details**, and then click a command link.
- **Info messages**: Marked with blue color, these messages inform you of normal transitions that occur at a single point in time during the creation or management of the filesystem, often in response to a command entered into the GUI. A single command may cause several such events to occur.
- **Warning alerts**: Marked with yellow color, these messages usually indicate that the filesystem is operating in degraded mode; for example, when a target fails over, high availability is no longer true for that target. A warning message marks a status change that has a specific **Begin** and **End** time. A warning is active at the beginning of the status change and inactive at the end of the status change; for example, a warning message may inform you that an OST has gone offline, and that message is active until the OST becomes operational again. Not all warnings necessarily signify a degraded state; for example, a target recovery to a failover server signifies that the failover occurred successfully.
- **Error alerts**: Marked with red color, these messages indicate that the filesystem is down or severely degraded, that one or more filesystem components are currently unavailable. For example, both primary and secondary servers for a target are not running. An error often has a remedial action you can take by clicking the button.

Before you see an unresolved filesystem error or warning in the Activity view, this error or warning pops up as a browser-level notification.

[Top of page](#Graphical-User-Interface)

<!--
**Running common searches**

At the Status window, under the **Common Searches** drop-down, select a search to run.

You can modify any of the listed searches. To do this, select a search type, edit the string displayed in the Search bar, and click **Search** or press **Enter**.

- **Search active alerts**: Display active alerts (warnings and errors) that reflect the current state of the filesystem. This search lists only warnings and errors that have not been resolved.
- **Search alerts**: Display all alerts (warnings and errors) generated since the creation of the filesystem. This includes active (unresolved) and inactive (resolved) alerts.
- **Search commands**: Display all commands, those successfully executed and those that are currently in process.
- **Search events**: Display all information messages occurred since the creation of the filesystem.
-->

<!--
**Composing search queries**

At the top of the Status window, start typing in the search bar and use auto-completion to finish your query.

You can run searches as follows:

1. Filter your search by keywords using the equals sign (=) or "in" keywords. Examples:
    - `severity = ERROR`
    - `severity in [WARNING, ERROR]`
1. Join keyword filters using the "and" keyword. Example:
    - `severity = ERROR and active = true`

Below is a description of available keywords:

|Keyword|Type|Description|
|---|---|---|
|active|boolean|Either 'true' for resolved record or 'false' unresolved record|
|record_type|string|Record type, such as info messages, warning alerts, and so on|
|severity|string|Either 'INFO', 'DEBUG', 'CRITICAL', 'WARNING', or 'ERROR'|

Below is a query example:
```
active = true
record_type = CorosyncNoPeersAlert
severity in [ERROR, WARNING]
```
[Top of page](#Graphical-User-Interface)
-->

[f11.1]: md_Graphics/dashboard.png
[f11.1.1]: md_Graphics/dashboard-sandwich.png
[f11.1.2]: md_Graphics/dashboard-login.png
[f11.1.3]: md_Graphics/mgmt-menu.png
[f11.2]: md_Graphics/servers.png
[f11.2.1]: md_Graphics/server-details.png
[f11.2.2]: md_Graphics/server-volumes.png
[f11.2.3]: md_Graphics/server-volumes-alt.png
[f11.2.4]: md_Graphics/server-dashboard.png
[f11.2.5]: md_Graphics/server-bandwidth-chart.png
[f11.2.6]: md_Graphics/server-cpu-chart.png
[f11.2.7]: md_Graphics/server-memory-chart.png
[f11.2.8]: md_Graphics/server-lnet-chart.png
[f11.3]: md_Graphics/filesystems.png
[f11.3.1]: md_Graphics/filesystem-details.png
[f11.3.2]: md_Graphics/filesystem-details-nav.png
[f11.3.3]: md_Graphics/target-details.png
[f11.3.4]: md_Graphics/pool-details.png
[f11.3.5]: md_Graphics/filesystem-dashboard.png
[f11.3.6]: md_Graphics/mgt-dashboard.png
[f11.3.7]: md_Graphics/mdt-dashboard.png
[f11.3.8]: md_Graphics/ost-dashboard.png

<!-- [f9.2]: md_Graphics/file_system_params.png
[f9.3]: md_Graphics/read-write-heat-map-chart.png
[f9.4]: md_Graphics/job_stats.png
[f9.5]: md_Graphics/OST_Balance_Chart.png
[f9.6]: md_Graphics/Metadata_Operations_chart.png
[f9.7]: md_Graphics/read-write-bandwidth-hover.png
[f9.8]: md_Graphics/Metadata_Servers_Chart.png
[f9.9]: md_Graphics/Object_Storage_Servers_Chart.png
[f9.10]: md_Graphics/CPU_Usage_Chart.png
[f9.11]: md_Graphics/Memory_Usage_Chart.png
[f9.12]: md_Graphics/Space_Usage_Chart.png
[f9.13]: md_Graphics/File_Usage_Chart.png
[f9.14]: md_Graphics/Object_Usage_Chart.png
[f9.15]: md_Graphics/config_servers.png
[f9.16]: md_Graphics/Power_Control_Tab.png
[f9.17]: md_Graphics/config_file_systems.png
[f9.18]: md_Graphics/check_mark.png
[f9.19]: md_Graphics/HSM_Operations.png -->

[f9.20]: md_Graphics/config_users.png

<!-- [f9.21]: md_Graphics/config_volumes.png
[f9.22]: md_Graphics/config_mgts.png -->

[f9.23]: md_Graphics/logs.png
[f9.24]: md_Graphics/activities.png

<!-- [f9.25]: md_Graphics/red_status_bar.png -->

<!-- [f9.26]: md_Graphics/treeview.png -->

[f9.27]: md_Graphics/breadcrumbs.png
