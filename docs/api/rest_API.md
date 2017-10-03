# <a name="1.0"></a>REST API for Intel® Manager for Lustre* software software

[**Software API Documentation Table of Contents**](./api_TOC.md)

## <a name="1.1"></a>Introduction
The manager server web interface and command line interface (CLI) included with the 
Intel® Manager for Lustre* software are built on the REST API, which is accessed
via HTTP.  This API is available for integration with third party applications.  The 
types of operations possible using the API include creating a file system, checking
the system for alert conditions, and downloading performance metrics.  All functionality
provided in the manager server web interface is based on this API, so anything 
that can be done using the web interface can also potentially be done from third party 
applications.

The API is based on the [REST](http://en.wikipedia.org/wiki/Representational_state_transfer)
style, and uses [JSON](http://en.wikipedia.org/wiki/JSON) serialization.  Some of the
resources exposed in the API correspond to functionality within the Lustre* file system, while
others refer to functionality specific to the Intel® Manager for Lustre* software.

This document consists of a series of sections explaining how to use the API, followed
by an [Example client](#1.7), and a detailed [API Reference](#1.8) describing all
available functionality.

### <a name="1.1.1"></a>Prerequisites

- Familiarity with managing Lustre* using the manager server web interface provided with the Intel® Manager for Lustre* software.
- Familiarity with HTTP, including the meanings and conventions around the methods (e.g. GET, POST, DELETE) and status codes (e.g. 404, 200).
- Competence in using a suitable high level programming language to write your API client and the libraries used with your language for HTTP network operations and JSON serialization.

## <a name="1.2"></a>Overview of Lustre* File Systems in the API


### <a name="1.2.1"></a>Terminology


The terminology used in this document differs somewhat from that used when administering a Lustre* file system manually. This document avoids referring to a host as an object storage server (OSS), metdata server (MDS), or management server (MGS) because, in a Lustre* file system created using the Intel® Manager for Lustre* software, a host can serve targets of any of these types.
 
Lustre-specific terms used in this API include:

|Term|Description|
|---|---|
|OST|a block device formatted as an object store target|
|MDT|a block device formatted as a metadata target|
|MGT|a block device formatted as a management target|
|File system|a collection of MGT, MDTs and OSTs|

### <a name="1.2.2"></a>Objects and Relationships


The following objects are required for a running file system:
MGT, MDT, OST (target), filesystem, volume, volume node, host.

The order of construction permitted for consumers of the REST API is:

1. Hosts
2. Volumes and volume nodes (these are detected from hosts)
3. MGTs (these may also be created during file system creation)
4. File system (includes creating an MDT and one or more OSTs)
5. Any additional OSTs (added to an existing file system)

The following cardinality rules are observed:

- An MGT has zero or more file systems, each file system belongs to one MGT.
- A file system has one or more MDTs, each MDT belongs to one file system. *(exception: a file system that is in the process of being deleted passes
  through a stage where it has zero MDTs)*
- A file system has one or most OSTs, each OST belongs to one file system.
  *(exception: a file system that is in the process of being deleted passes
  through a stage where it has zero OSTs)*
- MDTs, MGTs and OSTs are targets.  Targets are associated with one
  primary volume node, and zero or more secondary volume nodes.  Targets
  are associated with exactly one volume, and each volume is associated with
  zero or one targets.
- Volume nodes are associated with zero or one targets, exactly one volume, and exactly one host.


## <a name="1.3"></a>Fetching Objects


Access to objects such as servers, targets and file systems is provided using meaningful URLs. For example, to access a file system with ID 1, use 
``/api/filesystem/1/``. 
To read file system attributes, use an HTTP GET operation, while to modify the attributes, send back a modified copy of the object using an HTTP PUT operation to the same URL.  The PUT verb tells the server that you want to modify something, the URL tells the server which object you want to modify, and the payload contains the updated fields.  

Operations using a URL for a specific object are referred to in this document as _detail_ operations.
These operations usually return a single serialized object in the response.

To see all the file systems, omit the /1/ in the URL and do a 
```GET /api/filesystem/```.
This type of operation is referred to in this document as a _list_ operation. 

### <a name="1.3.1"></a>Use of HTTPS


By default, the manager server uses a server certificate signed by its built-in CA.  To verify this certificate in an API client, you must download the manager server CA. The CA is available for download from the manager server at the ``/certificate/`` path.

### <a name="1.3.2"></a>Filtering and Ordering


To filter on an attribute value, pass the attribute and value as an argument to a GET request.  For example, to get targets belonging to a file system with ID 1, use ``GET /api/target/?filesystem_id=1``.

Ordering of results is done using the ``order_by`` URL parameter set to the name
of the attribute by which the results are to be ordered, prefixed with ``-`` to reverse the order.  For example, to get all targets in reverse name order, use the URL ``/api/target/?order_by=-name``.

More advanced filtering is also possible (Note: The manager server uses the Django``*`` framework
to access its database, so [django style' queries](https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups) are used).  They use double-underscore
suffixes to field names to indicate the type of filtering. Some commonly used filters
are shown in the following list:

|Filter|Description|
|---|---|
|\__in:|Has one of the values in a list|
|\__lt:|Less than|
|\__gt:|Greater than|
|\__lte|Less than or equal to|
|\__gte:|Greater than or equal to|
|\__contains|Contains the string (case sensitive)|
|\__icontains:|Contains the string (case insensitive)|
|\__startswith:|Starts with the string|
|\__endswith:|Ends with the string|

For example, an object that supports ``id__in`` filtering allows an "If its ID is in this list" query.  Note that 
to pass lists as URL parameters, the argument must be repeated. So, to get a list of targets 1 and 2, the
URL is ``/api/target/?id__in=1&id__in=2``.  

See the [API Reference](#1.8) for details about which attributes are permitted for ordering and filtering on a resource-by-resource basis.


### <a name="1.3.3"></a>Encoding


The API will respect the ``Accept`` header in a request.  Set the Accept header to ``application/json``
to receive JSON responses.

JSON does not define an encoding for dates and times. The API uses the [ISO8601](http://www.w3.org/TR/NOTE-datetime) format 
for dates and times, with the caveat that the timezone must be specified in values or behaviour is undefined.

You may find it useful to browse the API using a web browser.  To do this on a running
system, first log into the manager server web interface, and then point your browser at
``http://my-command-center/api/host/?format=json``.  The resulting output is best browsed using a plugin like ``JSONView`` for the Google``*`` Chrome``*`` browser.  Note that using ``format=json`` is only necessary when using a browser: your own client will set the ``Accept`` header instead.

### <a name="1.3.4"></a>Detail Responses

Detail GET requests (e.g. ``GET /api/host/1/``) return a dict representing a single object.

Most serialized objects have at least ``resource_uri`` and ``id`` fields.  Where an object has a human readable name that is useful for presentation, it is in an attribute called ``label``.

Note that in some cases it may be necessary to manually compose the URL for an object
based on its type and integer ID. Usually when an object is provided by the server, it
is accompanied by a ``resource_uri`` attribute which should be used for subsequent
access to the object instead of building the URL on the client.


### <a name="1.3.5"></a>List Responses


All list methods (e.g. ``GET /api/host``) return a dict with 'meta' and 'objects' keys.  The 'meta' key contains information about the set of objects returned, which is useful for pagination.

If you wish to obtain all objects, pass ``limit=0`` as a parameter to the request.

```json
    {
        "meta": {
            "limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2
        },
        "objects": [{...}, {...}]
    }
```

Where:

|Parameter|Description|
|---|---|
|``limit``:|the maximum number of records returned in each response (you may pass this as a parameter to your request, or pass 0 to fetch an unlimited number)|
|``offset``:|offset of this page into the overall result (you may pass this as a parameter to your request)|
|``total_count``:|the total number of records matching your request, before pagination|
|``next``:|a URL to the next page of results|
|``previous``:|a URL to the previous page of results


## <a name="1.4"></a>Creating, Modifying, and Deleting Objects


Objects are created using the POST method.  The attributes provided at creation
time are sent as a JSON-encoded dict in the body of the POST (*not* as URL
parameters).  If an object is successfully created, its identifier will
be included in the response.

Some resources support using the PUT method to modify attributes.  In some cases, executing a PUT may result in a literal, immediate modification of an attribute (such as altering
a human readable name), while in other cases, it will start an asynchronous
operation (such as changing the ``state`` attribute of a target from ``mounted``
to ``unmounted``).  Most attributes are read only. Where it is possible to use
PUT to modify a resource, this is stated in the resource's documentation (see
[API Reference](#1.8))

On resources that support the DELETE method, this method may be used to remove resources
from the storage server.  Some objects can always be removed immediately, while
others take some time to remove and the operation may not succeed.  For example,
removing a file system requires removing the configuration of its targets from
the Lustre* servers: if a DELETE is sent for such an object then the operation
will be run asynchronously (see [Asynchronous Actions](#1.4.1))

### <a name="1.4.1"></a>Asynchronous Actions


When an action will occur in the background, the ACCEPTED (202) status code is
returned, with a dictionary containing a command object, e.g.:

```json
    {
        "command": {
            "id": 22,
            "resource_uri": 22,
            "message": "Starting filesystem testfs"
        }
    }
```

In some cases, the response may include additional fields describing work
that was completed synchronously. For example, POSTing to ``/api/filesystem/``
returns the ``command`` for setting up a file system, and also the newly
created ``filesystem``.

You can poll the ``/api/command/<command-id>/`` resource to check the 
status of your asynchronous operation.  You may start multiple operations
and allow them to run in parallel.

### <a name="1.4.2"></a>State Changes


Some objects with a ``state`` attribute allow PUTs to modify the attribute and return a
command for the resulting action.  To determine valid values for the state, examine
the ``available_transitions`` attribute of the object. This is a list of objects,
each with a ``state`` attribute and a ``verb`` attribute.  The ``verb`` attribute
is a hint for presentation to the user, while the ``state`` attribute is what should
be written back to the original object's ``state`` field in a PUT to cause its
state to change.

For example, consider this host object:

```json
    {
        "address": "flint02",
        "available_transitions": [
            {
                "state": "removed",
                "verb": "Remove"
            },
            {
                "state": "lnet_unloaded",
                "verb": "Unload LNet"
            },
            {
                "state": "lnet_down",
                "verb": "Stop LNet"
            }
        ],
        "content_type_id": 6,
        "fqdn": "flint02",
        "id": "10",
        "label": "flint02",
        "nodename": "flint02",
        "resource_uri": "/api/host/10/",
        "state": "lnet_up"
    }
```

The host is in state ``lnet_up``.  To stop LNet, the host state can be transitioned to the appropriate available 
transition 'lnet_down'/'Stop LNet' by executing a PUT ``{"state": "lnet_down"}`` to ``/api/host/10/``.

Assuming the transition sent is a valid one, this PUT will result in a response with status code 202,
and a ``command`` will be included in the response (see [Asynchronous actions](#1.4.1))

## <a name="1.5"></a>Access Control


If your application requires write access (methods other than GET) to the API, or if the server
is configured to prevent anonymous users from reading, then your application must
authenticate itself to the server.

User accounts and credentials can be created and managed using the manager server web
interface -- we assume here that a suitable account has already been created.  Create
an account for your application with the lowest possible privilege level.

For a complete example of how to authenticate with the API, see the [Example client](#1.7).

### <a name="1.5.1"></a>Sessions


Establishing a session only applies when authenticating by username and password.

Before authenticating you must establish a session.  Do this by sending
a GET to ``/api/session/``, and including the returned ``sessionid`` cookie
in subsequent responses.

### <a name="1.5.2"></a>CSRF


Cross Site Request Forgery (CSRF) protection only applies when authenticating by username and password.

Because the API is accessed directly from a web browser, it requires CSRF
protection.  When authenticating by username+password,
the client must accept and maintain the ``csrftoken`` cookie that is returned
from the  ``/api/session/`` resource used to establish the session and 
set the X-CSRFToken request header in each request to the value of that cookie.

Note that an absent or incorrect CSRF token only causes an error on POST requests.


### <a name="1.5.3"></a>Authentication


***By username and password***

Once a session is established, you may authenticate by POSTing to ``/api/session``
  (see [session](#1.5.1)).

***By key***

Currently, consumers of the API must log in using the same username/password credentials
  used in the web interface.  This will be augmented with optional public key authentication
  in future versions.  Authenticating using a key is exempt from the 
  requirement to maintain a session and handle CSRF tokens.*

  

## <a name="1.6"></a>Validation and Error Handling


### <a name="1.6.1"></a>Invalid Requests


BAD REQUEST (400) responses to POSTs or PUTs may be interpreted as validation errors
resulting from errors in fields submitted.  The body of the response contains a dictionary of
field names with corresponding error messages, which can be presented to the user as validation
errors on the fields.

For example, attempting to create a file system with a name longer than 8 characters
may result in a 400 response with the following body:

```json
    {
        "name": "Filesystem name 'verylongname' is too long (limit 8 characters)"
    }
```

BAD REQUEST (400) responses to GETs and DELETEs indicate that something more
serious was wrong with the request, for example, the caller attempted to filter
or sort on a field that is not permitted.

### <a name="1.6.2"></a>Exceptions


If an unhandled exception, INTERNAL SERVER ERROR (500), occurs during an API call, and the 
manager server is running in development mode, the exception and traceback will be serialized and returned as JSON:

```json
    {
        "error_message": "Exception 'foo'",
        "traceback": "Traceback (most recent call last):\n  File "/usr/lib/python2.7/site-packages/django/core/handlers/base.py", line 111, in get_response\n    response = callback(request, *callback_args, **callback_kwargs)"
    }
```

## <a name="1.7"></a>Example Client


The example below is written in Python``*`` and uses the ``python-requests``
module for HTTP operations.  It demonstrates how to establish a session, authenticate,
and retrieve a list of hosts.

```python
import os
import requests
import json
from urlparse import urljoin

LOCAL_CA_FILE = "chroma.ca"


def setup_ca(url):
    """
    To verify the server's identity on subsequent connections, first
    download the manager server's local CA.
    """

    if os.path.exists(LOCAL_CA_FILE):
        os.unlink(LOCAL_CA_FILE)

    response = requests.get(urljoin(url, "certificate/"), verify = False)
    if response.status_code != 200:
        raise RuntimeError("Failed to download CA: %s" % response.status_code)

    open(LOCAL_CA_FILE, 'w').write(response.content)
    print "dir %s" % os.getcwd()
    print "Stored chroma CA certificate at %s" % LOCAL_CA_FILE


def list_hosts(url, username, password):
    # Create a local session context
    session = requests.session()
    session.headers = {"Accept": "application/json", "Content-type": "application/json"}
    session.verify = LOCAL_CA_FILE

    # Obtain a session ID from the API
    response = session.get(urljoin(url, "api/session/"))
    if not 200 <= response.status_code < 300:
        raise RuntimeError("Failed to open session")
    session.headers['X-CSRFToken'] = response.cookies['csrftoken']
    session.cookies['csrftoken'] = response.cookies['csrftoken']
    session.cookies['sessionid'] = response.cookies['sessionid']

    # Authenticate our session by username and password
    response = session.post(urljoin(url, "api/session/"), data = json.dumps({'username': username, 'password': password}))
    if not 200 <= response.status_code < 300:
        raise RuntimeError("Failed to authenticate")

    # Get a list of servers
    response = session.get(urljoin(url, "api/host/"))
    if not 200 <= response.status_code < 300:
        raise RuntimeError("Failed to get host list")
    body_data = json.loads(response.text)
    # Print out each host's address
    return [host['fqdn'] for host in body_data['objects']]

if __name__ == '__main__':
    url = "https://localhost:8000/"
    username = 'debug'
    password = 'password'
    setup_ca(url)
    print list_hosts(url, username, password)
```

## <a name="1.8"></a>API Reference


**Note:** in addition to the information in this document, you may inspect the 
available API resources and their fields on a running manager server.  To enumerate 
available resources, use GET ``/api/``.  The resulting list includes links to 
individual resource schemas like ``/api/host/schema``.


* [alert_type](#alert_type)
* [help](#help)
* [server_profile](#server_profile)
* [power_control_type](#power_control_type)
* [pacemaker_configuration](#pacemaker_configuration)
* [copytool](#copytool)
* [copytool_operation](#copytool_operation)
* [client_mount](#client_mount)
* [group](#group)
* [log](#log)
* [power_control_device](#power_control_device)
* [network_interface](#network_interface)
* [power_control_device_outlet](#power_control_device_outlet)
* [nid](#nid)
* [alert](#alert)
* [test_host](#test_host)
* [job](#job)
* [lnet_configuration](#lnet_configuration)
* [user](#user)
* [volume_node](#volume_node)
* [registration_token](#registration_token)
* [step](#step)
* [corosync_configuration](#corosync_configuration)
* [target](#target)
* [alert_subscription](#alert_subscription)
* [volume](#volume)
* [storage_resource_class](#storage_resource_class)
* [storage_resource](#storage_resource)
* [package](#package)
* [host](#host)
* [system_status](#system_status)
* [session](#session)
* [command](#command)
* [filesystem](#filesystem)
* [ha_cluster](#ha_cluster)
* [host_profile](#host_profile)


[Top of page](#1.0)

<a id="alert_type"></a>
### alert_type (/api/alert_type/)
Description

> A list of possible alert types. Use for populating alert subscriptions.

Fields

> * description:	Unicode string data. Ex: “Hello World”
> * id:	Integer record identifier, unique for objects of this type
> * resource_uri:	URL for this object

Request options
> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="help"></a>
### help (/api/help/)¶

Description

> This resource provides contextual help for use in user interfaces.
>
> GETs to the /conf_param/ sub-url respond with help for Lustre configuration parameters. There are two ways to do this GET:
>
> * Set the keys parameter to a comma-separated list of configuration parameter names to get help for particular parameters.
> * Set the kind parameter to one of ‘OST’, ‘MDT’ or ‘FS’ to get all possible configuration parameters for this type of object.
>
> The response is a dictionary where the key is a configuration parameter name and the value is a help string.

Fields

> `resource_uri`:	URL for this object

Request options

> * Allowed list methods: none
> * Allowed detail methods: none
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="server_profile"></a>
### server_profile (/api/server_profile/)

Description None

Fields

> * **corosync:**	Boolean, True if the host will manage corosync
> * **corosync2:**	Boolean, True if the host will manage corosync2
> * **default:**	If True, this profile is presented as the default when addingstorage servers
> * **initial_state:**	Unicode string data. Ex: “Hello World”
> * **managed:**	Boolean, True if the host will be managed
> * **name:**	String, unique name
> * **ntp:**	Boolean, True if the host will manage ntp
> * **pacemaker:**	Boolean, True if the host will manage pacemaker
> * **resource_uri:**	URL for this object
> * **ui_description:**	Description of the server profile
> * **ui_name:**	String, human readable name
> * **user_selectable:** Boolean data. Ex: True
> * **worker:**	Boolean, True if the host is available to be used as a Lustre worker node

Request options
> * Allowed list methods: GET
> * Allowed detail methods: GET, POST, PUT, DELETE, PATCH
> * Allowed ordering fields: managed, default
> * Allowed filtering fields:
>    * default (exact)
>    * worker (exact)
>    * user_selectable (exact)
>    * managed (exact)
>    * name (exact)


[API Reference](#1.8)

<a id="power_control_type"></a>
### power_control_type (/api/power_control_type/)¶

Description

> A type (make/model, etc.) of power control device

Fields

> * **agent**:	Fencing agent (e.g. fence_apc, fence_ipmilan, etc.)
> * **default_options**: Default set of options to be passed when invoking fence agent (May be null)
> * **default_port**:	Network port used to access power control device
> * **id**:	Integer record identifier, unique for objects of this type
> * **make**:	Device manufacturer string (May be null)
> * **max_outlets**:	The maximum number of outlets which may be associated with an instance of this device type (0 is unlimited)
> * **model**:	Device model string (May be null)
> * **monitor_template**: Command template for checking that a PDU is responding
> * **name**:	Unicode string data. Ex: “Hello World”
> * **outlet_list_template**: Command template for listing all outlets on a PDU (May be null)
> * **outlet_query_template**: Command template for querying an individual outlet’s state
> * **powercycle_template**: Command template for cycling an outlet
> * **poweroff_template**: Command template for switching an outlet off
> * **poweron_template**: Command template for switching an outlet on
> * **resource_uri**:	URL for this object

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PUT, DELETE
> * Allowed ordering fields: name, make, model
> * Allowed filtering fields:
>    * make (exact)
>    * name (exact)

[API Reference](#1.8)

<a id="pacemaker_configuration"></a>
### pacemaker_configuration (/api/pacemaker_configuration/)¶

Description

> LNetConfiguration information.

Fields

> * **available_jobs**:	List of {‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: } for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of {‘verb’:, ‘state’:} for possible states (for use with POST)
> * **content_type_id**: Integer type identifier
> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **label**:	Non-unique human readable name for presentation
> * **locks**:	Lists of locked job ids for this object
> * **not_deleted**:	Boolean data. Ex: True (May be null)
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”

Request options
> * Allowed list methods: GET, PUT
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * host (including dereferenced attributes)
>   * host__fqdn (exact, startswith)
>   * id (exact)


[API Reference](#1.8)

<a id="copytool"></a>
### copytool (/api/copytool/)

Description None

Fields

> * **active_operations_count**: Integer data. Ex: 2673
> * **archive**:	HSM archive number
> * **available_jobs**:	List of {‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: } for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of {‘verb’:, ‘state’:} for possible states (for use with POST)
> * **bin_path**:	Path to copytool binary on HSM worker node
> * **content_type_id**: Integer type identifier
> * **filesystem**:	A single related resource. Can be either a URI or set of nested resource data.
> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **hsm_arguments**:	Copytool arguments that are specific to the HSM implementation
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **index**:	Instance index, used to uniquely identify per-host path-filesystem-archive instances
> * **label**:	Non-unique human readable name for presentation
> * **locks**:	Lists of locked job ids for this object
> * **mountpoint**:	Lustre mountpoint on HSM worker node
> * **pid**:	Current PID, if known (May be null)
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **uuid**:	UUID as assigned by cdt (May be null)

Request options
> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * filesystem_id (exact)


[API Reference](#1.8)

<a id="copytool_operation"></a>
### copytool_operation (/api/copytool_operation/)¶

Description None

Fields

> * **copytool**:	A single related resource. Can be either a URI or set of nested resource data. (May be null)
> * **description**:	Unicode string data. Ex: “Hello World”
> * **fid**:	Lustre FID of file (May be null)
> * **finished_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43” (May be null)
> * **id**:	Integer record identifier, unique for objects of this type
> * **info**:	Additional information, if available (May be null)
> * **path**:	Lustre path of file (May be null)
> * **processed_bytes**: Count of bytes processed so far for running operation (May be null)
> * **resource_uri**:	URL for this object
> * **started_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43” (May be null)
> * **state**:	Integer data. Ex: 2673
> * **total_bytes**:	Expected total bytes for running operation (May be null)
> * **type**:	Integer data. Ex: 2673
> * **updated_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43” (May be null)

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="client_mount"></a>
### client_mount (/api/client_mount/)

Description None

Fields

> * **filesystem**:	A single related resource. Can be either a URI or set of nested resource data.
> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **mountpoint**:	Unicode string data. Ex: “Hello World”
> * **not_deleted**:	Boolean data. Ex: True (May be null)
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, POST, PUT, DELETE, PATCH
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * host (exact)
>   * filesystem (exact)

[API Reference](#1.8)

<a id="group"></a>
### group (/api/group/)¶

Description

> A user group. Users inherit the permissions of groups of which they are a member. Groups are used internally to refer to factory-configured profiles, so this resource is read-only.

Fields

> * **id**:	Integer record identifier, unique for objects of this type
> * **name**:	Unicode string data. Ex: “Hello World”
> * **resource_uri**:	URL for this object

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: name
> * Allowed filtering fields:
>   * name (exact, iexact)


[API Reference](#1.8)

<a id="log"></a>
### log (/api/log/)¶

Description

> syslog messages collected by the manager server.

Fields

> * **datetime**:	A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **facility**:	Integer data. RFC5424 facility
> * **fqdn**:	FQDN of the host from which the message was received. Note that this host mayno longer exist or its FQDN may have changed since.
> * **id**:	Integer record identifier, unique for objects of this type
> * **message**:	Unicode string data. Ex: “Hello World”
> * **message_class**:	Unicode string. One of [‘NORMAL’, ‘LUSTRE’, ‘LUSTRE_ERROR’, ‘COPYTOOL’, ‘COPYTOOL_ERROR’]
> * **resource_uri**:	URL for this object
> * **severity**:	Integer data. RFC5424 severity
> * **substitutions**:	List of dictionaries describing substrings which may be used to decorate the ‘message’ attribute by adding hyperlinks. Each substitution has start, end, label and resource_uri attributes. (May be null)
> * **tag**:	Unicode string data. Ex: “Hello World”

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: datetime, fqdn
> * Allowed filtering fields:
>   * message (contains, exact, startswith, endswith)
>   * tag (contains, exact, startswith, endswith)
>   * message_class (exact, contains, startswith, endswith, in)
>   * fqdn (contains, exact, startswith, endswith)
>   * datetime (exact, gte, lte, gt, lt)

[API Reference](#1.8)

<a id="power_control_device"></a>
### power_control_device (/api/power_control_device/)

Description

> An instance of a power control device, associated with a power control type

Fields

> * **address**:	IP address of power control device
> * **device_type**:	A single related resource. Can be either a URI or set of nested resource data.
> * **id**:	Integer record identifier, unique for objects of this type
> * **name**:	Optional human-friendly display name (defaults to address)
> * **options**:	Custom options to be passed when invoking fence agent (May be null)
> * **outlets**:	Many related resources. Can be either a list of URIs or list of individually nested resource data. (May be null)
> * **port**:	Network port used to access power control device
> * **resource_uri**:	URL for this object
> * **username**:	Username for device administration

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PUT, DELETE
> * Allowed ordering fields: name
> * Allowed filtering fields:
>   * name (exact)

[API Reference](#1.8)

<a id="network_interface"></a>
### network_interface (/api/network_interface/)¶

Description

> NetworkInterface information.

Fields

> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **id**:	Integer record identifier, unique for objects of this type
> * **inet4_address**:	Unicode string data. Ex: “Hello World”
> * **inet4_prefix**:	Integer data. Ex: 2673
> * **lnd_types**:	A list of data. Ex: [‘abc’, 26.73, 8]
> * **name**:	Unicode string data. Ex: “Hello World”
> * **nid**:	A single related resource. Can be either a URI or set of nested resource data. (May be null)
> * **resource_uri**:	URL for this object
> * **state_up**:	Boolean data. Ex: True
> * **type**:	Unicode string data. Ex: “Hello World”

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * host (including dereferenced attributes)
>   * id (exact)

[API Reference](#1.8)

<a id="power_control_device_outlet"></a>
### power_control_device_outlet (/api/power_control_device_outlet/)

Description

> An outlet (individual host power control entity) associated with a Power Control Device.

Fields

> * **device**:	A single related resource. Can be either a URI or set of nested resource data.
> * **has_power**:	Outlet power status (On, Off, Unknown) (May be null)
> * **host**:	A single related resource. Can be either a URI or set of nested resource data. (May be null)
> * **id**:	Integer record identifier, unique for objects of this type
> * **identifier**:	A string by which the associated device can identify the controlled resource (e.g. PDU outlet number, libvirt domain name, ipmi mgmt address, etc.)
> * **resource_uri**:	URL for this object

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PUT, DELETE, PATCH
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="nid"></a>
### nid (/api/nid/)¶

Description

> Nid information.

Fields

> * **lnd_network**:	The lustre network number for this link (May be null)
> * **lnd_type**:	The protocol type being used over the link (May be null)
> * **lnet_configuration**: A single related resource. Can be either a URI or set of nested resource data.
> * **network_interface**: A single related resource. Can be either a URI or set of nested resource data.
> * **resource_uri**:	URL for this object

Request options

> * Allowed list methods: GET, POST, DELETE
> * Allowed detail methods: GET, POST, PUT, DELETE
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * lnet_configuration (including dereferenced attributes)
>   * id (exact)
>   * network_interface (including dereferenced attributes)


[API Reference](#1.8)

<a id="alert"></a>
### alert (/api/alert/)¶

Description

> Notification of a bad health state. Alerts refer to particular objects (such as servers or targets), and can either be active (indicating this is a current problem) or inactive (indicating this is a historical record of a problem).

Fields

> * **_message**:	Message associated with the Alert. Created at Alert creation time (May be null)
> * **active**:	Boolean data. Ex: True (May be null)
> * **affected**:	List of objects which are affected by the alert (e.g. a target alert also affects the file system to which the target belongs) (May be null)
> * **alert_item**:	URI of affected item
> * **alert_item_id**:	Integer data. Ex: 2673 (May be null)
> * **alert_item_str**:	A human readable noun describing the object that is the subject of the alert
> * **alert_type**:	Unicode string data. Ex: “Hello World”
> * **begin**:	Time at which the alert started
> * **dismissed**:	True denotes that the user has acknowledged this alert.
> * **end**:	Time at which the alert was resolved if active is false, else time that the alert was last checked (e.g. time when we last checked an offline target was still not offline) (May be null)
> * **id**:	Integer record identifier, unique for objects of this type
> * **lustre_pid**:	Integer data. Ex: 2673 (May be null)
> * **message**:	Human readable description of the alert, about one sentence
> * **record_type**:	The type of the alert described as a Python classes
> * **resource_uri**:	URL for this object
> * **severity**:	String indicating the severity of the alert, one of [‘INFO’, ‘DEBUG’, ‘CRITICAL’, ‘WARNING’, ‘ERROR’]
> * **variant**:	Unicode string data. Ex: “Hello World”

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET, PATCH, PUT
> * Allowed ordering fields: begin, end, active
> * Allowed filtering fields:
>   * begin (exact, gte, lte, gt, lt)
>   * alert_type (exact, contains, startswith, endswith, in)
>   * record_type (exact, contains, startswith, endswith, in)
>   * active (exact)
>   * message (contains, exact, startswith, endswith)
>   * id (exact, gte, lte, gt, lt)
>   * end (exact, gte, lte, gt, lt)
>   * severity (exact, contains, startswith, endswith, in)
>   * created_at (exact, gte, lte, gt, lt)
>   * dismissed (exact)
>   * alert_item_id (exact, gte, lte, gt, lt)
>   * lustre_pid (exact, gte, lte, gt, lt)

[API Reference](#1.8)

<a id="test_host"></a>
### test_host (/api/test_host/)

Description

> A request to test a potential host address for accessibility, typically used prior to creating the host. Only supports POST with the ‘address’ field.

Fields

> * **address**:	Same as address field on host resource.
> * **auth_type**:	SSH authentication type. If has the value ‘root_password_choice’, then the root_password field must be non-empty, and if the value is ‘private_key_choice’ then the private_key field must be non empty. All other values are ignored and assume existing private key. This field is not for actual ssh connections. It is used to validate that enough information is available to attempt the chosen auth_type.
> * **private_key**:	ssh private key matching a public key on the new server.
> * **private_key_passphrase**: passphrase to decrypt private key
> * **resource_uri**:	URL for this object
> * **root_pw**:	ssh root password to new server.
> * **server_profile**:	Server profile chosen

Request options

> * Allowed list methods: POST
> * Allowed detail methods: none
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="job"></a>
### job (/api/job/)

Description

> Jobs refer to individual units of work that the server is doing. Jobs may either run as part of a Command, or on their own. Jobs which are necessary to the completion of more than one command may belong to more than one command.
> 
> For example:
>
> * a Command to start a filesystem has a Job for starting each OST.
> * a Command to setup an OST has a series of Jobs for formatting, registering etc
> 
> Jobs which are part of the same command may run in parallel to one another.
>
> The lock objects in the read_locks and write_locks fields have the following form:
>```json
> {
>    "id": "1",
>    "locked_item_id": 2,
>    "locked_item_content_type_id": 4
>}
>```
> The `id` and `content_type_id` of the locked object form a unique identifier which can be compared with API-readable objects which have such attributes.

Fields

> * **available_transitions**: List of {‘verb’:, ‘state’:} for possible states (for use with POST)
> * **cancelled**:	True if the job has completed as a result of a user cancelling it, or if it never started because of a failed dependency
> * **class_name**:	Internal class name of job
> * **commands**:	Commands which require this job to complete sucessfully in order to succeed themselves (May be null)
> * **created_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **description**:	Human readable string around one sentence long describing what the job is doing
> * **errored**:	True if the job has completed with an error
> * **id**:	Integer record identifier, unique for objects of this type
> * **modified_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **read_locks**:	List of objects which must stay in the required state while this job runs (May be null)
> * **resource_uri**:	URL for this object
> * **state**:	One of (‘pending’, ‘tasked’, ‘complete’)
> * **step_results**:	List of step results
> * **steps**:	Steps executed within this job (May be null)
> * **wait_for**:	List of other jobs which must complete before this job can run (May be null)
> * **write_locks**:	List of objects which must be in a certain state for this job to run, and may be modified by this job while it runs. (May be null)

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: created_at
> * Allowed filtering fields:
>   * state (exact, in)
>   * id (exact, in)

[API Reference](#1.8)

<a id="lnet_configuration"></a>
### lnet_configuration (/api/lnet_configuration/)¶

Description

> LNetConfiguration information.

Fields

> * **available_jobs**:	List of {‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: } for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of {‘verb’:, ‘state’:} for possible states (for use with POST)
> * **content_type_id**: Integer type identifier
> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **label**:	Non-unique human readable name for presentation
> * **locks**:	Lists of locked job ids for this object
> * **nids**:	Many related resources. Can be either a list of URIs or list of individually nested resource data. (May be null)
> * **not_deleted**:	Boolean data. Ex: True (May be null)
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”

Request options

> * Allowed list methods: GET, PUT
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * host (including dereferenced attributes)
>   * host__fqdn (exact, startswith)
>   * id (exact)


[API Reference](#1.8)

<a id="user"></a>
### user (/api/user/)

Description

> A user account

Fields

> * **alert_subscriptions**: List of alert subscriptions (alerts for which this userwill be sent emails. See alert_subscription resourcefor format (May be null)
> * **email**:	Unicode string data. Ex: “Hello World”
> * **first_name**:	Unicode string data. Ex: “Hello World”
> * **full_name**:	Human readable form derived from first_name and last_name
> * **groups**:	List of groups that this user is a member of. May only be modified by superusers (May be null)
> * **id**:	Integer record identifier, unique for objects of this type
> * **is_superuser**:	Is the user a superuser
> * **last_name**:	Unicode string data. Ex: “Hello World”
> * **new_password1**:	Used for modifying password (request must be made by the same user or by a superuser)
> * **new_password2**:	Password confirmation, must match new_password1
> * **password1**:	Used when creating a user (request must be made by a superuser)
> * **password2**:	Password confirmation, must match password1
> * **resource_uri**:	URL for this object
> * **username**:	Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PUT, DELETE
> * Allowed ordering fields: username, email
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="volume_node"></a>
### volume_node (/api/volume_node/)

Description

> Represents a device node on a particular host, which accesses a particular volume. Usually accessed as an attribute of a volume rather than on its own. 
>
> This resource cannot be written to directly. To update use and primary, PUT to the volume that the node belongs to. 
> 
> This resource is used by the CLI.

Fields

> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **host_id**:	id of the host that this device node is on
> * **host_label**:	label attribute of the host that this device node is on, as a convenience for presentation
> * **id**:	Integer record identifier, unique for objects of this type
> * **path**:	Device node path, e.g. ‘/dev/sda/’
> * **primary**:	If true, this node will be used for the primary Lustre server when creating a target
> * **resource_uri**:	URL for this object
> * **use**:	If true, this node will be used as a Lustre server when creating a target (if primary is not set, this node will be used as a secondary server)
> * **volume_id**:	id of the volume that this node belongs to

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * path (exact)
>   * host (exact)

[API Reference](#1.8)

<a id="registration_token"></a>
### registration_token (/api/registration_token/)¶

Description

> Server registration tokens. To add a server via HTTPS registration, acquire one of these first. 
>
> POSTs may be passed ‘expiry’ and ‘credits’
>
> PATCHs may only be passed ‘cancelled’

Fields

> * **cancelled**:	Boolean, whether this token has been manually cancelled. Once this is set, thetoken will no longer be accessible. Initially false.
> * **credits**:	Integer, the number of servers which may register using this token before it expires (default 1)
> * **expiry**:	DateTime, at which time this token will expire. Defaults to 60 seconds in the future.
> * **id**:	Integer record identifier, unique for objects of this type
> * **profile**:	Server profile to be used when setting up servers using this token
> * **register_command**: Command line to run on a storage server to register it using this token
> * **resource_uri**:	URL for this object
> * **secret**:	String, the secret used by servers to authenticate themselves (16 characters alphanumeric)String, the secret used by servers to authenticate themselves (16 characters alphanumeric)

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: PATCH, GET
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="step"></a>
### step (/api/step/)

Description

> A step belongs to a Job. Steps execute sequentially, and may be retried. A given Job may have multiple ‘step 1’ records if retries have occurred, in which case they may be distinguished by their created_at attributes.
>
> The details of the steps for a job are usually only interesting if something has gone wrong and the user is interested in any captured exceptions or console output.
>
> Don’t load steps for a job unless they’re really needed; the console output may be large.

Fields

> * **args**:	A dictionary of data. Ex: {‘price’: 26.73, ‘name’: ‘Daniel’}
> * **backtrace**:	Backtrace of an exception, if one occurred
> * **class_name**:	Name of the class representing this step
> * **console**:	Combined standard out and standard error from all subprocesses run while completing this step. This includes output from successful as well as unsuccessful commands, and may be very verbose.
> * **created_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **description**:	Unicode string data. Ex: “Hello World”
> * **id**:	Integer record identifier, unique for objects of this type
> * **log**:	Human readable summary of progress during execution.
> * **modified_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **resource_uri**:	URL for this object
> * **result**:	Arbitrary result data. (May be null)
> * **state**:	One of incomplete, failed, success
> * **step_count**:	Number of steps in this job
> * **step_index**:	Zero-based index of this step within the steps of a job. If a step is retried, then two steps can have the same index for the same job.

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: created_at, modified_at
> * Allowed filtering fields:
>   * job (exact)
>   * id (exact, in)

[API Reference](#1.8)

<a id="corosync_configuration"></a>
### corosync_configuration (/api/corosync_configuration/)

Description

> Corosync Configuration information.

Fields

> * **available_jobs**:	List of {‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: } for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of {‘verb’:, ‘state’:} for possible states (for use with POST)
> * **content_type_id**: Integer type identifier
> * **corosync_reported_up**: True if corosync on a node in this node’s cluster reports that this node is online
> * **host**:	A single related resource. Can be either a URI or set of nested resource data.
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **label**:	Non-unique human readable name for presentation
> * **locks**:	Lists of locked job ids for this object
> * **mcast_port**:	Integer data. Ex: 2673 (May be null)
> * **network_interfaces**: Network interfaces the form part of the corosync configuration. (May be null)
> * **not_deleted**:	Boolean data. Ex: True (May be null)
> * **record_type**:	Unicode string data. Ex: “Hello World”
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”

Request options

> * Allowed list methods: GET, PUT
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * host (including dereferenced attributes)
>   * host__fqdn (exact, startswith)
>   * id (exact)

[API Reference](#1.8)

<a id="target"></a>
### target (/api/target/)

Description

> A Lustre target.
>
> Typically used for retrieving targets for a particular file system (by filtering on filesystem_id) and/or of a particular type (by filtering on kind).
>
> A Lustre target may be a management target (MGT), a metadata target (MDT), or an object store target (OST).
>
> A single target may be created using POST, and many targets may be created using PATCH, with a request body as follows:
> 
>```json
> {
>   "objects": [...one or more target objects...],
>   "deletions": []
> }
>```

Fields

> * **active_host**:	The server on which this target is currently started, or null if the target is not currently started (May be null)
> * **active_host_name**: Human readable label for the host on which this target is currently started
> * **available_jobs**:	List of {‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: } for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of {‘verb’:, ‘state’:} for possible states (for use with POST)
> * **conf_params**:	A dictionary of data. Ex: {‘price’: 26.73, ‘name’: ‘Daniel’}
> * **content_type_id**: Integer type identifier
> * **failover_server_name**: Human readable label for the secondary server for this target
> * **failover_servers**: A list of data. Ex: [‘abc’, 26.73, 8] (May be null)
> * **filesystem**:	For OSTs and MDTs, the owning file system. Null for MGTs. (May be null)
> * **filesystem_id**:	For OSTs and MDTs, the id attribute of the owning file system. Null for MGTs. (May be null)
> * **filesystem_name**: For OSTs and MDTs, the name attribute of the owning file system. Null for MGTs.
> * **filesystems**:	For MGTs, the list of file systems belonging to this MGT. Null for other targets. (May be null)
> * **ha_label**:	Label used for HA layer; human readable but unique (May be null)
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **index**:	Index of the target (May be null)
> * **inode_count**:	The number of inodes in this target’sbacking store (May be null)
> * **inode_size**:	Size in bytes per inode (May be null)
> * **kind**:	Type of target, one of [‘OST’, ‘MDT’, ‘MGT’]
> * **label**:	Non-unique human readable name for presentation
> * **locks**:	Lists of locked job ids for this object
> * **name**:	Lustre target name, e.g. ‘testfs-OST0001’. May be null if the target has not yet been registered. (May be null)
> * **primary_server**:	A single related resource. Can be either a URI or set of nested resource data.
> * **primary_server_name**: Human readable label for the primary server for this target
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **uuid**:	UUID of the target’s internal file system. May be null if the target has not yet been formatted (May be null)
> * **volume**:	The volume on which this target is stored.
> * **volume_name**:	The label attribute of the volume on which this target exists

Request options

> * Allowed list methods: GET, POST, PATCH
> * Allowed detail methods: GET, PUT, DELETE
> * Allowed ordering fields: volume_name, name
> * Allowed filtering fields:
>   * immutable_state (exact)
>   * kind (exact)
>   * name (exact)
>   * host_id (exact)
>   * filesystem_id (exact)
>   * id (exact, in)

[API Reference](#1.8)

<a id="alert_subscription"></a>
### alert_subscription (/api/alert_subscription/)

Description None

Fields

> * **alert_type**:	Content-type id for this subscription’s alert class
> * **id**:	Integer record identifier, unique for objects of this type
> * **resource_uri**:	URL for this object
> * **user**:	User to which this subscription belongs

Request options

> * Allowed list methods: GET, POST, PATCH
> * Allowed detail methods: GET, DELETE, PUT
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="volume"></a>
### volume (/api/volume/)

Description

> A volume represents a unit of storage suitable for use as a Lustre target. This typically corresponds to a SCSI LUN. Since volumes are frequently accessible from multiple hosts via different device nodes, the device node information is represented in the volume_node resource. A list of volume nodes is provided with each volume in the volume_nodes list attribute.
>
> Depending on available volume nodes, the status attribute may be set to one of:
>
> * **configured-ha**:	We can build a highly available lustre target on this volume.
> * **configured-noha**: We can build a Lustre target on this volume but it will only be accessed by a single server so won’t be highly available.
> * **unconfigured**:	We do not have enough information to build a Lustre target on this volume. Either it has no nodes, or none of the nodes is marked for use as the primary server.
> 
> To configure the high availability for a volume before creating a Lustre target, you must update the use and primary attributes of the volume nodes. To update the use and primary attributes of a node, use PUT to the volume to access the volume_node attribute for the node. Only one node can be identified as primary.
>
> PUT to a volume with the volume_nodes attribute populated to update the use and primary attributes of the nodes (i.e. to configure the high availability for this volume before creating a Lustre target). You may only identify one node as primary.

Fields

> * **filesystem_type**: Unicode string data. Ex: “Hello World” (May be null)
> * **id**:	Integer record identifier, unique for objects of this type
> * **kind**:	A human readable noun representing thetype of storage, e.g. ‘Linux partition’, ‘LVM LV’, ‘iSCSI LUN’
> * **label**:	Non-unique human readable name for presentation
> * **resource_uri**:	URL for this object
> * **size**:	Integer number of bytes. Can be null if this device was manually created, rather than detected. (May be null)
> * **status**:	A string representing the high-availability configuration status of the volume.
> * **storage_resource**: The storage_resource corresponding to the device which this Volume represents (May be null)
> * **usable_for_lustre**: True if the Volume can be selected for use as a new Lustre Target
> * **volume_nodes**:	Device nodes which point to this volume (May be null)

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: label, size
> * Allowed filtering fields:
>   * id (exact)
>   * label (exact, endswith)

[API Reference](#1.8)

<a id="storage_resource_class"></a>
### storage_resource_class (/api/storage_resource_class/)

Description

> Defines a type of storage_resource that can be created.
>
> Storage resource classes belong to a particular plugin (plugin_name attribute) . The name of the storage resource class (class_name attribute) is unique within the plugin.

Fields

> * **class_name**:	Unicode string data. Ex: “Hello World”
> * **columns**:	List of resource attributes to be used when presenting resource in tabular form
> * **fields**:	List of resource attributes which should be presented in an input form
> * **id**:	Integer record identifier, unique for objects of this type
> * **label**:	Non-unique human readable name for presentation
> * **plugin_internal**: Boolean data. Ex: True
> * **plugin_name**:	Unicode string data. Ex: “Hello World”
> * **resource_uri**:	URL for this object
> * **user_creatable**:	Boolean data. Ex: True

Request options

> * Allowed list methods: GET
> * Allowed detail methods: GET
> * Allowed ordering fields: class_name
> * Allowed filtering fields:
>   * class_name (exact)
>   * user_creatable (exact)
>   * plugin_name (exact)
>   * plugin_internal (exact)


[API Reference](#1.8)

<a id="storage_resource"></a>
### storage_resource (/api/storage_resource/)

Description

> Storage resources are objects within the storage plugin framework. Note: the term ‘resource’ is used to refer to REST API resources and also in this context to refer to the separate concept of a storage resource.
> 
> A storage resource is of a class defined by the storage_resource_class resource.
> 
> This resource has a special ancestor_of filter argument, which may be set to the ID of a storage resource to retrieve all the resources that are its ancestors.

Fields

> * **alerts**:	List of active alert objects which are associated with this resource
> * **alias**: The human readable name of the resource (may be set by user)
> * **attributes**:	Dictionary of attributes as defined by the storage plugin
> * **charts**:	List of charts for this resource (defined by the plugin as Meta.charts)
> * **class_name**:	Name of a storage_resource_class
> * **default_alias**: The default human readable name of the resource
> * **deletable**: If true, this object may be removed with a DELETE operation
> * **id**:	Integer record identifier, unique for objects of this type
> * **parent_classes**:	List of strings, parent classes ofthis object’s class. (May be null)
> * **plugin_name**: Name of the storage plugin which defines this resource
> * **propagated_alerts**: List of active alert objects which are associated with ancestors of this resource
> * **resource_uri**:	URL for this object
> * **stats**: List of statistics defined by the plugin, with recent data for each. Each statistic has the format:
>
>   ```
>    {
>      "name": <internal name of the statistic>,
>      "label": <human readable name of the statistic>,
>      "type": <'histogram' or 'timeseries'>,
>      "unit_name": <human readable unit>,
>      "data": <for histograms only>
>    }
>   ```
>
>    The data format for histograms is:
>
>   ```
>    {
>      "bin_labels": <list of strings>,
>      "values": <list of floats>
>    }
>   ```
>
>   For time series statistics, fetch the data separately with a call for the /metrics/ sub-URL of the resource.
> * **storage_id_str**:	Unicode string data. Ex: “Hello World”

Request options

> * Allowed list methods: GET, POST, PUT, DELETE, PATCH
> * Allowed detail methods: GET, POST, PUT, DELETE, PATCH
> * Allowed ordering fields: none
> * Allowed filtering fields:
>   * class_name (exact)
>   * plugin_name (exact)


[API Reference](#1.8)

<a id="package"></a>
### package (/api/package/)

Description

> Represents a particular version of a package. Includes which servers have this package installed, and on which servers this package is available. Filter by `host` to obtain a report including only packages which are installed on or available to a particular host.

Fields

> * **arch**:	Unicode string data. Ex: “Hello World”
> * **available_hosts**: List of URIs of servers on which this package is available (May be null)
> * **epoch**:	Integer data. Ex: 2673
> * **installed_hosts**: List of URIs of servers on which this package is installed (May be null)
> * **name**:	Name of the package, for example “lustre”
> * **release**:	Unicode string data. Ex: “Hello World”
> * **resource_uri**:	URL for this object
> * **version**:	Unicode string data. Ex: “Hello World”

Request options

> * Allowed list methods: GET
> * Allowed detail methods: none
> * Allowed ordering fields: name
> * Allowed filtering fields:
>   * host (exact)

[API Reference](#1.8)

<a id="host"></a>
### host (/api/host/)

Description

> Represents a Lustre server that is being monitored and managed from the manager server.
> 
> PUTs to this resource must have the state attribute set.
> 
> POSTs to this resource must have the address attribute set.

Fields

> * **address**:	A URI like `user@myhost.net:22`
> * **available_jobs**:	List of `{‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: }` for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of `{‘verb’:, ‘state’:}` for possible states (for use with POST)
> * **boot_time**:	A date & time as a string. Ex: “2010-11-10T03:07:43” (May be null)
> * **client_mounts**:	A list of data. Ex: [‘abc’, 26.73, 8] (May be null)
> * **content_type_id**: Integer type identifier
> * **corosync_configuration**: A single related resource. Can be either a URI or set of nested resource data. (May be null)
> * **fqdn**:	Unicode string, fully qualified domain name
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **install_method**:	The method used to install the agent on the server
> * **label**:	Non-unique human readable name for presentation
> * **lnet_configuration**: A single related resource. Can be either a URI or set of nested resource data.
> * **locks**:	Lists of locked job ids for this object
> * **member_of_active_filesystem**: Boolean data. Ex: True
> * **needs_update**:	True if there are package updates available for this server
> * **nids**:	A list of data. Ex: [‘abc’, 26.73, 8] (May be null)
> * **nodename**:	Unicode string, node name
> * **pacemaker_configuration**: A single related resource. Can be either a URI or set of nested resource data. (May be null)
> * **private_key**:	ssh private key matching a public key on the new server.
> * **private_key_passphrase**: passphrase to decrypt private key
> * **properties**:	Unicode string data. Ex: “Hello World”
> * **resource_uri**:	URL for this object
> * **root_pw**:	ssh root password to new server.
> * **server_profile**:	A single related resource. Can be either a URI or set of nested resource data.
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”

Request options

> * Allowed list methods: GET, POST, PUT
> * Allowed detail methods: GET, PUT, DELETE
> * Allowed ordering fields: fqdn
> * Allowed filtering fields:
>   * role (exact)
>   * id (exact)
>   * fqdn (exact, startswith)

[API Reference](#1.8)

<a id="system_status"></a>
### system_status (/api/system_status/)

Description

> The internal status of this server.

Fields

> * **postgres**:	PostgreSQL statistics
> * **rabbitmq**:	RabbitMQ statistics
> * **resource_uri**:	URL for this object
> * **supervisor**:	Supervisor status

Request options

> * Allowed list methods: GET
> * Allowed detail methods: none
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="session"></a>
### session (/api/session/)

Description

> The current user session. This resource exposes only list-style methods, all of which implicitly operate on the current session (determined from HTTP headers).
>
> In addition to finding out about who is logged in, GET operations on the session resource are a useful way of obtaining sessionid and csrftoken values (see Access control)
>
> Authenticate a session by using POST to send credentials. Use DELETE to log out from a session.

Fields

> * **read_enabled**:	If true, the current session is permitted to do GET operations on other API resources. Always true for authenticated users, depends on settings for anonymous users.
> * **resource_uri**:	URL for this object
> * **user**:	A user object (May be null)

Request options

> * Allowed list methods: GET, POST, DELETE
> * Allowed detail methods: none
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="command"></a>
### command (/api/command/)

Description

> Asynchronous user-initiated operations which create, remove or modify resources are represented by command objects. When a PUT, POST, PATCH or DELETE to a resource returns a 202 ACCEPTED response, the response body contains a command identifier. The command resource is used to query the status of these asynchronous operations.
>
> Typically this is used to poll a command for completion and find out whether it succeeded.

Fields

> * **cancelled**:	True if one or more of the command’s jobs completed with its cancelled attribute set to True, or if this command was cancelled by the user
> * **complete**:	True if all jobs have completed, or no jobs were needed to satisfy the command
> * **created_at**:	A date & time as a string. Ex: “2010-11-10T03:07:43”
> * **errored**:	True if one or more of the command’s jobs failed, or if there was an error scheduling jobs for this command
> * **id**:	Integer record identifier, unique for objects of this type
> * **jobs**:	Jobs belonging to this command
> * **logs**:	String. Concatentation of all user-visible logs from the``job`` objects associated with this command.
> * **message**:	Human readable string about one sentence long describing the action being done by the command
> * **resource_uri**:	URL for this object

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PATCH
> * Allowed ordering fields: created_at
> * Allowed filtering fields:
>   * complete (exact)
>   * created_at (gte, lte, gt, lt)
>   * dismissed (exact)
>   * cancelled (exact)
>   * errored (exact)
>   * id (exact, in)

[API Reference](#1.8)

<a id="filesystem"></a>
### filesystem (/api/filesystem/)

Description

> A Lustre file system, associated with exactly one MGT and consisting of one or mode MDTs and one or more OSTs.
>
> When using POST to create a file system, specify volumes to use like this:
>
>```json
> {
>   "osts": [{"volume_id": 22}],
>   "mdt": {"volume_id": 23},
>   "mgt": {"volume_id": 24}
> }
>```
>
> To create a file system using an existing MGT instead of creating a new MGT, set the id attribute instead of the volume_id attribute for that target (i.e. `mgt: {id: 123}`).
>
> Note: A Lustre file system is owned by an MGT, and the name of the file system is unique within that MGT. Do not use name as a globally unique identifier for a file system in your application.

Fields

> * **available_jobs**:	List of `{‘args’:{}, ‘class_name’:, ‘confirmation’:, verb: }` for possible non-state-change jobs (for use with the command resource)
> * **available_transitions**: List of `{‘verb’:, ‘state’:}` for possible states (for use with POST)
> * **bytes_free**:	Integer data. Ex: 2673
> * **bytes_total**:	Integer data. Ex: 2673
> * **client_count**:	Number of Lustre clients which are connected to this file system
> * **conf_params**:	A dictionary of data. Ex: {‘price’: 26.73, ‘name’: ‘Daniel’}
> * **content_type_id**: Integer type identifier
> * **files_free**:	Integer data. Ex: 2673
> * **files_total**:	Integer data. Ex: 2673
> * **id**:	Integer record identifier, unique for objects of this type
> * **immutable_state**: If true, this object may not have its state modified by the user (monitoring only)
> * **label**:	Non-unique human readable name for presentation
> * **locks**:	Lists of locked job ids for this object
> * **mdts**:	List of MDTs in this file system, should be at least 1 unless the file system is in the process of being deleted (May be null)
> * **mgt**:	The MGT on which this file system is registered
> * **mount_command**:	Example command for mounting this file system on a Lustre client, e.g. “mount -t lustre 192.168.0.1:/testfs /mnt/testfs” (May be null)
> * **mount_path**:	Path for mounting the file system on a Lustre client, e.g. “192.168.0.1:/testfs” (May be null)
> * **name**:	Lustre filesystem name, up to 8 characters
> * **osts**:	List of OSTs which belong to this file system (May be null)
> * **resource_uri**:	URL for this object
> * **state**:	Unicode string, may be set based on available_transitions field
> * **state_modified_at**: A date & time as a string. Ex: “2010-11-10T03:07:43”

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, DELETE, PUT
> * Allowed ordering fields: name
> * Allowed filtering fields:
>   * id (exact, in)
>   * name (exact)

[API Reference](#1.8)

<a id="ha_cluster"></a>
### ha_cluster (/api/ha_cluster/)

Description None

Fields

> * **peers**:	A list of data. Ex: [‘abc’, 26.73, 8]

Request options

> * Allowed list methods: GET
> * Allowed detail methods: none
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

<a id="host_profile"></a>
### host_profile (/api/host_profile/)

Description

> Get and set profiles associated with hosts.

Fields

> * **resource_uri**:	URL for this object

Request options

> * Allowed list methods: GET, POST
> * Allowed detail methods: GET, PUT
> * Allowed ordering fields: none
> * Allowed filtering fields: none

[API Reference](#1.8)

## <a name="1.9"></a>Legal Information


Copyright (c) 2017 Intel® Corporation. All rights reserved.
 Use of this source code is governed by a MIT-style
 license that can be found in the LICENSE file.

\* Other names and brands may be claimed as the property of others.
This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)

[Top of page](#1.0)