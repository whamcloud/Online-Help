
# <a name="1.0"></a>Scheduler Plugin Developer's Guide for Manager for Lustre\* software


## <a name="1.1"></a>Introduction

IML collects and displays metrics on a per-job basis, when enabled in Lustre.
See the Lustre manual for supported schedulers and configuration.
By default, the data is associated by unique job_id, from whichever job scheduler is configured.
In order to display more useful metata, e.g. user, a corresponding plugin must be registered to lookup the job_ids.

Plugins are registered by linking a python module (.py) in the plugin directory:  <root>/chroma_core/lib/scheduler/.
The provided plugin (procname_uid) uses the shell as the scheduler.

## <a name="1.2"></a>API


```
automodule:: chroma_core.lib.scheduler

autofunction:: fetch

attribute:: FIELDS
```


Tuple of field names that the plugin will retrieve


## <a name="1.3"></a>procname_uid


```
automodule:: chroma_core.lib.scheduler.procname_uid

autofunction:: fetch

autoattribute:: chroma_core.lib.scheduler.procname_uid.FIELDS
```


## <a name="1.4"></a>Legal Information

Copyright (c) 2017 Intel Corporation. All rights reserved.
 Use of this source code is governed by a MIT-style
 license that can be found in the LICENSE file.

\* Other names and brands may be claimed as the property of others.
This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)