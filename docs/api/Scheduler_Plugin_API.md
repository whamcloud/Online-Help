# <a name="1.0"></a>Scheduler Plugin Developer's Guide for Integrated Manager for Lustre* software

[**Software API Documentation Table of Contents**](./api_TOC.md)

## <a name="1.1"></a>Introduction

IML collects and displays metrics on a per-job basis, when enabled in Lustre.
See the Lustre manual for supported schedulers and configuration.
By default, the data is associated by unique job_id, from whichever job scheduler is configured.
In order to display more useful metadata, e.g. user, a corresponding plugin must be registered to lookup the job_ids.

Plugins are registered by linking a python module (.py) in the plugin directory:  `<root>/chroma_core/lib/scheduler/`.
The provided plugin (procname_uid) uses the shell as the scheduler.

## <a name="1.2"></a>API

Registered job scheduler plugins: slurm_job_id, job_id, lsb_jobid, loadl_step_id, pbs_jobid, procname_uid.

Modules will be loaded dynamically as needed. Plugins must implement fetch function as documented. Plugins should also document the available metadata fields.

```
chroma_core.lib.scheduler.fetch(ids)
```
> Given an iterable of job ids, return an interable of associated metadata dicts. Ids will be unique and requested in batch whenever possible. Plugins are responsible for any caching necessary for performance.

```
chroma_core.lib.scheduler.FIELDS
```
> tuple of field names that the plugin will retrieve

## <a name="1.3"></a>procname_uid

Shell-based scheduler which records process name and user id.

```
chroma_core.lib.scheduler.procname_uid.fetch(ids)
```
> Generate process names and user ids.

```
procname_uid.FIELDS = ('name', 'user')
```

[Top of page](#1.0)

## <a name="1.4"></a>Legal Information

Copyright (c) 2017 Intel® Corporation. All rights reserved.
 Use of this source code is governed by a MIT-style
 license that can be found in the LICENSE file.

\* Other names and brands may be claimed as the property of others.
This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)

[Top of page](#1.0)