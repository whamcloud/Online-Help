<a id="9.0"></a>

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
    <!-- - [Dashboard charts](#9.2) -->
    <!-- - [Management menu](#9.3) -->
    <!-- - [Job stats](#9.4) -->
- [Users](#9.3.6)
- [Logs](#9.5)
- [Activities](#9.6)
  <!-- - [Resources](#9.7) -->
  <!-- - [Breadcrumb navigation](#9.8) -->
  <!-- - [Alert bar](#9.9) -->

## <a id="9.1"></a>Dashboard

Dashboard is the first view that you see on starting a new session in the GUI. You can also navigate to this view from any other view by clicking Dashboard at the top or on the breadcrumbs trail.

<a id="f11.1"></a>
![md_Graphics/dashboard.png][f11.1]

You will see a portable, "sandwich" view for all browser windows less than 1024 pixels in width.

<a id="f11.1.1"></a>
![md_Graphics/dashboard-sandwich.png][f11.1.1]

The Dashboard view displays four charts with usage and performance data aggregated at several levels for monitored or managed file systems:

- **Filesystem Space Usage**: Used vs available space across all file systems.
- **I/O Performance**: Throughput and IOPS with day, 2 days, and week scaling.
- **OST Balance**: Percentage points interpreting space usage on each OST in the cluster.
- **LNet Performance**: Filesystem network speed with day, 2 days, and week scaling.

Note that monitored filesystems do not support failover of their targets through the GUI.

[Top of page](#9.0)

## <a id="10.1.1"></a>Login

If you are a filesystem administrator, log in to see a list of resources and the Management menu, as well as logs for the filesystem cluster. When you log in, besides seeing the default Dashboard view, you can select to monitor and manage individual file systems and servers.

<a id="f11.1.2"></a>
![md_Graphics/dashboard-login.png][f11.1.2]

[Top of page](#9.0)

## <a id="10.1.2"></a>Management menu

The Management menu appears at the top of the GUI page after [login](#10.1.1). From there, you can click a resource to jump to its details and do the various management actions on the resource. The list of resources on the left, which also appears after login, mirrors most of the Management menu and makes it easy to drill to a particular resource.

<a id="f11.1.3"></a>
![md_Graphics/mgmt-menu.png][f11.1.3]

[Top of page](#9.0)

## <a id="9.8"></a>Breadcrumb navigation

Breadcrumb navigation lets you see where in the hierarchy of the GUI you currently are.

![md_Graphics/breadcrumbs.png][f9.27]

Breadcrumbs display a path outlining the steps taken to arrive at the current page, up from your starting point.

You can click a breadcrumb to jump directly to the corresponding previous step. For consecutive navigation, use the Back and Forward buttons of the browser.

If you create a cycle by clicking an item already seen and listed in breadcrumbs, the breadcrumbs automatically slice up to the current location, preventing an unnecessary build-up of items. If you drill down to an item and then refresh the page, the item becomes the only one in the breadcrumb list. Breadcrumb navigation is also reset if you click the Dashboard link at the top of the page.

[Top of page](#9.0)

<!--
### <a id="9.1.1"></a>File System Details window
After you have created a file system, you can view its configuration and manage the file system at the *File System Details* window.

To access the File System Details window, at the Dashboard, click the name of the file system of interest.
![md_Graphics/file_system_params.png][f9.2]


This window identifies the:

- *Management Target* (MGT)
- *Metadata Target* (MDT). There may be more than one MDT.
- *Object Storage Targets*
- *Alert status*
- Overall file system capacity and free space


This window also identifies the volume(s), primary server(s), and failover server(s) for the MGS, MDT(s) and all OST(s). From this window you can [Update Advanced Settings](Advanced_Topics_11_0.md/#10.1) and
 [View Client Mount Information](Creating_new_lustre_fs_3_0.md/#3.11).


### <a id="9.1.2"></a>Configuring the Dashboard
By default, the Dashboard displays information and charts for all file systems. Click **Configure Dashboard** to open a window to let you do the following:

- To view a file system's charts: Click **File System** (default). You can view information and charts for all file systems, or select a specific file system from the drop-down menu.
- To view a server's charts: Click **Select Server**. You can view information and charts for all servers (on all file systems), or select a specific server from the drop-down menu.
- To view charts for one or all targets: Click **File System**. Select the desired file system and then select **All Targets** or an individual target.

Click **Update** to apply your choices and **Cancel** to close.

[Top of page](#9.0)
-->

## <a id="10.2"></a>Servers

To see filesystem servers, log in to the management interface, and then on the left menu click **Servers** or click **Management > Servers** on the top menu.

<a id="f11.2"></a>
![md_Graphics/servers.png][f11.2]

The listed filesystem servers are identified by:

- **Host**: Server's clickable host name. Click it to jump to a detailed server view.
- **Boot time**: Last time the server was started.
- **Profile**: Currently either EXAScaler managed or monitored storage server. You define the profile when you add a server to the file system.
- **LNet**: Current Lustre networking service status, either Up, Down, or Unloaded.

[Top of page](#9.0)

### <a id="10.2.1"></a>Server actions

There are several actions that you can perform on servers and related LNet in Servers view.

For any listed server, you can do:

- **Reboot**: Initiate a server reboot.
- **Shutdown**: Initiate an orderly server shutdown.
  - Note that with both reboot or shutdown, until the server is back online, HA capable file system targets fail over to a peer server or, if they are non HA capable, become unavailable.
  - **Remove**: Remove the server, including dependent file system targets.
  - **Force Remove**: (only if the remove command was unsuccessful) Remove the server record from the configuration database without contacting the server. This also removes all dependent file system targets without any attempt to unconfigure them.
  - Note that after a forced removal, you cannot add the server to another file system until removing the management software from the server. To do this, contact technical support.

You can additionally control the Lustre networking service:

- **Stop LNet**: Shut down the service and stop any targets running on the server.
- **Unload LNet**: If the service is up, stop it and unload its kernel module to ensure that it is reloaded before any targets are started again.
- **Load LNet**: Load the service's kernel module on the server.
- **Start LNet**: Start the service on the server.

There is also a linked host name for each server. Click it, and you will jump to a server-specific view with the same server and LNet actions. Alternatively, expand the list of servers on the left and click a server. Remember that you must be logged in to do this.

<a id="f11.2.1"></a>
![md_Graphics/server-details.png][f11.2.1]

[Top of page](#9.0)

### <a id="10.2.2"></a>Server volumes

To see all volumes, for all servers, log in to the management interface, and then click **Management > Servers** on the top:

<a id="f11.2.2"></a>
![md_Graphics/server-volumes.png][f11.2.2]

Alternatively, expand the list of volumes for a server on the left:

<a id="f11.2.3"></a>
![md_Graphics/server-volumes-alt.png][f11.2.3]

If there are a lot of volumes, the list is paginated.

Volumes, also called LUNs or block devices, are the underlying units of storage used to create file systems. Each file system target corresponds to a single volume.

Currently, you can only see the volumes that are in use as file system targets. If a volume's server, also called host, is configured for HA, you can also see the volume's peer servers. You can see that a volume may be accessible on one or more servers via different device paths, such as _/dev/disk/by-id/scsi-360001ff0e06680000000002a880d000b_, and that a volume may also be accessible via multiple device paths on the same server. In a future version of the management interface, you will be able to set or change the volume's primary and peer servers.

[Top of page](#9.0)

### <a id="10.2.3"></a>Server dashboard

Each server has a dashboard with four charts, which you can see if you log in to the management interface, expand the list of servers on the left, and click a chart icon next to a server's name.

<a id="f11.2.4"></a>
![md_Graphics/server-dashboard.png][f11.2.4]

The server dashboard displays the following charts:

- **Read/Write Bandwidth**
- **CPU Usage**
- **Memory Usage**
- **LNet Usage**

#### Server's read/write bandwidth

The Read/Write Bandwidth chart on the server's dashboard shows the read and write activity over time for the file system(s) that the server hosts.

- Read operations appear above the center line. Write operations appear below the center line. Zero read or write operations are across the center line.
- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.5"></a>
![md_Graphics/server-bandwidth-chart.png][f11.2.5]

#### Server's CPU usage

The CPU Usage chart on the server's dashboard shows the percentage of CPU activity over time, measured individually for user processes, system processes, and processes in an IO Wait state.

- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.6"></a>
![md_Graphics/server-cpu-chart.png][f11.2.6]

#### Server's memory usage

The Memory Usage chart on the server's dashboard shows total vs used RAM and total vs used swap space.

- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.7"></a>
![md_Graphics/server-memory-chart.png][f11.2.7]

#### Server's LNet usage

The LNet Usage chart on the server's dashboard shows packets received vs sent over each Lustre Network Identifier on the server, such as _172.18.0.1@o2ib_.

- Mouse over any point on the chart to see the exact time and measurement.
- Click at any point on the chart to add annotation.

<a id="f11.2.8"></a>
![md_Graphics/server-lnet-chart.png][f11.2.8]

[Top of page](#9.0)

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

[Top of page](#9.0)

### <a id="10.3.1"></a>Filesystem actions

There are several actions that you can perform on filesystems in Filesystems view:

- **Stop**: Stop the filesystem's metadata and storage targets (MDTs and OSTs), which makes the filesystem unavailable to clients.
- **Forget**: Remove the filesystem. The filesystem becomes unavailable to clients but you can reuse the volumes, and the contents, in another filesystem.

[Top of page](#9.0)

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
- **Volume**: The [volume](id="10.2.2") for the target.

Here is how the details may look like for a metadata target:

<a id="f11.3.3"></a>
![md_Graphics/target-details.png][f11.3.3]

If you drill down the list of filesystem resources to OST pools, you will see the OSTs of a pool, and can click any target to display the details as above.

<a id="f11.3.4"></a>
![md_Graphics/pool-details.png][f11.3.4]

You can perform actions on each target (MGT, MDT, or OST) that you view:

- **Stop**: Stop the target. When an MGT is stopped, clients are unable to make new connections to the file systems using this MGT. However, the MDT and OST(s) stay up if they were started before this MGT was stopped, and can be stopped and restarted while this MGT is stopped.
- **Failover**: Forcibly migrate the target to its failover server. Clients attempting to access data on the target while the migration is in process may experience delays until the migration completes. If this action is not displayed, then it is either the MGT has already failed over, and you will see the Failback action instead, or a failover, secondary server has not been configured.
- **Failback**: Migrate the target back to its primary server. Clients attempting to access data on the target while the migration is in process may experience delays until the migration completes. This action is displayed only after a target has failed over.
- **Remove**: (for OSTs only) Remove the target, for example, if you need to replace it.

[Top of page](#9.0)

### <a id="10.3.3"></a>Filesystem dashboard

Each filesystem has a dashboard with the charts:

- **Filesystem Space Usage**: Used vs available space on the file system.
- **Filesystem Usage**: Percentage of used space, OST inodes, and MDT inodes over time, with day, 2 days, and week scaling.
- **OST Balance**: Percentage points interpreting space usage on each OST.
- **MDT Usage**: getattr and statfs operations over time, with day, 2 days, and week scaling.

To see the dashboard, log in to the GUI, expand the list of filesystems on the left, and then click the chart icon for a filesystem:

<a id="f11.3.5"></a>
![md_Graphics/filesystem-dashboard.png][f11.3.5]

[Top of page](#9.0)

### <a id="10.3.4"></a>MGT dashboard

Each filesystem's management target has a dashboard with the charts:

- **Metadata Operations**: Number of metadata operations through this target over time.
- **Space Usage**: Percentage of space used in operations through this target over time.
- **File Usage**: Percentage of file used in operations through this target over time.

To see the dashboard, log in to the GUI, navigate to a file system listed on the left, expand the list of MGTs, and click the chart icon for a target:

<a id="f11.3.6"></a>
![md_Graphics/mgt-dashboard.png][f11.3.6]

[Top of page](#9.0)

### <a id="10.3.5"></a>MDT dashboard

Each filesystem's metadata target has a dashboard with the charts:

- **Metadata Operations**: Number of metadata operations through this target over time.
- **Space Usage**: Percentage of space used in operations through this target over time.
- **File Usage**: Percentage of file used in operations through this target over time.

To see the dashboard, log in to the GUI, navigate to a file system listed on the left, expand the list of MDTs, and click the chart icon for a target:

<a id="f11.3.7"></a>
![md_Graphics/mdt-dashboard.png][f11.3.7]

[Top of page](#9.0)

### <a id="10.3.6"></a>OST dashboard

Each filesystem's object storage target has a dashboard with the charts:

- **I/O Performance**: Number of metadata operations through this target over time.
- **Space Usage**: Percentage of space used in operations through this target over time.
- **File Usage**: Percentage of file used in operations through this target over time.

To see the dashboard, log in to the GUI, navigate to a file system listed on the left, expand the list of OSTs, and click the chart icon for a target:

<a id="f11.3.8"></a>
![md_Graphics/ost-dashboard.png][f11.3.8]

[Top of page](#9.0)

<!--
## <a id="9.2"></a>Dashboard charts

Several Dashboard charts provide quick, detailed, visual representation of the performance of your Lustre file system(s).  You can configure certain data display parameters for each chart, and your chart configuration will persist until you reload/refresh the Dashboard page, using the browser.

Charts are presented as:

- [File system charts](#9.2a)
- [Server charts](#9.2b)
- [MDT charts](#9.2c)
- [OST charts](#9.2d)

[Top of page](#9.0)

**<a id="9.2a"></a>File system charts**

The Dashboard window displays the following six charts for one or more file systems:

- [Read/Write Heat Map](#9.2.1)
- [OST Balance](#9.2.2)
- [Metadata Operations](#9.2.3)
- [Read/Write Bandwidth](#9.2.4)
- [Object Storage Servers](#9.2.6)



**<a id="9.2b"></a>Server charts**

The Dashboard displays the following three charts for an individual server (MDS or OSS). To access, click **Configure Dashboard**. Then select **Servers** and select the desired server.

- [Read/Write Bandwidth](#9.2.4)
- [CPU Usage](#9.2.7)
- [Memory Usage](#9.2.8)



**<a id="9.2c"></a>MDT charts**

The Dashboard window displays the following three charts for the selected MDT. To access, click **Configure Dashboard**. Then select the specific file system. Lastly, select the desired MDT.

- [Metadata Operations](#9.2.3)
- [Space Usage](#9.2.9)
- [File Usage](#9.2.10)



**<a id="9.2d"></a>OST charts**

The OST Dashboard window displays the following three charts for the selected OST. To access, click Configure Dashboard. Then select the specific file system. Lastly, select the desired OST.

- [Read/Write Bandwidth](#9.2.4)
- [Space Usage](#9.2.9)
- [Object Usage](#9.2.11)


### <a id="9.2.1"></a>Read/Write Heat Map chart

The Read/Write Heat Map chart shows the level of read or write activity for each OST in all file systems. Each row is a single OST, and each column is a consecutive time sample. The chart updates from right to left, so the most recent sample for any OST is in the right-most column. This chart is displayed when all File Systems are selected on the Dashboard window (default). You can also view this chart for a single file system.

You can the monitor the level of read or write activity for a given OST over time by looking across the chart. Activity is displayed in shades, from light-blue to red. Displayed data transfer rates are not fixed: Light-blue represents the lowest percent of maximum for the preceding twenty samples, while darkest-red represents the highest percent of maximum and the most read or write activity.

**Note:**
Because of the way that activity information is averaged, the heat map may show slightly different information following a refresh of the display. This is normal.
![md_Graphics/read-write-heat-map-chart.png][f9.3]


**Features**

- Mouse over any cell on the heat map to learn which OST this is, its file system, its read or write activity, and the actual starting date and time of that measurement period.
- Click on a specific heat map cell to open the Job Stats window (job statistics) for that OST and read/write measurement. See [View job statistics](Monitoring_lustre_fs_4_0_0.md/#4.3).
- To better view larger numbers of OSTs, for example, more than forty OSTs, click Full Screen to expand the map.

**View this chart for a specific file system**

This chart is displayed by default for all file systems. To view this chart for a single file system:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **File System** (default).
1. At the File System drop-down menu, select the file system. Then click **Update**.

**Configure the Heat Map chart**

1. Click **Configure** to open the configuration window.
1. Click **Set Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4) for the entire map. This is a sliding duration. Based on your selection, the heat map is divided into columns of equal duration. Note that for long durations, the map will be divided over several days, with measurements taken at different times of the day. The value given in each cell is the average for that measurement period. After clicking **Update** to apply changes, the duration of measurements begins immediately.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of a heat map is a static snapshot, starting and ending as configured.
1. Click **Select data** to view to select **read bytes**, **write bytes**, **read IOPS**, or **write IOPS**.
1. Click **Update** to close this window and apply changes. Click **Cancel** to close.


#### <a id="9.2.1.1"></a>Job Stats

Job statistics information is accessible from the Read/Write Heat Map chart. Simply click on an OST cell on the chart, and for that OST and time interval, a window opens that shows metrics for the top ten jobs for that OST. Current metrics include average, min, and max for read and write bandwidth and read and write IOPS per the time interval. Because this information is specific to a time period, it is static.

![md_Graphics/job_stats.png][f9.4]

The Jobs Stats window is available for any dashboard window that has a heat map: These are the File Systems dashboard windows and the Servers dashboard window. This feature also supports the creation of plug-ins to display user account, command line, job size, and job start/finish times.

For statistics regarding the top ten jobs for all active file systems, click **Job Stats** at the top menu bar. This view updates in real time, showing a top-like interface of current jobs. Durations and sort-order are customizable.


### <a id="9.2.2"></a>OST Balance chart

This chart shows the percentage of storage capacity currently consumed for each OST. This chart is displayed when File Systems are selected on the Dashboard window (default). You can also view this chart for a single file system.

![md_Graphics/OST_Balance_Chart.png][f9.5]

**Features**

- Click **Full Screen** to fill the browser window with this chart. Click Exit Full Screen to return to the normal view.
- Click **Stacked** to arrange the display so that the used and unused capacities are stacked for each OST.
- Click **Grouped** to arrange the display so that the used and unused capacities are shown separately for each OST.

**View this chart for a specific file system**

This chart is displayed by default for all file systems. To view this chart for a single file system:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **File System** (default).
1. At the File System drop-down menu, select the file system. Then click **Update**.

**Configure the OST Balance chart**

1. Click **Configure**:
1. This control lets you filter and display only those OSTs for which their usage (consumed capacity) is equal to or greater than the threshold you set. The default usage is set to zero percent, so that all OSTs are displayed. Set the desired threshold.
1. Click **Update**.



### <a id="9.2.3"></a>Metadata Operations chart

This chart is shown for file systems and for specific MDTs. The chart shows the number of metadata I/O operations over time, based on command type. These are system calls or commands performed on all file systems. You can also view this chart for a single file system or MDT.
![md_Graphics/Metadata_Operations_chart.png][f9.6]

**Features**

- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.
- Mouse over any point on the chart to learn the values for each system call or command type executing at that time. Values shown vary, based on the chart type: For Stacked and Stream display, values are absolute. For Expanded display, values are relative percentages.
- Click on any area in the chart to display only information for that specific system call or command type. The vertical scale will adjust to better display that information.
- Click the command icons (e.g. **close**, **getattr**, etc.) to display or not display those command types on the chart.
- Click **Stacked** to show all displayed command types stacked, with the command types stacked alphabetically.
- Click **Stream** to display a "stream-graph" of the relative volume of each type of metadata operation. The display of each command-type (or layer) out from the horizontal center-line is ordered, from the least-varying volume to most-varying volume, per command type, over time.
- Click **Expanded** to show the percentage of each command type versus 100%.

**View this chart for a specific file system**

This chart is displayed by default for all file systems. To view this chart for a single file system:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **File System** (default).
1. At the File System drop-down menu, select the file system. Then click **Update**.

**View this chart for a specific MDT**

To view this chart for a single MDT:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **Server**.
1. At the **Server** drop-down menu, select the server hosting the desired target.
1. At the **Target** drop-down menu, select the desired MDT. Then click **Update**.

**Configure the Metadata Operations chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the chart will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.


### <a id="9.2.4"></a>Read/Write Bandwidth chart

The Read/Write Bandwidth chart shows read and write activity on all file systems, all servers one file system, or a specific server, or over time.

Depending on the view selected, the chart notation and display adjusts to occupy the full vertical range of the chart. This chart shows zero read or write operations across the center-line and values greater than zero expanding from the center-line. Read operations are shown above the center line; write operations are shown below the center line. This chart is displayed when File Systems are selected for display (default), or servers, or targets are selected.

![md_Graphics/read-write-bandwidth-hover.png][f9.7]


**Features**

- Mouse over any point on the chart to learn the date/time of this measurement and the read and write values at that time.
- Click **Change Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4).  Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.
- Click **Read** or **Write** to view only read or write information on the chart.

**View this chart for a specific file system**

This chart is displayed by default for all file systems. To view this chart for a single file system:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **File System** (default).
1. At the File System drop-down menu, select the file system. Then click **Update**.

**View this chart for a specific OST**

To view this chart for a single OST:

1. On the Dashboard, click **Configure Dashboard**.
1. Select Server.
1. At the Server drop-down menu, select the server hosting the desired target.
1. At the Target drop-down menu, select the desired OST. Then click **Update**.

**Configure the Read/Write Bandwidth chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.


### <a id="9.2.5"></a>Metadata Servers chart

This chart shows the percentage of CPU and RAM resources consumed on all metadata server(s) in all file systems, over time. This chart is displayed when all File Systems are selected on the Dashboard window (default). You can also view this chart for a single file system.
![md_Graphics/Metadata_Servers_Chart.png][f9.8]


**Features**

- Mouse over any point on the chart to learn the date/time of this measurement and the values at that time.
- Click **Change Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.
- Click **CPU** or **RAM** to select/deselect to view only that information on the chart.

**View this chart for a specific file system**

This chart is displayed by default for all file systems. To view this chart for a single file system:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **File System** (default).
1. At the **File System** drop-down menu, select the file system. Then click **Update**.

**Configure the Metadata Servers chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.



### <a id="9.2.6"></a>Object Storage Servers chart

The Object Storage Servers chart shows the percentages of CPU and RAM resources used on object storage servers (in all file systems) over time. This chart is displayed when File Systems are selected on the Dashboard window (default).  This chart can also be displayed for a single file system.
![md_Graphics/Object_Storage_Servers_Chart.png][f9.9]

**Features**

- Click **Change Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4).  Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.
- Click **CPU** or **RAM** to select/deselect to view only that information on the chart.

**View this chart for a specific file system**

This chart is displayed by default for all file systems. To view this chart for a single file system:

1. On the Dashboard, click **Configure Dashboard**.
1. Select **File System** (default).
1. At the **File System** drop-down menu, select the file system. Then click **Update**.

**Configure the Object Storage Servers chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.



### <a id="9.2.7"></a>CPU Usage chart

This chart is visible for an individual server. The chart shows the percentages of CPU activity attributed separately to:

- user-level processes
- system-level processes
- processes in an IO Wait state

Data is displayed for the specific metadata server or object storage server selected, over time.
![md_Graphics/CPU_Usage_Chart.png][f9.10]


- Mouse over any point on the chart to learn the date/time of this measurement and the values at that time.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.
- Click **user**, **system**, or **iowait** to select/deselect to view only that information on the chart.

**View this chart**

1. On the Dashboard, click **Configure Dashboard**.
1. Select **Server**.
1. Under *Server*, select the server of interest and click **Update**.

**Configure the CPU Usage chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the Start and End times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.


### <a id="9.2.8"></a>Memory Usage chart

For an individual metadata server or object storage server selected, the Memory Usage chart shows:

- the total amount of RAM memory present
- the amount of RAM currently used
- the total swap space currently available
- the amount of swap space being used.

Data is displayed for the server selected, over time.
![md_Graphics/Memory_Usage_Chart.png][f9.11]


**Features**

- Mouse over any point on the chart to learn the date/time of this measurement and the values at that time.
- Click **Change Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.
- Click any of the display icons: **Total memory**, **Used memory**, **Total swap**, **Used swap** to display only your selected parameters.

**View this chart**

1. On the Dashboard, click **Configure Dashboard**.
1. Select **Server**.
1. Under **Server**, select the server of interest and click **Update**.

**Configure the Memory Usage chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.


### <a id="9.2.9"></a>Space Usage chart

This chart is displayed for a selected MDT or OST and shows percentage of file system space consumed on a target over time.
![md_Graphics/Space_Usage_Chart.png][f9.12]



**Features**

- Mouse over any point on the chart to learn the date/time of this measurement and the values at that time.
- Click **Change Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4).  Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.

**View this chart**

1. On the Dashboard, click **Configure Dashboard**.
1. Select **Server**.
1. At the **Server** drop-down menu, select the sever hosting the desired target.
1. At the **Target** drop-down menu, select the desired target. Then click **Update**.

**Configure the Space Usage chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.


### <a id="9.2.10"></a>File Usage chart

This chart is displayed for a selected MDT and shows the percentage of available files (inodes) used over time. Data is displayed for the specific metadata target selected.
![md_Graphics/File_Usage_Chart.png][f9.13]

**Features**

- Mouse over any point on the chart to learn the date/time of this measurement and the values at that time.
- Click **Change Duration** to set the total time duration to Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4).  Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day.
- Click **Full Screen** to fill the browser window with this chart. Click **Exit Full Screen** to return to the normal view.

**View this chart**

1. On the Dashboard, click **Configure Dashboard**.
1. Select **Server**.
1. At the **Server** drop-down menu, select the server hosting the desired target.
1. At the **Target** drop-down menu, select the desired MDT. Then click **Update**.

**Configure the File Usage chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.


### <a id="9.2.11"></a>Object Usage chart

This chart is displayed for a selected OST and shows the percentage of metadata objects used over time. Data is displayed for the object storage target selected.
![md_Graphics/Object_Usage_Chart.png][f9.14]


**View this chart**

1. On the Dashboard, click **Configure Dashboard**.
1. Select **Server**.
1. At the **Server** drop-down menu, select the server hosting the desired OST.

**Configure the Object Usage chart**

1. Click **Configure**.
1. Click **Set Duration** and enter a time period over which samples will be taken. Enter Minutes (1-60), Hours (1-24), Days (1- 31), or Weeks (1-4). Note that for long durations, the map will be divided over several days, with sample periods starting at different times of the day. The value given is an average for that sample period.
1. Click **Set Range** to set the **Start** and **End** times and dates over which measurements will be displayed. This  view of the chart is a static snapshot, starting and ending as configured.
1. Click **Update** to apply and close this window.

[Top of page](#9.0)


## <a id="9.3"></a>Configuration menu

The Configuration menu provides access to the following windows, to let you create and manage file systems:

- The [Server window](#9.3.1) lets you configure a new server for a new file system or add a server to an existing file system.
- At the [Power Control window](#9.3.2), you can configure power distribution units and outlets, and assign servers to PDU outlets to support high availability/failover.
- At the [File Systems window](#9.3.3), you can create a new file system or manage a file system.
- The [HSM window](#9.3.4) configure and monitor hierarchical storage management (HSM) activities. You can also add a copytool to a worker agent and assign that tool instance to a file system.
- The [Storage window](#9.3.5) lists detected storage module plug-ins (provided by third parties), which may provide configuration, status, and/or failover control of RAID based storage devices, depending entirely on the plug-in.
- At the [Users window](#9.3.6), add and configure superusers and users. Superusers are administrators.
- Add volumes and configure those volumes for high availability at the [Volumes window](#9.3.7).
- The [MGTs window](#9.3.8) lets you configure the management target.


### <a id="9.3.1"></a>Server Configuration window

The Server Configuration window is shown next. This is an example configuration only.
![md_Graphics/config_servers.png][f9.15]

This window supports the range of server configuration tasks. For instructions on how to add servers, see [Add one or more HA servers](Creating_new_lustre_fs_3_0.md/#3.4).

Under Server Configuration, you can:

- Add an object storage server. Click **+ Add Server** or **+ Add More Servers**.
- View existing servers for all file systems.
- View **Server State**: This indicator tells you the alert status for that server. A green check mark indicates that all is well with that server. A red exclamation mark indicates an active alert has been generated for this server; you can mouse over the exclamation mark to learn the cause of the alert. See [View all status messages](#9.6a) for more information.
- View the **Profile** associated with each server. When you add a new server, you select the server profile for that server. The profile defines the role of that server. There are generally four server profiles available, however your installation may list more. The four common server profiles are:
    - *Managed storage server*
    - *Monitored storage server*
    - *POSIX HSM Agent Node*
    - *Robinhood Policy Engine server*
- Determine **LNet state** for a given server. Possible LNet states are: *LNet up*, *LNet down*, and *LNet unloaded*.
- Click on the server name (hostname) to open a [Server Detail window](#9.3.1.1) to learn more about that server and access configuration options.
- Under **Actions**, specific to each server, you can perform the following commands. These commands are used primarily to decommission servers. See [Decommissioning a server for an MGT, MDT, or OST](Manage_maintain_HA_lustre_fs_5_0.md/#5.13).
    - **Reboot**: Initiate a reboot on this server. If this server is configured as the primary server of an HA pair, the file system will failover to the secondary server until this server is back online. The file system will then fail back to the primary server. If this is not configured as an HA server, then any file systems or targets that rely on this server will be unavailable until rebooting is complete.
    - **Shutdown**: Initiate an orderly shutdown on this server. If this server is configured as the primary server of an HA pair, the file system will failover to the secondary server. If this is not configured as an HA server, then any file systems or targets that rely on this server will be unavailable until this server is rebooted.
    - **Warning**: If this is not configured as an HA server, then any file systems or targets that rely on this server will also be removed.
    - **Power Off**: Switch power off for this server. Any HA-capable targets running on the server will be failed-over to a peer. Non-HA-capable targets will be unavailable until power for the server is switched on again. This action is visible only if PDUs have been added and outlets assigned to servers.
    - **Power On**: Switch power on for this server. This action is visible only if PDUs have been added and outlets assigned to servers, and after the server has been powered-off at PDU.
    - **Power Cycle**: Switch power off and then back on again for this server. Any HA-capable targets running on the server will be failed over to a peer. Non-HA-capable targets will be unavailable until the server has finished booting. This action is visible only if PDUs have been added and outlets assigned to servers.
    - **Remove**: Remove this server. If this server is configured as the primary server of an HA pair, then the file system will failover to the secondary server. If it is not configured as an HA server, then any file systems or targets that rely on this server will also be removed.
    - **Force Remove**: This action removes the record for the storage server in the manager database, without attempting to contact the storage server. All targets that depend on this server will also be removed without any attempt to unconfigure them. **Warning: You should only perform this action if the server is permanently unavailable**.

Under **Server Actions**, you can perform the commands listed next. Note that these commands are *bulk action commands*. This means that when you click one of the following commands, you can then select which server(s) to perform this command on. You can enter a host name or host name expression in the file to generate a list of existing servers. You can choose **Select All**, **Select None**, or **Invert Selection**. At the far right, under *Select Server*, you can also select or deselect a server. After selecting the desired server(s), you can proceed to perform the command and it will be run on all selected servers.

- **Detect File Systems**: Detect an existing file system to be monitored at the manager GUI.
- **Re-write Target Configuration**: Update each target with the current NID for the server with which it is associated. This is necessary after making changes to server/target configurations and is done after rescanning NIDs. Also see [Handling network address changes](Manage_maintain_HA_lustre_fs_5_0.md/#5.9) (updating NIDs).
- **Install Updates**: When an updated release of Integrated Manager for Lustre software is installed on the *manager* server, a notification is displayed in the manager GUI indicating that updated software is also available for installation on a managed server or servers and the *Install Updates* button becomes enabled. After clicking the **Install Updates** button, a list of servers (default: all) to be included in this update operation is displayed in the Update dialog. Clicking the **Run** button in this dialog will cause the updated packages to be installed on the managed servers.



#### <a id="9.3.1.1"></a>Server Detail window

Each Server Detail window contains the full extent of information for that server. To open a Server Detail window, click **Configuration > Servers**, and then click on the server of interest.

This window is divided into five sections:

- [Server Detail](#9.3.1.1a)
- [Pacemaker configuration](#9.3.1.1b)
- [Corosync configuration](#9.3.1.1c)
- [LNet detail](#9.3.1.1d)
- [NID configuration](#9.3.1.1e)


**<a id="9.3.1.1a"></a>Server Detail**

This section lists:

- **Address**: This is the IP address or the node name.
- **State**: The type of server, HA managed or unmanaged.
- **FQDN**: Fully qualified domain name
- **Node name**: The name previously assigned to this node.
- **Profile**: Indicates the profile assigned to this server during the Add Server process, including the OS.
- **Boot time**: Date of last boot
- **State changed**: Date of last State change; see State above.
- **Alerts**: Any alerts received pertinent to this server.

Click the **Actions** menu to access the following commands that are available for this server:

- **Reboot**: Initiate a reboot on this server. If this server is configured as the primary server of an HA pair, the file system will failover to the secondary server until this server is back online. The file system will then fail back to the primary server. If this is not configured as an HA server, then any file systems or targets that rely on this server will be unavailable until rebooting is complete.
- **Shutdown**: Initiate an orderly shutdown on this server. If this server is configured as the primary server of an HA pair, the file system will failover to the secondary server. If this is not configured as an HA server, then any file systems or targets that rely on this server will be unavailable until this server is rebooted.
- **Power Off**: This will switch power off for this server. If this is a primary server to any targets, those targets will be failed-over to the secondary server. Non-HA-capable targets (targets not supported by a secondary server) will be unavailable until power for the server is switched on again. This action is visible only if PDUs have been added and outlets assigned to servers.
- **Power Cycle**: Switch power off and then back on again for this server. Any HA-capable targets running on the server will be failed over to a peer. Non-HA-capable targets will be unavailable until the server has finished booting. This action is visible only if PDUs have been added and outlets assigned to servers.
- **Remove**: Remove this server. If this server is configured as the primary server of an HA pair, then the file system will failover to the secondary server. If it is not configured as an HA server, then any file systems or targets that rely on this server will also be removed.
- **Force Remove**: This action removes the record for the storage server in the manager database, without attempting to contact the storage server. All targets that depend on this server will also be removed without any attempt to unconfigure them. Warning: You should only perform this action if the server is permanently unavailable.


**<a id="9.3.1.1b"></a>Pacemaker configuration**

Pacemaker configuration and enabling is performed automatically by Integrated Manager for Lustre software. However, an administrator may need to reset or configure Pacemaker when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with Pacemaker.

Click the **Actions** menu to access the following commands:

- **Stop Pacemaker**: This command stop Pacemakers. If this is a primary server, then failover to the secondary server occurs. The file system remains available but not in a high-availability state.
- **Unconfigure Pacemaker**: This command stops and unconfigures Pacemaker. If this is a primary server, then failover to the secondary server occurs. The file system remains available but not in a high-availability state.
- **Configure Pacemaker**: Visible if Pacemaker is unconfigured. This command configures Pacemaker, but does not start it. To start Pacemaker and restore this server to HA capability, click **Start Pacemaker**.
- **Start Pacemaker**: Visible if Pacemaker is stopped or unconfigured. Start Pacemaker to restore this server to HA capability. If failover has occurred from this server to the backup server, then after starting Pacemaker, manually failback the affected target(s) to this primary server. To do this, open the Status window, locate any warnings for target(s) running on the secondary server (and served by this primary server) and under Actions, click **Failback**.


**<a id="9.3.1.1c"></a>Corosync configuration**

Corosync configuration and enabling is performed automatically by Integrated Manager for Lustre software. However, an administrator may need to reset or configure Corosync when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with Corosync.

Click the **Actions** menu to access the following commands:

- **Stop Corosync**: This command stops Corosync and also stops Pacemaker. If this is a primary server, then failover to the secondary server occurs. The file system remains available, but not in a high-availability state. Corosync must be restarted before Pacemaker can be started again.
- **Unconfigure Corosync**: This command stops and unconfigures Corosync and also stops Pacemaker. If this is a primary server, then failover to the secondary server occurs. The file system remains available, but not in a high-availability state. Corosync must be restarted before Pacemaker can be started again.
- **Configure Corosync**: Visible if Corosync is unconfigured. This command will configure Corosync, but not start it. To configure and start Corosync, click **Start Corosync**. After Corosync is started, you need to start Pacemaker.
- **Start Corosync**: Visible if Corosync is stopped or unconfigured. After Corosync is started, you also need to start Pacemaker. If failover occurred from this server to the backup server, then after Corosync and Pacemaker are running, you need to manually failback the affected target(s) to this primary server. See Start Pacemaker, above.

Click **Configure** to change the mcast port number.


**<a id="9.3.1.1d"></a>LNet detail**

LNet operations for a given server may need to be reset during maintenance. Doing so will take this server and any volumes it hosts offline, and depending on the server, will degrade or stop the file system.

Click the **Actions** menu to access the following commands:

- **Stop LNet**: Shut down the LNet networking layer and stop any targets running on this server.
- **Unload LNet**: If LNet is running, stop LNet and unload the LNet kernel module to ensure that it will be reloaded before any targets are started again.
- **Load LNet**: Load the LNet kernel module for this server.
- **Start LNet**: Start LNet.


**<a id="9.3.1.1e"></a>NID configuration**

An administrator may need to reconfigure NIDs for a server when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with network interfaces. For each interface, you can set the network driver and assign the Lustre network. To be able to edit NID configuration, the file system first needs to be taken offline. Perform these steps:

1. At the menu bar, click **Configuration > File Systems**.
1. For the listed file system, select **Stop** under *Actions*.
1. Return to the Server Detail window for the server in question. Click **Configuration > Servers**. Click on the desired server.
1. Under NID Configuration, click **Configure**.
1. The IP address is not editable.  At the Network Driver drop-down menu, the available driver types are dependent on the network interface. Select the appropriate driver.
1. If you are ready to place the file system online again, click **Configuration > File Systems**. Then, for this file system, select **Start** under **Actions**.


### <a id="9.3.2"></a>Power Control window

The Power Control window accessed from the Configuration menu is shown next.
![md_Graphics/Power_Control_Tab.png][f9.16]

The Power Control window lets you configure and manager power distribution units. In this window you can add a detected PDU and then assign specific PDU outlets to specific servers. Once configured, this feature lets you check the status of PDUs and individual outlets. Based on server power requirements and your failover configuration, you may want to assign more than one outlet to a server. For improved failover performance, assign the failover outlet from a different PDU than the primary outlet. When you associate PDU failover outlets with servers using this tool, STONITH is automatically configured. Note that primary and secondary servers for each target must first be configured on the Volumes window.

See [Add power distribution units](Creating_new_lustre_fs_3_0.md/#3.6).


### <a id="9.3.3"></a>File Systems window

The *File Systems* window accessed from the *Configuration* menu is shown next.
![md_Graphics/config_file_systems.png][f9.17]

The *File Systems* window lets you configure, view and manage multiple file systems.

Click **Create File System** (or **Create More File Systems**) to begin the process of creating a new file system. See [Create a new Lustre file system](Creating_new_lustre_fs_3_0.md/#3.0).

Under Current File Systems, for each file system you can:

- view the file system name
- view the management server (MGS)
- view the metadata server (MDS)
- view the number of connected clients
- view total file system capacity (Size)
- view available free space
- check file system status. A green check mark ![md_Graphics/check_mark.png][f9.18] indicates that the file system is operating normally. No warnings or error messages have been received.

Under Actions, you can:

- **Remove** the file system: This file system is removed and will not be available to clients. However, the file system's contents will remain intact until its volumes are reused in another file system.
- **Stop** the file system: This stops the metadata and object storage targets, thus making the file system unavailable to clients. If the file system has been stopped, click **Start** to restart the file system.

To view the full display of file system parameters, click on the file system name in the left column. See [View All File System Parameters](Monitoring_lustre_fs_4_0_0.md/#4.4).


### <a id="9.3.4"></a>HSM window

After Hierarchical Storage Management (HSM) has been configured for a file system, this HSM Copytool chart displays a moving time-line of waiting copytool requests, current copytool operations, and the number of idle copytool workers. For information about setting up HSM for a file system, see [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0).

![md_Graphics/HSM_Operations.png][f9.19]


On this window, you can:

- Select to display copytool operations for all file systems (default), or one you select.
- Mouse over the graph to learn the specific values at a given point in time.
- Use Change Duration to change the time period for the range of data displayed on the HSM Copytool chart. The chart begins at a start time set and ends now. You can set this to select Minutes, Hours, Days or Weeks, up to four weeks back in time and ending now. The most recent data displayed on the right. The number of data points will vary, based primarily on the duration.
- Click **Actions > Disable** to pause the HSM coordinator for this file system (pause HSM activities). New requests will be scheduled and HSM activities will resume after the HSM coordinator is enabled. To enable again, click **Actions > Enable**.
- Click **Actions > Shutdown** to stop the HSM coordinator for this file system. No new requests will be scheduled.

If a copytool has been added but never configured or started, then click **Actions** to show the following menu:

- **Start** - Configure and Start this copytool to begin processing HSM requests.
- **Remove** - Deconfigure and remove this copytool from the manager database. It will no longer appear on this HSM window. This is the best way to remove a copytool.
- **Configure** - Configure this copytool on the worker. Do not start the copytool. Status will show as Configured.
- **Force Remove** - Remove this copytool from the manager database without deconfiguring this copytool on the worker node. It will no longer appear on this HSM window. This is NOT the best way to remove a copytool, because a later attempt to add this copytool back will fail unless it is manually reconfigured. Only consider using Force Remove if Remove has failed.

To learn about HSM capabilities supported in Integrated Manager for Lustre software, see [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0).


### <a id="9.3.5"></a>Storage window

The *Storage* window lists detected storage module plug-ins (provided by third parties), which may provide configuration, status, and/or failover control of RAID based storage devices, depending entirely on the plug-in. If no plug-ins are detected, none are listed. The layout and information displayed on this window is dependent on the storage plug-in(s).
-->

### <a id="9.3.6"></a>Users

If you are a superuser, you can view, create, and manage users by clicking **Management > Users** at the top of the page.

![md_Graphics/config_users.png][f9.20]

The following types of users exist:

- **File system user** - File system users have full GUI access except for the Management menu, which is hidden from view. The logged-in users cannot create or manage a file system, but can use Dashboard and Activity views to monitor file systems.
- **Superuser** - Superusers, such as file system administrators, have full access to the application, including the Management menu. The logged-in users can create, monitor, manage, and remove file systems and their components. <!-- The users can also create, modify (change passwords), and delete other users, including superusers, but cannot delete its own account. For more information, see [Creating User Accounts](Getting_started_2_0.md/#2.1). -->

Superusers also have these options by clicking a user's account:

- **Details** - View and change the username, email, first and last names.
- **Password** - (Coming soon) Change the password.
- **Email Notifications** - (Coming soon) Select events for email notifications. <!-- If nothing is selected, all events except for "Host contact alerts" are included. For more information, see [Setting up Email Notifications](Getting_started_2_0.md/#2.2). -->

[Top of page](#9.0)

<!--
### <a id="9.3.7"></a>Volumes

To view storage volumes, click **Management > Volumes** on the top of the Dashboard page.

![md_Graphics/config_volumes.png][f9.21]

Volumes, also called LUNs or block devices, are the underlying units of storage for creating file systems. Each file system target corresponds to a single volume.

For each volume, you will see the path, the size, and the hosts.

If volume hosts are configured for high availability, primary and secondary hosts can be designated for a volume. A volume may be accessible on one or more hosts via different device nodes, and it may be accessible via multiple device nodes on the same host.

<!--
On the *Volume* window, you can do the following:

- Set or change the Primary Server and Failover Server for each volume. Each change you select to make will be displayed in orange, indicating that you have selected to change this setting, but have not applied it yet. Changes you make on the Volumes Configuration window will be updated and displayed after clicking **Apply** and **Confirm**. After confirming the change, the orange setting turns white. Other users viewing this file system's Volume Configuration window will see these updated changes after you apply and confirm them. If you select to change a setting (it becomes orange), you can click **X** to cancel that selection (it turns white and returns to the original setting). To cancel all changes you have selected (but not yet applied), click **Cancel**.

    **Note:** There is currently no lock-out of one user's changes versus changes made by another user. The most-recently applied setting is the one in-force and displayed.
- View the status of all volumes in all file systems.
- View each volume's name, primary server, failover server, volume size, and volume status.
    - A green Status light for the volume indicates that the volume has a primary and failover server.
    - A yellow Status light means that there is no failover server.
    - A red Status light indicates that this volume is not available.
-->
<!--
### <a id="9.3.8"></a>MGTs window

The *MGT* window accessed from the *Configuration* menu is shown next.
![md_Graphics/config_volumes.png][f9.22]
At the MGT window, you can do the following:

- View your existing management target (if configured). Here you can determine the Capacity, Type, and high availability (HA) Status of the MGT. If this is an HA target, then the primary and secondary servers are identified. A green check mark ![md_Graphics/check_mark.png][f9.18] indicates this target and server are functioning normally.
- Select storage for a new MGT and then create a new MGT. This task is not common; MGTs are created when you click **Create File System** at the *Configuration > File Systems* window.

Under MGT Configuration for an existing MGT, you can perform these actions under **Actions**:

- **Stop**: Stop the MGT. When an MGT is stopped, clients are unable to make new connections to the file systems using this MGT. However, the MDT and OST(s) stay up if they were started before this MGT was stopped, and can be stopped and restarted while this MGT is stopped.
- **Failover**: Clicking Failover will forcibly migrate the target to its failover server. Clients attempting to access data on the target while the migration is in process may experience delays until the migration completes. If this action is not displayed, then the MGT has already failed-over and this button will display as Failback. Otherwise, a secondary server has not been configured.
- **Failback**: Migrate the target back to its primary server. Clients attempting to access data on the target while the migration is in process may experience delays until the migration completes. This action is displayed only after a target has failed-over.

[Top of page](#9.0)
-->

<!--
## <a id="9.4"></a>Job Stats window

The Job Stats window is accessible at the top menu bar. Click **Job Stats**.

Clicking **Job Stats** opens the Job Stats window and reveals the top five jobs currently in process. The listed jobs can be sorted by column and average duration can be selected. Column sorts and duration selections are persistent if you leave and later return to this window.

**Note:** Job stats need to be enabled before then can be viewed. See [View Job stats](Monitoring_lustre_fs_4_0_0.md/#4.3).
![md_Graphics/job_stats.png][f9.4]

On the [Read/Write Heat Map](#9.2.1) (on the Dashboard), you can also click a heat map cell and go to the Job Stats screen for that OST. Doing so will present a static view of job stats for the selected OST. Because it is static, *Duration* is not selectable.

[Top of page](#9.0)
-->

## <a id="9.5"></a>Logs

To view logs, log in to the management interface, and then click **Logs** on the right. The view will expand and display a paginated list of logged events.

![md_Graphics/logs.png][f9.23]

<!-- You can filter logs by date range, host, service, and messages from Lustre or all sources. You can also use auto-completion for search and host name links to jump to host information. -->

You can identify each logged event by time, service, message, and host.

As an example of logged events, consider what happens if a failover takes place:

- A red alert appears briefly to notify you of related unresolved warnings.
- In the Activity view, another alert appears saying that the server has failed over. Other related alerts are also displayed.
- In file system details, an alert is displayed and the server, on which the target is now running, is shown in the Started On column for that target.
- The superuser receives a configured email alert.

An event is logged for each case above, and you can see it displayed in **Logs**.

[Top of page](#9.0)

## <a id="9.6"></a>Activities

Activity messages provide information about the functioning and health of a managed file system. You do not need to be logged in to view activity messages.

To view activity messages, click **Activity** on the right of the page. The view will expand and display a paginated list of all file system activities, listing most recent messages first.

![md_Graphics/activities.png][f9.24]

The counter next to the activity icon reflects the number of active issues with the cluster. The color of the icon will change between green, yellow, and red according to the severity of the highest active issue.

There are five types of activity messages:

- **Command running**: Marked with gray color, these messages inform you of commands currently in progress.<!-- These are the commands that you have entered into the manager GUI.-->
- **Command successful**: Marked with green color, these messages identify successfully completed commands. To learn about the underlying commands and their syntax, click **Details**, and then click a command link.
- **Info messages**: Marked with blue color, these messages inform you of normal transitions that occur at a single point in time during the creation or management of the file system, often in response to a command entered into the GUI. A single command may cause several such events to occur.
- **Warning alerts**: Marked with yellow color, these messages usually indicate that the file system is operating in degraded mode; for example, when a target fails over, high availability is no longer true for that target. A warning message marks a status change that has a specific **Begin** and **End** time. A warning is active at the beginning of the status change and inactive at the end of the status change; for example, a warning message may inform you that an OST has gone offline, and that message is active until the OST becomes operational again. Not all warnings necessarily signify a degraded state; for example, a target recovery to a failover server signifies that the failover occurred successfully.
- **Error alerts**: Marked with red color, these messages indicate that the file system is down or severely degraded, that one or more file system components are currently unavailable. For example, both primary and secondary servers for a target are not running. An error often has a remedial action you can take by clicking the button.

<!--
**Running common searches**

At the Status window, under the **Common Searches** drop-down, select a search to run.

You can modify any of the listed searches. To do this, select a search type, edit the string displayed in the Search bar, and click **Search** or press **Enter**.

- **Search active alerts**: Display active alerts (warnings and errors) that reflect the current state of the file system. This search lists only warnings and errors that have not been resolved.
- **Search alerts**: Display all alerts (warnings and errors) generated since the creation of the file system. This includes active (unresolved) and inactive (resolved) alerts.
- **Search commands**: Display all commands, those successfully executed and those that are currently in process.
- **Search events**: Display all information messages occurred since the creation of the file system.
-->

Before you see an unresolved filesystem error or warning in the Activity view, this error or warning briefly pops up on the red bar across the page. Clicking **Details** on the bar will open the Status window and display the alerts.

![md_Graphics/red_status_bar.png][f9.25]

[Top of page](#9.0)

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
[Top of page](#9.0)
-->

<!--
## <a id="9.7"></a>Resources

You can see a tree view of resources on the left of the Dashboard page.

![f9.26]

The tree view lists items in real time. You can descend the hierarchy of a file system or server down to a desired resource. Click a resource (file systems, servers, volumes,  targets, and so on) to see a detailed view on the right. Click a chart icon next to the name of a resource to see the Dashboard page with charts displaying metrics specific to the resource. Click inside a chart to add annotation.

When many resources are available, the list will paginate. You can adjust its width by toggling the right edge.

Breadcrumb navigation above the tree view tracks your journey through listed resources.

[Top of page](#9.0)
-->

<!--
## <a id="9.9"></a>Alert bar

This red bar briefly appears if there are any active error or warning alerts on your system. Click **Details** to open the Status window and reveal the current, active alerts.

![f9.25]

[Top of page](#9.0)
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
[f9.19]: md_Graphics/HSM_Operations.png
[f9.20]: md_Graphics/config_users.png
[f9.21]: md_Graphics/config_volumes.png
[f9.22]: md_Graphics/config_mgts.png -->

[f9.23]: md_Graphics/logs.png
[f9.24]: md_Graphics/activities.png
[f9.25]: md_Graphics/red_status_bar.png

<!-- [f9.26]: md_Graphics/treeview.png -->

[f9.27]: md_Graphics/breadcrumbs.png
