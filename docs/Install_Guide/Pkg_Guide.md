# <a name="1.0"></a> Server Profile Packaging Guide

[**Software Installation Guide Table of Contents**](ig_TOC.md)

## Introduction

Integrated Manager for Lustre software is delivered as a single unified
installer file, including both the central management component and the packages
deployed to storage servers. Because storage servers sometimes requires
additional packages (such as drivers) or customized packages (such as custom
Lustre builds), a mechanism is included whereby these packages can be included
in a Integrated Manager for Lustre software installation.

## Server Profiles

A server profile is metadata describing the packaging and deployment options for
a class of storage servers. Where repos contain collections of packages, server
profiles contain the instruction for the packages to be deployed to a particular
class of servers.

## Creating a Server Profile

A server profile is simply a JSON file defining various options. For example,
the JSON below is the default profile for a managed storage server:

```json
{
  "ui_name": "Managed Storage Server",
  "managed": true,
  "worker": false,
  "name": "base_managed_rh7",
  "initial_state": "managed",
  "ntp": true,
  "corosync": false,
  "corosync2": true,
  "pacemaker": true,
  "ui_description": "A storage server suitable for creating new HA-enabled filesystem targets",
  "packages": [
    "python2-iml-agent-management",
    "kernel-devel-lustre",
    "pcs",
    "fence-agents",
    "fence-agents-virsh",
    "lustre-resource-agents",
    "lustre-ldiskfs-zfs"
  ],
  "repolist": [
    "base",
    "lustre-server"
  ],
  "validation": [
    {
      "test": "distro_version < 8 and distro_version >= 7",
      "description": "The profile is designed for version 7 of EL"
    }
  ]
}
```

- **name:** An ID. This must be unique within a Integrated Manager for Lustre software
installation. To avoid name collisions, it is recommended to include the name
of your organization.

- **packages:** A list of names of required RPM packages. These are the packages
to be installed on storage servers using this profile. Note that it is usually
not necessary to list all packages: `yum` is used to install packages, so
dependencies are respected. For example, when installing `lustre-ldiskfs-zfs` we
do not also name `e2fsprogs` because it is a dependency of `lustre` which is a
dependency of `lustre-ldiskfs-zfs` and therefore installed automatically.

- **repolist:** A list of repoistory files that are needed by nodes that are
configured with this profile. The names in this list should exist as
`NAME.repo`.

- **ui_name:** A string for presentation to users of the web interface and
command line interface to IML. This should be short (a few words at most) and
meaningful to system administrators.

- **ui_description:** A string containing a more detailed explanation of what
this profile includes and what it is for. Like `ui_name`, this may be presented
to users.

- **managed:** A boolean. If true, servers using this profile will be fully
managed by IML, including the creation and modification of filesystems. If false,
servers using this profile will only be able to report monitoring data to IML.

## Installing a server profile

1. Copy your profile to the IML management server, e.g. copy `myprofile.json` to `/tmp/`
2. Register your profile using `chroma-config profile register /tmp/myprofile.json`
3. Remove `myprofile.json`, as it has now been loaded into the database.

## Setting a server profile as the default

You may wish to make a custom server profile the default, if all storage servers
managed by the installation should be of that type.

To make a named storage profile the default, enter this command on the IML
management server:

```bash
 chroma-config profile default <profile name>
```


## Yum Repo

A server repo is a standard yum .repo file.  It can contain one or more yum
repositories.

```
[lustre-client-latest]
name=Lustre Client - latest
baseurl=https://downloads.whamcloud.com/public/lustre/lustre-latest/el7/client/
enabled=1
gpgcheck=0
repo_gpgcheck=0
```

To install custom repos, they can be installed in the standard location
(`/usr/share/chroma-manager/`) and then have chroma-config scan for it.

```bash
	chroma-config repos scan 
```

Alternatively, the repo can be installed elsewhere on the manager and then imported from there:

```bash
	chroma-config repos register /path/to/example.repo
```

## Locally Hosted Yum Repo

To facilitate hosting local repos there is a process to install, create, and
register a repo given a tarball of rpms. The tarball can be compressed with any
compression type that can be auto detected with GNU tar.

```base
	chroma-config repos install reponame /path/to/example.tar.bz2
```


## Example: deploying a custom build of Lustre and some additional drivers

For this example, we will create a custom profile for a managed server with custom packages.

Provided by the customer:

- A tarball containing the custom Lustre packages
- A tarball containing the additional driver packages

Created during this example:

- A server profile referencing packages in the local repos

Assuming that this profile is for use with Acme storage servers, our customer
profile might be called `acme_storage`.  The following creates the local
repositories containing the customers extra driver rpms and custom lustre rpms.

```bash
	chroma-config repos install acme acme-1.0.0.tar.xz
	chroma-config repos install acme-lustre-server custom-lustre-server.tar.gz
```

The following uses the above created repos in a custom profile.

```json
{
  "name": "acme_storage",
  "repos": [
	"base",
	"acme",
	"acme-lustre-server"
	],
  "packages": [
    "python2-iml-agent-management",
	"lustre-ldiskfs-zfs",
	"acme-core",
	"acme-scsi"
  ],
  "ui_name": "Acme storage server",
  "ui_description": "A storage server using Acme SCSI drivers, using Acme Lustre extensions",
  "managed": true
}
```

The above profile can then be registered.

```bash
	chroma-config profile register acme.profile
```

## <a name="1.9"></a>Legal Information

Copyright (c) 2019 DDN. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.

\* Other names and brands may be claimed as the property of others.  This
product includes software developed by the OpenSSL Project for use in the
OpenSSL Toolkit. (http://www.openssl.org/)

[Top of page](#1.0)
