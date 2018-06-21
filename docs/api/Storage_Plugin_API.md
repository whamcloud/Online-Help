# <a name="1.0"></a>Storage Plugin Developer's Guide for Integrated Manager for Lustre software

[**Software API Documentation Table of Contents**](./api_TOC.md)

## <a name="1.1"></a>Introduction

Storage plugins are responsible for delivering information about
entities that are not part of the Linux/Lustre stack.  This primarily means
storage controllers and network devices, but the plugin system is generic and 
does not limit the type of objects that can be reported.

To present device information to the manager server, a Python\* module is written using
the Storage Plugin API described in this document:

* The objects to be reported are described by declaring a series of
  Python classes (refer to [Resources](#1.2)
* Certain of these objects are used to store the contact information
  such as IP addresses for managed devices(refer to [Scannable Storage Resources](#scannable_storage_resources))
* A main plugin class is implemented to provide required hooks for
  initialization and teardown(refer to [Storage Plugins](#storage_plugins))

The API is designed to minimize the lines of code required to write a plugin, 
minimize the duplication of effort between different plugins, and make as much
of the plugin code as possible declarative in style to minimize the need for 
per-plugin testing.  For example, rather than having plugins procedurally
check for resources that are in bad states during an update, we provide the means to declare
conditions that are automatically checked.  Similarly, rather than requiring explicit 
notification from the plugin when a resource attribute is changed, we detect
assignments to attributes and schedule transmission of updates in the background.

Plugins can provide varying levels of functionality.  The most basic plugins can provide
only discovery of storage resources at the time the plugin is loaded (requiring a manual
restart to detect any changes).  Most plugins will provide at least the initial discovery
and live detection of added/removed resources of certain classes, for example LUNs
as they are created and destroyed.  On a per-resource-class basis, alert conditions
can be added to report issues with the resources such as pools being rebuilt or 
physical disks that fail.

In addition to reporting a set of resources, plugins report a set of relationships between
the resources, used for associating problems with one resource with another resource.  This 
takes the form of an "affects" relationship between resources, for example the health of 
a physical disk affects the health of its pool, and the health of a pool affects LUNs
in that pool.  These relationships allow the effects of issues to be traced all the 
way up to the Lustre file system level and an appropriate drill-down user interface to be provided.

The API may change over time.  To ensure plugins are able to run against a particular
version of the API, each plugin module must declare the version of the API it intends to use.
The manager server will check the version of each plugin when loading and write a message to
the log if there is a problem.  The manager server supports version |api_version| of the API.
The plugin needs to declare the version in the top level module file where the
plugins and resources are defined.  Note, that if you have Python errors that prevent the plugin module
from importing, the version is not checked.  The version is only validated on cleanly imported plugins.
See the example plugin below for details on how to specify the version in your plugins.


### <a name="1.1.1"></a>Terminology

- **plugin:** A Python module providing a number of classes inheriting from the Plugin and Resource classes.
- **resource class:** A subclass of Resource declaring a means of identification, attributes, statistics and alert conditions.
- **resource:** An instance of a particular resource class, with a unique identifier.

## <a name="1.2"></a>Declaring Resources
-------------------

A `Resource` represents a single, uniquely identified object.  It may be a physical
device such as a physical hard drive, or a virtual object such as a storage pool or 
virtual machine.

```python

   from chroma_core.lib.storage_plugin.api import resources, identifiers, attributes, statistics

   class HardDrive(resources.Resource):
       serial_number = attributes.String()
       capacity = attributes.Bytes()
       temperature = statistics.Gauge(units = 'C')

       class Meta:
           identifier = identifiers.GlobalId('serial_number')
```

In general, storage resources may inherit from Resource directly, but
optionally they may inherit from a built-in resource class as a way of 
identifying common resource types for presentation purposes.  See 
[Resource Classes](#storage_plugin_builtin_resource_classes) for the available built-in
resource types.

Attributes
----------

The ``serial_number`` and ``capacity`` attributes of the HardDrive class are
from the ``attributes`` module.  These are special classes which:

* Apply validation conditions to the attributes
* Act as metadata for the presentation of the attribute in the manager server user interface

Various attribute classes are available for use, see [Attribute Classes](#storage_plugin_attribute_classes).

Attributes may be optional or mandatory.  They are mandatory by default. To 
make an attribute optional, pass ``optional = True`` to the constructor.

Statistics
----------

The ``temperature`` attribute of the HardDrive class is an example of
a resource statistic. Resource statistics differ from resource
attributes in the way they are presented to the user.  See [Statistic Classes](#storage_plugin_statistic_classes)
for more on statistics.

Statistics are stored at runtime by assigning to the relevant
attribute of a storage resource instance.  For example, for a 
``HardDrive`` instance ``hd``, assigning ``hd.temperature = 20`` updates
the statistic.

Identifiers
-----------

Every Resource subclass is required to have an ``identifier`` attribute
that declares which attributes are to be used to uniquely identify the resource.

If a resource has a universally unique name and may be reported from more than one
place (for example, a physical disk which may be reported from more than one 
controller), use ``chroma_core.lib.storage_plugin.api.identifiers.GlobalId``.  For example, 
in the ``HardDrive`` class described above, each drive has a unique factory-assigned ID.

If a resource has an identifier that is scoped to a *scannable* storage resource or
a resource always belongs to a particular scannable storage resource, use
``chroma_core.lib.storage_plugin.api.identifiers.ScopedId``.

Either of the above classes is initialized with a list of attributes which
in combination are a unique identifier.  For example, if a true hard drive 
identifier is unavailable, a drive might be identified within a particular couplet 
by its shelf and slot number, like this:

```python
    class HardDrive(Resource):
        class Meta:
            identifier = identifiers.ScopedId('shelf', 'slot')
        shelf = attributes.ResourceReference()
        slot = attributes.Integer()
```

If a resource is created by users that doesn't have a natural unique
set of attributes, you can use ``identifiers.AutoId()`` to have
an internal ID assigned.  This is only valid for ScannableResource subclasses, and will
allow the user to create more than one identical resource. Therefore, use with care.

Relationships
-------------

The ``update_or_create`` function used to report resources (see [Storage Plugins](#storage_plugins)) 
takes a ``parents`` argument, which is a list of the resources that directly affect the 
status of this resource.  This relationship does not imply ownership, but rather "a problem 
with parent is a problem with child" relationship.  For example,
a chain of relationships might be *Fan->Enclosure->Physical disk->Pool->LUN*. The graph of these relationships must be acyclic.

Although plugins will run without any parent relationships, it is important
to populate them so that hardware issues can be associated with the relevant
Lustre target or file system.

Alert Conditions
----------------

Plugins can communicate error states by declaring *Alert conditions*,
which monitor the values of resource attributes and display alerts in the
manager server user interface when an error condition is encountered.

Alert conditions are specified for each resource in the Meta section, like this:

```python
    class HardDrive(Resource):
        class Meta:
            identifier = identifiers.ScopedId('shelf', 'slot')
            alert_conditions = [
                alert_conditions.ValueCondition('status', warn_states = ['FAILED'], message = "Drive failure")
               ] 
        shelf = attributes.ResourceReference()
        slot = attributes.Integer()
        status = attributes.String()
```

Several types of alert conditions are available. See [Alert Conditions](#storage_plugin_alert_conditions).

If a resource has more than one alert condition that refers to the same attribute, it is
necessary to add an `id` argument to allow each alert condition to be uniquely identified.  For example:

```python
    class HardDrive(Resource):
        class Meta:
            identifier = identifiers.ScopedId('shelf', 'slot')
            alert_conditions = [
                alert_conditions.ValueCondition('status', warn_states = ['NEARFAILURE'], message = "Drive near failure", id = 'nearfailure'),
                alert_conditions.ValueCondition('status', warn_states = ['FAILED'], message = "Drive failure", id = 'failure')
               ] 
        shelf = attributes.ResourceReference()
        slot = attributes.Integer()
        status = attributes.String()
```

You can tell if it is necessary to add an explicit ID by looking for an error in the
output of the validation process ([validation](#validation)) -- if a plugin passes validation without `id`
arguments to alert conditions, it is recommended that `id` be omitted.

<a name="scannable_storage_resources"></a>Declaring a ScannableResource
-----------------------------------------------------------------------

Certain storage resources are considered 'scannable':

* They can be added by the administrator using the manager server user interface
* Plugins contact this resource to learn about other resources
* This resource 'owns' some other resources

A typical scannable resource is a storage controller or couplet of
storage controllers.

```python
   from chroma_core.lib.storage_plugin.api import attributes, identifiers, resources

   class StorageController(resources.ScannableResource):
       address_1 = attributes.Hostname()
       address_2 = attributes.Hostname()

       class Meta:
           identifier = identifiers.GlobalId('address_1', 'address_2')
```

<a name="storage_plugins"></a>Implementing a Plugin
---------------------

The Resource classes are simply declarations of what resources can be 
reported by the plugin and what properties they will have.  The plugin module
must also contain a subclass of *Plugin* which implements at least the
``initial_scan`` function:

*Plugin.initial_scan*
```
Plugin.initial_scan(root_resource)
```
   
> Required
>  
> Identify all resources present at this time and call register_resource on them.
>
> If you return from this function you must have succeeded in communicating with the scannable resource. Any resources which were present previously and are absent when initial_scan returns are assumed to be permanently absent and are deleted. If for any reason you cannot return all resources (for example, communication failure with a controller), you must raise an exception.
>
> **Parameters:**	**root_resource** – All resources of the plugin for each host are children of 
> this resource. 
>   
> **Returns:**	No return value


Within ``initial_scan``, plugins use the ``update_or_create`` function to 
report resources.

*Plugin.update_or_create*
```
Plugin.update_or_create(klass, parents=[], **attrs)
```
> Report a storage resource. If it already exists then it will be updated, otherwise it will be 
> created. The resulting resource instance is returned.
>
> The ‘created’ return value indicates whether this is the first report of the resource within 
> this plugin session, not whether it is the first report of the resource ever (e.g. from a 
> different or previous plugin session).
>
> The identifier of the resource is used as the key to check for an existing object.
>    
> <b>Parameters:</b> 
>       
> * <b>klass</b> – The resource class of the object being created.
> * <b>parents</b> – The parent resources of the resource being created.
> * <b>attrs</b> – The attributes of the resource being updated or fetched.
>
> <b>Returns:</b> (resource, created) – the storage resource and a boolean indicating whether 
> this was the first report this session.


If any resources are allocated in ``initial_scan``, such as threads or 
sockets, they may be freed in the ``teardown`` function:


*Plugin.teardown*
```
Plugin.teardown()
```
> Optional
>
> Perform any teardown required before terminating.
>
> Guaranteed not to be called concurrently with initial_scan or update_scan. Guaranteed that 
> initial_scan or update_scan will not be called after this. Guaranteed that once initial_scan 
> has been entered this function will later be called unless the whole process terminates 
> prematurely.
>
> This function will be called even if initial_scan or update_scan raises an exception.


After initialization, the ``update_scan`` function will be called periodically.
You can set the delay between ``update_scan`` calls by assigning to
``self.update_period`` before leaving in ``initial_scan``.  Assignments to
``update_period`` after ``initial_scan`` will have no effect.

*Plugin.update_scan*
```
Plugin.update_scan(root_resource)
```
> Optional
>
> Perform any required periodic refresh of data and update any resource instances. It is 
> guaranteed that initial_scan will have been called before this.
>
> <b>Parameters:</b>	<b>root_resource</b> – All resources of the plugin for each host are 
> children of this resource.
>
> <b>Returns:</b>	No return value

If a resource has changed, you can either use ``update_or_create`` to modify 
attributes or parent relationships, or you can directly assign to the resource's 
attributes or use its add_parent and remove_parent functions.  If a resource has 
gone away, use ``remove`` to remove it:

*Plugin.remove*
```
Plugin.remove(resource)
```
> Remove the resource passed from the resource list. The operation is not immediate with the 
> resource being marked for deletion and actually deleted at the next periodic cycle.
>
> <b>Parameters:</b>	<b>resource</b> – The resource to be removed


Although resources must be reported synchronously during ``initial_scan``, this
is not the case for updates.  For example, if a storage device provides asynchronous
updates via a network protocol, the plugin author may spawn a thread in ``initial_scan``
that listens for these updates.  The thread listening for updates may modify resources
and make ``update_or_create`` and ``remove`` calls on the plugin object.
Plugins written in this way would probably not implement ``update_scan`` at all.

Logging
-------

Plugins should refrain from using ``print`` or any custom logging, in favor of
using the ``log`` attribute of the Plugin instances, which is a standard Python
``logging.Logger`` object provided to each plugin.

The following shows the wrong and right ways to emit log messages:

```python
    # BAD: do not use print
    print "log message"

    # BAD: do not create custom loggers
    logging.getLogger('my_logger').info("log message")

    # Good: use the provided logger
    self.log.info("log message")
```

Presentation Metadata
---------------------

Names
-----

Sensible defaults are used wherever possible when presenting UI elements
relating to storage resources.  For example, by default, attribute names are
transformed to capitalized text. For example,``file_size`` is transformed to *File size*.  When a different
name is desired, the plugin author can provide a ``label`` argument to attribute 
constructors:

```python
   my_internal_name = attributes.String(label = 'Fancy name')
```

Resource classes are by default referred to by their Python class name, qualified
with the plugin module name.  For example, if the ``acme`` plugin had a class called
``HardDrive``, it would be called ``acme.HardDrive``.  This can be overridden by setting
the ``label`` attribute on the Meta attribute of a Resource class.

Instances of resources have a default human readable version of their class name followed by
their identifier attributes.  This can be overridden by implementing the ``get_label``
function on the storage resource class, returning a string or unicode string for the instance.

Charts
------

By default, the manager server web interface presents a separate chart for each statistic
of a resource.  However, it is often desirable to group statistics on the same
chart, such as a read/write bandwidth graph.  This may be done by setting the ``charts``
attribute on a resource class to a list of dictionaries, where each dictionary
has a ``title`` element with a string value and a ``series`` element whose value
is a list of statistic names to plot together.

When two or more series are plotted together, they must be of the same type (time series or histogram).  They do
not have to be in the same units, but only up to two different units may be 
used on the same chart (one Y axis on either side of the chart).

For example, the following resource has a ``charts`` attribute which presents
the read and write bandwidth on the same chart:

```python
class MyResource(Resource):
    read_bytes_per_sec = statistics.Gauge(units = 'bytes/s')
    write_bytes_per_sec = statistics.Gauge(units = 'bytes/s')

    class Meta:
        charts = [
            {
                'title': "Bandwidth",
                'series': ['read_bytes_per_sec', 'write_bytes_per_sec']
            }
        ]
```

Running a Plugin
----------------

<a name="validation"></a>Validating
-----------------------------------

Before running your plugin as part of a manager server instance, it is a good idea to check it over
using the `validate_storage_plugin` command:

```bash
    $ cd /usr/share/chroma-manager
    $ ./manage.py validate_storage_plugin /tmp/my_plugin.py
    Validating plugin 'my_plugin'...
    OK
```

Installing
----------

Plugins are loaded according to the ``settings.INSTALLED_STORAGE_PLUGINS`` variable.  This variable
is a list of module names within the Python import path.  If your plugin is located
at ``/home/developer/project/my_plugin.py``, create a ``local_settings.py`` file
in the ``chroma-manager`` directory (``/usr/share/chroma-manager`` when installed
from RPM) with the following content:

```python
    sys.path.append("/home/developer/project/")
    INSTALLED_STORAGE_PLUGINS.append('my_plugin')
```

After modifying this setting, restart the manager server services.

Errors from the storage plugin subsystem, including any errors output
from your plugin can be found in `/var/log/chroma/storage_plugin.log`. To
increase the verbosity of the log output (by default only WARN and above
is output), add your plugin to ``settings.STORAGE_PLUGIN_DEBUG_PLUGINS``.
Changes to these settings take effect when the manager server services are
restarted.

Running the Plugin Process Separately
-------------------------------------

During development, the process that hosts storage plugins can be run separately,
so that it can be stopped and started quickly by plugin developers:

```bash
    cd /usr/share/chroma-manager
    supervisorctl -c production_supervisord.conf stop plugin_runner
    ./manage.py chroma_service --verbose plugin_runner
```

Correlating Controller Resources with Linux Devices Using Relations
-------------------------------------------------------------------

As well as explicit *parents* relations between resources, resource attributes can be 
declared to *provide* a particular entity.  This is used for linking up resources between
different plugins, or between storage controllers and Linux hosts.

To match up two resources based on their attributes, use the `Meta.relations` attribute,
which must be a list of `relations.Provide` and `relations.Subscribe` objects.  In the following
example, a plugin matches its LUNs to detected SCSI devices of the built in class `linux.ScsiDevice`,
which stores the device's WWID as the `serial` attribute.


```python
class MyLunClass(Resource):
    serial = attributes.String()

    class Meta:
        identifier = identifiers.GlobalId('my_serial')
        relations = [relations.Provide(
            provide_to = ('linux', 'ScsiDevice'),
            attributes = 'serial')]
```

The `provide_to` argument to `Provide` can either be a resource class, or a 2-tuple of `([plugin name], [class name])`
for referring to resources in another plugin.  In this case, we are referring to a resource in the 'linux' plugin, which
is what the manager server uses for detecting standard devices and device nodes on Linux servers.  Note that these
relations are case sensitive.

Example Plugin
--------------

```python
from chroma_core.lib.storage_plugin.api import attributes, identifiers, plugin, relations, resources, statistics

version = 1


class Couplet(resources.ScannableResource):
    class Meta:
        identifier = identifiers.GlobalId('address_1', 'address_2')

    address_1 = attributes.Hostname()
    address_2 = attributes.Hostname()


class Controller(resources.Controller):
    class Meta:
        identifier = identifiers.ScopedId('index')

    index = attributes.Enum(0, 1)


class HardDrive(resources.PhysicalDisk):
    class Meta:
        identifier = identifiers.ScopedId('serial_number')

    serial_number = attributes.String()
    capacity = attributes.Bytes()
    temperature = statistics.Gauge(units = 'C')


class RaidPool(resources.StoragePool):
    class Meta:
        identifier = identifiers.ScopedId('local_id')

    local_id = attributes.Integer()
    raid_type = attributes.Enum('raid0', 'raid1', 'raid5', 'raid6')
    capacity = attributes.Bytes()

    def get_label(self):
        return self.local_id


class Lun(resources.LogicalDrive):
    class Meta:
        identifier = identifiers.ScopedId('local_id')
        relations = [
            relations.Provide(provide_to=('linux', 'ScsiDevice'), attributes=['serial'], ignorecase=True),
        ]

    local_id = attributes.Integer()
    name = attributes.String()

    serial = attributes.String()

    def get_label(self):
        return self.name


class ExamplePlugin(plugin.Plugin):
    def initial_scan(self, scannable_resource):
        # This is where the plugin should detect all the resources
        # belonging to scannable_resource, or throw an exception
        # if that cannot be done.
        pass

    def update_scan(self, scannable_resource):
        # Update any changed or added/removed resources
        # Update any statistics
        pass

    def teardown(self):
        # Free any resources
        pass
```

Resource Attributes
-------------------

<a name="common_options"></a>**Common Options**

*BaseResourceAttribute.__init__*
```
BaseResourceAttribute.__init__(optional=False, label=None, hidden=False, 
    user_read_only=False, default=None)
``` 
> **Parameters:**
> * **optional** – If this is True, the attribute may be left unassigned (i.e. null). 
> Otherwise, a non-null value must be provided for all instances.
> **label** – Human readable string for use in the user interface. Use this if the 
> programmatic attribute name in the resource declaration is not 
> appropriate for presentation to the user.
> * **hidden** – If this is True, this attribute will not be included as a column in 
> the tabular view of storage resources.
> * **user_read_only** – If this is True, this attribute can only be set internally 
> by the plugin, not by the user. For example, a controller might have some 
> attributes entered by the user, and some read from the hardware: those 
> read from the hardware would be marked user_read_only. Attributes which 
> are user_read_only must also be optional.
> * **default** – If not None then this default value will be used in the case of a 
> non-optional value missing. Generally used in the case of upgrades to 
> supply previous records. default maybe callable or a fixed value.


<a id="storage_plugin_attribute_classes"></a>**Available Attribute Classes**

The following classes allow plugin authors to specify type and bound information for the attributes of their resources. 
Plugin authors are encouraged to be as specific as possible in their choice of attribute class, and avoid using generic 
types like String as much as possible.

*Boolean*
```
class chroma_core.lib.storage_plugin.api.attributes.Boolean(optional=False, label=None, 
    hidden=False, user_read_only=False, default=None)
```
> A True/False value. Any truthy value may be assigned to this, but it will be stored as True or False.

*Bytes*
```
class chroma_core.lib.storage_plugin.api.attributes.Bytes(min_val=None, max_val=None, *args, 
    **kwargs)
```
> An exact size in bytes. This will be formatted with appropriate units and rounding when presented to the user, and should be used in preference to storing values in kilobytes/megabytes, etc., wherever possible.

*Enum*
```
class chroma_core.lib.storage_plugin.api.attributes.Enum(*args, **kwargs)
```
> An enumerated type. Arguments to the constructor are the possible values, for example
>
>```python
> status = Enum('good', 'bad', 'ugly')
> ...
> status = 'good'  # valid
> status = 'other' # invalid
> ```
>
> Assigning any value not in those options will fail validation. When presented to the user, this will appear as a dropdown box of available options.

*Hostname*
```
class chroma_core.lib.storage_plugin.api.attributes.Hostname(optional=False, label=None, 
    hidden=False, user_read_only=False, default=None)
```
> A DNS hostname or an IP address, e.g. mycompany.com, 192.168.0.67

*Integer*
```
class chroma_core.lib.storage_plugin.api.attributes.Integer(min_val=None, max_val=None, 
    *args, **kwargs)
```
> An integer. This may optionally be bounded by setting the inclusive min_val and/or max_val keyword arguments to the constructor.

*Password*
```
class chroma_core.lib.storage_plugin.api.attributes.Password(encrypt_fn, *args, **kwargs)
```
> A password. Plugins must provide their own obfuscation function. The encryption function will be called by the manager server when processing user input (e.g. when a resource is added in the UI). The obfuscated text will be seen by the plugin when the resource is retrieved.
>
> ```python
> def encrypt_fn(password):
>    return rot13(password)
>
> Password(encrypt_fn)
> ```

*PosixPath*
```
class chroma_core.lib.storage_plugin.api.attributes.PosixPath(optional=False, label=None, 
    hidden=False, user_read_only=False, default=None)
```
> A POSIX filesystem path, e.g. /tmp/myfile.txt

*String*
```
class chroma_core.lib.storage_plugin.api.attributes.String(max_length=None, *args, **kwargs)
```
> A unicode string. A maximum length may optionally be specified in the constructor using the max_length keyword argument

*Uuid*
```
class chroma_core.lib.storage_plugin.api.attributes.Uuid(optional=False, label=None, hidden=False, 
    user_read_only=False, default=None)
```
> A UUID string. Arguments may have any style of hyphenation. For example:
>
> ```python
> wwn = Uuid()
> ...
> resource.wwn = "b44f7d8e-a40d-4b96-b241-2ab462b4c1c1"  # valid
> resource.wwn = "b44f7d8ea40d4b96b2412ab462b4c1c1"  # valid
> resource.wwn = "other"  # invalid
> ```

*ResourceReference*
```
class chroma_core.lib.storage_plugin.api.attributes.ResourceReference(optional=False, label=None, 
    hidden=False, user_read_only=False, default=None)
```
> A reference to another resource. Conceptually similar to a foreign key in a database. Assign instantiated 
BaseStorageResource objects to this attribute. When a storage resource is deleted, any other resources having a 
reference to it are affected:
* If the ResourceReference has optional = True then the field is cleared
* Otherwise, the referencing resource is also deleted

**Note:** Creating circular reference relationships using this attribute has undefined (most likely fatal) behaviour.


<a name="storage_plugin_statistic_classes"></a>**Statistic Classes**

*BytesHistogram*
```
class chroma_core.lib.storage_plugin.api.statistics.BytesHistogram(*args, **kwargs)
```
> A fixed-length array of integers used for representing histogram data. The number of bins and the value 
> range of each bin are specified in the bins constructor argument:
>
> ```python
> BytesHistogram(bins = [(0, 512), (513, 1024), (1025, 4096), (4097,)])
> ```
>
> **Parameters**:	
> * **bins** – a list of tuples, either length 2 for a bounded range or length 1 to represent “this value or higher”.

*Counter*
```
class chroma_core.lib.storage_plugin.api.statistics.Counter(sample_period=10, units=None, 
    label=None)
```
> A monotonically increasing time series.

*Gauge*
```
class chroma_core.lib.storage_plugin.api.statistics.Gauge(sample_period=10, units=None, label=None)
```
> A numerical time series which can go up or down

<a name="storage_plugin_builtin_resource_classes"></a>**Built-in Resource Classes**

Plugin authors are encouraged to inherit from these classes when there is a clear analogy between an object in their plugin and one of those provided here.

*Controller*
```
class chroma_core.lib.storage_plugin.api.resources.Controller(**kwargs)
```
> A RAID controller

*Enclosure*
```
class chroma_core.lib.storage_plugin.api.resources.Enclosure(**kwargs)
```
> A physical enclosure/drawer/shelf

*Fan*
```
class chroma_core.lib.storage_plugin.api.resources.Fan(**kwargs)
```
> A physical cooling fan

*LogicalDrive*
```
class chroma_core.lib.storage_plugin.api.resources.LogicalDrive(**kwargs)
```
> A storage device with a fixed size that could be used for installing the Lustre software
> * *classmethod* **device_type()**
>
> By default devices are linux block devices
>
> * **usable_for_lustre** = *True*
   
This has to be a class method today because at the point we call it we only have the type not the object

*LogicalDriveOccupier*
```
class chroma_core.lib.storage_plugin.api.resources.LogicalDriveOccupier(**kwargs)
```
> When a subclass of this class is the descendent of a LogicalDrive, that LogicalDrive is considered 
unavailable. This is used for marking LUNs/partitions/LVs which are in use, for example those which 
are mounted in existing file systems.

*LogicalDriveSlice*
```
class chroma_core.lib.storage_plugin.api.resources.LogicalDriveSlice(**kwargs)
```
> A part of a slicable device like partition or lvm

*PhysicalDisk*
```
class chroma_core.lib.storage_plugin.api.resources.PhysicalDisk(**kwargs)
```
> A physical storage device, such as a hard drive or SSD

*StoragePool*
```
class chroma_core.lib.storage_plugin.api.resources.StoragePool(**kwargs)
```
> An aggregation of physical drives

*VirtualMachine*
```
class chroma_core.lib.storage_plugin.api.resources.VirtualMachine(**kwargs)
```
> A Linux* host provided by a plugin. This resource has a special behaviour when created: the 
manager server will add this (by the address attribute) as a Lustre server and attempt to 
configure the chroma-agent service on it. The host_id attribute is used internally by the 
manager server and must not be assigned to by plugins.

<a name="storage_plugin_alert_conditions"></a>**Alert Conditions**

*LowerBoundCondition*
```
class chroma_core.lib.storage_plugin.api.alert_conditions.LowerBoundCondition(attribute, 
    error_bound=None, warn_bound=None, info_bound=None, message=None, *args, **kwargs)
```
> A condition that checks a numeric attribute against a lower bound, and raises the alert if it falls 
below that bound
>
> ```python
> LowerBoundCondition('rate', error_bound = 10, message = "Rate too low")
> ```

*UpperBoundCondition*
```
class chroma_core.lib.storage_plugin.api.alert_conditions.UpperBoundCondition(attribute, 
    error_bound=None, warn_bound=None, info_bound=None, message=None, *args, **kwargs)
```
> A condition that checks a numeric attribute against an upper bound, and raises the alert if 
> it exceeds that bound
> 
> ```
> UpperBoundCondition('temperature', error_bound = 85, message = "Maximum operating 
>      temperature exceeded")
> ```

*ValueCondition*
```
class chroma_core.lib.storage_plugin.api.alert_conditions.ValueCondition(attribute, error_states=[], 
    warn_states=[], info_states=[], message=None, *args, **kwargs)
```
> A condition that checks an attribute against certain values indicating varying severities of alert. 
> For example, if you had a ‘status’ attribute on your ‘widget’ resource class which could be ‘OK’ or 
> ‘FAILED’ then you might create an AttrValAlertCondition like this:
> 
> ```
> AttrValAlertCondition('status', error_states = ['FAILED'], message = "Widget failed")
> ```



Advanced: Using Custom Block Device Identifiers
-----------------------------------------------

A best effort is made to extract standard SCSI identifiers from block devices that
are encountered on Lustre servers.  However, in some cases:

* The SCSI identifier may be missing
* The storage controller may not provide the SCSI identifier

Storage plugins may provide additional code to run on Lustre servers that extracts additional
information from block devices.

Agent Plugins
-------------

Plugin code running within the chroma-agent service has a simple interface:

*DevicePlugin*
```
class chroma_agent.plugin_manager.DevicePlugin(session)
```
> A plugin which maintains a state and sends and receives messages.
>
> * **start_session()**
>
>    Return information needed to start a manager-agent session, i.e. a full listing of all available information.
>
>    <b>Return type:</b>	   JSON-serializable object, DevicePluginMessage, or DevicePluginMessageCollection
>
> * **update_session()**
>   
>    Return information needed to maintain a manager-agent session, i.e. what has changed since the start of the session or since the last update.
>
>    If you need to refer to any data from the start_session call, you can store it as an attribute on this DevicePlugin instance.
>
>    This will never be called concurrently with respect to start_session, or before start_session.
>
>    <b>Return type:</b>	   JSON-serializable object, DevicePluginMessage, or DevicePluginMessageCollection

Implementing `update_session` is optional. Plugins that do not implement this function will only send
information to the server once when the agent begins its connection to the server.

The agent guarantees that the instance of your plugin class is persistent within the process
between the initial call to start_session and subsequent calls to update_session, and that
start_session will only ever be called once for a particular instance of your class.  This allows
you to store information in start_session that is used for calculating deltas of the system
information to send in update_session.

To install an agent plugin like this, copy the .py file containing a DevicePlugin subclass into
`/usr/lib/python2.[46]/site-packages/chroma_agent-*.egg/chroma_agent/device_plugins/` on the
servers with chroma-agent installed, and restart the chroma-agent service.  Test the output
of your plugin with `chroma-agent device-plugin --plugin=my_controller` (if for example
your plugin file was called my_controller.py).

The name of the agent plugin module must exactly match the name of the plugin module running
on the manager server server.

Handling Data from Agent Plugins
--------------------------------

The information sent by an agent plugin is passed on to the server plugin with the same name.  To handle
this type of information, the plugin must implement two methods:

*Plugin*
```
class chroma_core.lib.storage_plugin.api.plugin.Plugin(resource_manager, scannable_id=None)
```
> * **agent_session_start**(host_id, data)
>   
>    Optional
>
>    Start a session based on information sent from an agent plugin.
>
>    <b>Parameters:</b>
>    * <b>host_id</b> – ID of the host from which the agent information was sent – this is a database identifier which is mainly useful for constructing DeviceNode resources.
>    * <b>data</b> – Arbitrary JSON-serializable data sent by plugin.
>    :return No return value
>
> * **agent_session_continue**(host_id, data)
>    Optional
>
>    Continue a session using information sent from an agent plugin.
>
>    This will only ever be called on Plugin instances where agent_session_start has already been called.
>
>    <b>Parameters:</b>
>    * <b>host_id</b> – ID of the host from which the agent information was sent – this is a database identifier which is mainly useful for constructing DeviceNode resources.
>    * <b>data</b> – Arbitrary JSON-serializable data sent by plugin.
>    :return No return value

Advanced: Reporting Hosts
-------------------------

Your storage hardware may be able to provide server addresses, for example
if the storage hardware hosts virtual machines that act as Lustre servers.

To report these hosts from a storage plugin, create resources of a class with
subclasses `resources.VirtualMachine`.

```python
    class MyController(resources.ScannableResource):
        class Meta:
            identifier = identifiers.GlobalId('address')
        address = attributes.Hostname()

    class MyVirtualMachine(resources.VirtualMachine):
        class Meta:
            identifier = identifiers.GlobalId('vm_id', 'controller')

        controller = attributes.ResourceReference()
        vm_id = attributes.Integer()
        # NB the 'address' attribute is inherited

    class MyPlugin(plugin.Plugin):
        def initial_scan(self, controller):
            # ... somehow learn about a virtual machine hosted on `controller` ...
            self.update_or_create(MyVirtualMachine, vm_id = 0, controller = controller, address = "192.168.1.11")
```

When a new VirtualMachine resource is created by a plugin, the configuration
process is the same as if the host had been added via the manager server user interface, and the added host 
will appear in the list of servers in the user interface.

Advanced: Specifying Homing Information
---------------------------------------

A given device node (i.e. presentation of a LUN) may be a more or less preferable means
of access to a storage device.  For example:

* If a single LUN is presented on two controller ports, a device node on a host connected to one port 
  may be preferable to a device node on a host connected to the other port.
* If a LUN is accessible via two device nodes on a single server, one may be preferable to the other.

This type of information allows the manager server to make an intelligent selection of primary/secondary Lustre servers.

To express this information, create a PathWeight resource that is a parent of the device node and has as its
parent the LUN.

Legal Information
-----------------

Copyright (c) 2017 Intel® Corporation. All rights reserved.
 Use of this source code is governed by a MIT-style
 license that can be found in the LICENSE file.

\* Other names and brands may be claimed as the property of others.
This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)

[Top of page](#1.0)