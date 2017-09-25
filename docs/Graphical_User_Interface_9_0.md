[**Manager for Lustre\* Online Help Main Table of Contents**](../README.md)

<a id="9.0"></a>
# Graphical User Interface

This section details the Manager for Lustre\* graphical user interface.  Click the desired topic.

- [Dashboard window](#9.1)
- [Dashboard charts](#9.2)
- [Configuration menu](#9.3)
- [Job stats](#9.4)
- [Logs window](#9.5)
- [Status window](#9.6)
- [Resources tree view](#9.7)
- [Breadcrumb navigation](#9.8)
- [Alert bar](#9.9)

## <a id="9.1"></a>Dashboard window

The Dashboard window is shown next.

<a id="f9.1"></a>
![md_Graphics/dashboard.png][f9.1]

The Dashboard displays a set of charts that provide usage and performance data at several levels for each file system. At the top level, this window displays an aggregate view of all file systems you're currently monitoring. You can select to monitor individual file systems and servers by clicking **Configure Dashboard**; See [Configuring the Dashboard](#9.1.2).

To view charts for OSTs and MDT(s), select the specific file system. Then select the desired target(s).

At the top, the Dashboard lists the file system(s) being managed or monitored-only. The following information is provided for each file system:

- *File System name*: The name assigned to this file system during its creation on the Configuration window.
- *Type*: Monitored or Managed. "Managed" file systems are configured and managed for high availability (HA). Managed file systems are both monitored and managed, whereas "monitored" file systems are monitored-only and do not support failover via Manager for Lustre\* software.
- S*pace Used / Total*: This indicates the amount of file system capacity consumed, versus the total file system capacity. 
- *Files Used / Total*: This indicates the total number of inodes consumed by file creation versus the total number of inodes established for this file system.
- Clients: Indicates the number of clients accessing the file system at this moment.

Data used to produce the charts is saved for long-term use. Data is averaged and compressed over time so that the most recent data is stored and viewed at maximum resolution while aging data is stored and viewed at progressively lower resolutions over time.


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


This window also identifies the volume(s), primary server(s), and failover server(s) for the MGS, MDT(s) and all OST(s). From this window you can [Update Advanced Settings](Advanced_Topics_10_0.md/#10.1) and
 [View Client Mount Information](Creating_new_lustre_fs_3_0.md/#3.11).


### <a id="9.1.2"></a>Configuring the Dashboard
By default, the Dashboard displays information and charts for all file systems. Click **Configure Dashboard** to open a window to let you do the following:

- To view a file system's charts: Click **File System** (default). You can view information and charts for all file systems, or select a specific file system from the drop-down menu.
- To view a server's charts: Click **Select Server**. You can view information and charts for all servers (on all file systems), or select a specific server from the drop-down menu. 
- To view charts for one or all targets: Click **File System**. Select the desired file system and then select **All Targets** or an individual target.

Click **Update** to apply your choices and **Cancel** to close.

[Top of page](#9.0)

## <a id="9.2"></a>Dashboard charts

Several Dashboard charts provide quick, detailed, visual representation of the performance of your Lustre* file system(s).  You can configure certain data display parameters for each chart, and your chart configuration will persist until you reload/refresh the Dashboard page, using the browser. 

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

- Mouse over any cell on the heat map to learn which OST this is, its file system, its read or write activity, and the actual starting date and time of that measurement period. 
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
- **Install Updates**: When an updated release of Manager for Lustre\* software is installed on the *manager* server, a notification is displayed in the manager GUI indicating that updated software is also available for installation on a managed server or servers and the *Install Updates* button becomes enabled. After clicking the **Install Updates** button, a list of servers (default: all) to be included in this update operation is displayed in the Update dialog. Clicking the **Run** button in this dialog will cause the updated packages to be installed on the managed servers.



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

Pacemaker configuration and enabling is performed automatically by Manager for Lustre\* software. However, an administrator may need to reset or configure Pacemaker when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with Pacemaker.

Click the **Actions** menu to access the following commands:

- **Stop Pacemaker**: This command stop Pacemakers. If this is a primary server, then failover to the secondary server occurs. The file system remains available but not in a high-availability state.
- **Unconfigure Pacemaker**: This command stops and unconfigures Pacemaker. If this is a primary server, then failover to the secondary server occurs. The file system remains available but not in a high-availability state.
- **Configure Pacemaker**: Visible if Pacemaker is unconfigured. This command configures Pacemaker, but does not start it. To start Pacemaker and restore this server to HA capability, click **Start Pacemaker**.
- **Start Pacemaker**: Visible if Pacemaker is stopped or unconfigured. Start Pacemaker to restore this server to HA capability. If failover has occurred from this server to the backup server, then after starting Pacemaker, manually failback the affected target(s) to this primary server. To do this, open the Status window, locate any warnings for target(s) running on the secondary server (and served by this primary server) and under Actions, click **Failback**.


**<a id="9.3.1.1c"></a>Corosync configuration**

Corosync configuration and enabling is performed automatically by Manager for Lustre\* software. However, an administrator may need to reset or configure Corosync when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with Corosync.

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

An administrator may need to reconfigure NIDs for a server when performing maintenance on a server, altering the server's configuration, or troubleshooting problems with network interfaces. For each interface, you can set the network driver and assign the Lustre* network. To be able to edit NID configuration, the file system first needs to be taken offline. Perform these steps:

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

Click **Create File System** (or **Create More File Systems**) to begin the process of creating a new file system. See [Create a new Lustre* file system](Creating_new_lustre_fs_3_0.md/#3.0).

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

To learn about HSM capabilities supported in Manager for Lustre* software, see [Configuring and using Hierarchical Storage Management](Config_and_using_HSM_6_0.md/#6.0).


### <a id="9.3.5"></a>Storage window

The *Storage* window lists detected storage module plug-ins (provided by third parties), which may provide configuration, status, and/or failover control of RAID based storage devices, depending entirely on the plug-in. If no plug-ins are detected, none are listed. The layout and information displayed on this window is dependent on the storage plug-in(s).


### <a id="9.3.6"></a>Users window

The *Users* window accessed from the *Configuration* menu is shown next.
![md_Graphics/config_users.png][f9.20]

The *Users* window lets you create and manage the following accounts types:

- **File system user** - A file system user has access to the full GUI, except for the Configuration drop-down menu, which is not displayed. A file system user cannot create or manage a file system, but can monitor all file systems using the Dashboard, Alerts, and Logs windows. Users log in by clicking **Login** in the upper-right corner of the screen, and log out by clicking **Logout**. 
- **Superuser** - A superuser has full access to the application, including the Configuration drop-down menu and all sub-menus. A superuser can create, monitor, manage, and remove file systems and their components. A superuser can create, modify (change passwords), and delete users. A superuser cannot delete their own account, but a superuser can create or delete another superuser.

See [Creating User Accounts](Getting_started_2_0.md/#2.1) for more information. 

After logging in, a user can modify their own account by clicking Account near the upper-right corner of the screen. A user can set these options:

- **Details** - Username, email address, and first and last name can be changed.
- **Password** - Password can be changed and confirmed.
- **Email Notifications** - The types of events for which this account will receive emailed notifications can be selected from a checklist. If no notifications are selected, email notifications will be sent for all alerts except “Host contact alerts”. See [Setting up Email Notifications](Getting_started_2_0.md/#2.2).

See [Creating User Accounts](Getting_started_2_0.md/#2.1) for more information.


### <a id="9.3.7"></a>Volumes window

The *Volumes* window accessed from the Configuration menu is shown next.
![md_Graphics/config_volumes.png][f9.21]

The *Volumes* window is used to add volumes to a file system. Volumes (also called LUNs or block devices) are the underlying units of storage used to create Lustre* file systems. Each Lustre* target corresponds to a single volume. Only volumes that are not already in use as Lustre* targets or local file systems are shown. If servers in the volume have been configured for high availability, primary and secondary servers can be designated for a Lustre* volume. A volume may be accessible on one or more servers via different device nodes, and it may be accessible via multiple device nodes on the same host.

On the *Volume* window, you can do the following:

- Set or change the Primary Server and Failover Server for each volume. Each change you select to make will be displayed in orange, indicating that you have selected to change this setting, but have not applied it yet. Changes you make on the Volumes Configuration window will be updated and displayed after clicking **Apply** and **Confirm**. After confirming the change, the orange setting turns white. Other users viewing this file system's Volume Configuration window will see these updated changes after you apply and confirm them. If you select to change a setting (it becomes orange), you can click **X** to cancel that selection (it turns white and returns to the original setting). To cancel all changes you have selected (but not yet applied), click **Cancel**.
 
    **Note:** There is currently no lock-out of one user's changes versus changes made by another user. The most-recently applied setting is the one in-force and displayed.
- View the status of all volumes in all file systems.
- View each volume's name, primary server, failover server, volume size, and volume status.
    - A green Status light for the volume indicates that the volume has a primary and failover server. 
    - A yellow Status light means that there is no failover server. 
    - A red Status light indicates that this volume is not available. 


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

## <a id="9.4"></a>Job Stats window

The Job Stats window is accessible at the top menu bar. Click **Job Stats**. 

Clicking **Job Stats** opens the Job Stats window and reveals the top five jobs currently in process. The listed jobs can be sorted by column and average duration can be selected. Column sorts and duration selections are persistent if you leave and later return to this window.

**Note:** Job stats need to be enabled before then can be viewed. See [View Job stats](Monitoring_lustre_fs_4_0_0.md/#4.3).
![md_Graphics/job_stats.png][f9.4]

On the [Read/Write Heat Map](#9.2.1) (on the Dashboard), you can also click a heat map cell and go to the Job Stats screen for that OST. Doing so will present a static view of job stats for the selected OST. Because it is static, *Duration* is not selectable.

[Top of page](#9.0)


## <a id="9.5"></a>Logs window

The *Logs* window is shown next.
![md_Graphics/logs.png][f9.23]

The **Logs** window displays log information and allows filtering of events by date range, host, service, and messages from Lustre* or all sources. The Logs window also features auto-complete search functions and linkable host names.

The logs window also features querying with auto-complete and linkable host names. 

For example, if a failover event takes place, the following occurs:

- The red Alert bar will appear briefly to notify you of active warning alerts related to the failover. 
- An alert is displayed with a message on the Status window that a server has failed over. Other related alerts will be displayed.
- The alert icon appears on the Configuration > File System window for the file system. The server on which the target is now running is shown in the Started On column for that target.
- An email alert is sent to the superuser. See the documentation provided by your storage solution provider for how to configure your mail server to enable and set up email alerts.

Each of the above items generates a log message which is generated and displayed on the Logs window.

[Top of page](#9.0)


## <a id="9.6"></a>Status window

The *Status* window provides messages about the functioning and health of each managed file system. 
The Status window is shown next.
![md_Graphics/status_page.png][f9.24]

The *Status* window shows current active and past alerts. 


**<a id="9.6a"></a>View all status messages**

Click **Status** to view all status messages. All messages are displayed most-recent first. Note that *warning* and *error* messages are displayed as alerts.  The Status window displays messages in five categories:

- *Command Running*: These messages are gray in color and inform you of commands that are currently in progress / running. These are commands that you have entered into the manager GUI.
- *Command Successful*: These messages are green in color and identify commands that have completed successfully. You can click **Details** and then click the command link to learn about underlying commands and their syntax. 
- *Info messages*: These messages are displayed in blue. Events are normal transitions that occur during the creation or management of the file system, often in response to a command entered into the GUI. A single command may cause several events to occur. An event message informs you of an event occurring at a single point in time. 
- *Warning alerts*: Warnings are displayed in orange. A warning usually indicates that the file system is operating in a degraded mode, for example a target has failed over so that high availability is no longer true for that target. A warning message marks a status change that has a specific **Begin** and **End** time. A warning is active at the beginning of the status change and inactive at the end of the status change. For example, a warning message may inform you that an OST has gone offline, and that message is active until the OST becomes operational again. Not all warnings necessarily signify a degraded state; for example a target recovery to a failover server signifies that the failover occurred successfully. 
- *Errors alerts*: Errors are displayed in red. An error message indicates that the file system is down or severely degraded. One or more file system components are currently unavailable, for example both primary and secondary servers for a target are not running. An error often has a remedial action you can take by clicking the button.

**Common Searches**

At the Status window, under the **Common Searches** drop-down menu, you can select from the searches listed next. 

Note that you can modify any of the searches below. First select the search type. Then edit the string that is displayed in the *Search* field, and click **Search** or press the Enter key.

- **Search active alerts**: Display active alerts (warnings and errors) that currently reflect the state of the file system. This search will list only active warnings and errors that have not been resolved.
- **Search alerts**: Display all alerts (warnings and errors) that have been generated since the file system was created. This includes active and inactive alerts (alerts that have been resolved).
- **Search commands**: Display all commands that have successfully executed and those that are currently in process.
- **Search events**: Display all information messages (events) that have occurred since the file system was created.

**Alert bar**

Note that the red Alert bar briefly appears on the GUI if there are any active error or warning alerts on your system. Clicking **Details** opens the Status window and reveals the current, active alerts.

![md_Graphics/red_status_bar.png][f9.25]

**Using the Search field**

The Status window also incorporates an auto-complete search function.  Simply begin entering text into the search field to use this feature. 

You can run searches using the following rules:

1. Keywords can be filtered using the equals sign (=) or "in" keywords. Examples: 
    - `severity = ERROR`
    - `severity in [WARNING, ERROR]`
1. Filters can be joined using the "and" keyword. Example:
    - `severity = ERROR and active = true`

The following table lists field names, associated types, and information about that field. 

|Field name|Type|Field description|
|---|---|---|
|active|boolean|True or False depending if record is active|
|record_type|string|Identifying type of the record|
|severity|string|String indicating the severity one of ['INFO', 'DEBUG', 'CRITICAL', 'WARNING', 'ERROR']|

Here is an example query:
```
active = true
record_type = CorosyncNoPeersAlert
severity in [ERROR, WARNING]
```

[Top of page](#9.0)

## <a id="9.7"></a>Resources tree view

The following image is a partial display of the Resources tree view.

![f9.26]

The Resources tree view is a tree listing of resources in the selected file system. It lists items in real time and lets you descend the file system hierarchy to the desired resource.  You can click a resource (file systems, servers, volumes, and targets) to view that resource in the tree, and click its metrics link to view that resource's metrics. This pane displays pages when many records are available. You can size this pane by dragging its edge drawer.

[Top of page](#9.0)

## <a id="9.8"></a>Breadcrumb navigation

Breadcrumb navigation lets you see where in the hierarchy of the GUI you currently are.

Navigating between pages is now tracked by breadcrumbs. The breadcrumb path is shown at the upper-left of the page. 

![f9.27]

Breadcrumbs display a path, outlining the steps taken to arrive at the current page. Breadcrumb navigation is reset when selecting a link from the Menu, or when selecting an item from the Resources tree view pane. 

If you create a cycle, the breadcrumbs will automatically slice up to the current location, preventing an unnecessary build-up of items. Another key feature of this feature is that it always has a starting point of reference. If you drill down to a target and then refresh the page, the target will now be the only item in the breadcrumb list, because the page will start at that location.

If you click the Back button and the browser indicates that it is going to a previous page not in the breadcrumbs list, the new page will act as the starting breadcrumb location. This prevents a "reverse build-up" of breadcrumbs.

[Top of page](#9.0)

## <a id="9.9"></a>Alert bar

This red bar briefly appears if there are any active error or warning alerts on your system. Click **Details** to open the Status window and reveal the current, active alerts.

![f9.25]

[Top of page](#9.0)


[f9.1]: md_Graphics/dashboard.png
[f9.2]: md_Graphics/file_system_params.png
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
[f9.22]: md_Graphics/config_mgts.png
[f9.23]: md_Graphics/logs.png
[f9.24]: md_Graphics/status_page.png
[f9.25]: md_Graphics/red_status_bar.png
[f9.26]: md_Graphics/treeview.png
[f9.27]: md_Graphics/breadcrumbs.png