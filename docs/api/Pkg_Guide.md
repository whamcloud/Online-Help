# <a name="1.0"></a> Packaging Guide for Intel® Manager for Lustre* software

[**Software API Documentation Table of Contents**](./api_TOC.md)

Introduction
------------

Intel® Manager for Lustre* software is delivered as a single unified installer file, including
both the central management component and the packages deployed to storage servers.  Because
storage servers sometimes requires additional packages (such as drivers) or customized packages 
(such as custom Lustre* builds), a mechanism is included whereby these packages can be included
in a Intel® Manager for Lustre* software installation.

Bundles
-------

A bundle is comprised of a collection of RPM packages and metadata files.  The metadata
in a bundle is comprised of a standard [yum](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-yum) ``repodata`` directory containing information about
all the included packages, plus an additional [JSON](https://en.wikipedia.org/wiki/JSON) file named ``meta`` containing information about the
bundle as a whole.

- yum: [https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-yum](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-yum)
- JSON: [https://en.wikipedia.org/wiki/JSON](https://en.wikipedia.org/wiki/JSON)


```bash
    meta
    packageA-1.0.rpm
    packageB-1.0.rpm
    repodata/
```



The format of the ``meta`` file is as follows:

```json
    {
      "name": "acme_drivers",
      "version": "x.y.z",
      "description": "Acme Corporation networking drivers"
    }
```


The ``name`` attribute serves as a unique identifier for a bundle within a Intel® Manager for Lustre* software
installation.  It is wise to include the name of your organization in this string to reduce
the likelihood of name collisions.

The ``version`` attribute is provided to allow identification of a bundle by version.

The `description` attribute is a human-readable description of the bundle.  This may be visible
to system administrators of the Intel® Manager for Lustre* software installation, so it should be something
meaningful to that audience.

Creating a Bundle
-----------------

1. Create an empty folder on a CentOS* {{site.centos_version}} or Red Hat* {{site.centos_version}} host
2. Collect the RPM packages which you wish to include in your bundle.  You will need to build RPMs for any software which is not already packaged in this format: doing so is outside the scope of this documentation.  Place these RPM files in the folder you just created.
3. Create your ``meta`` file (in the format described above) in the same folder as the RPM packages
4. Install the ``createrepo`` package using ``yum`` if it is not already installed.
5. Change directory to the folder containing your RPM packages and ``meta`` file, and run ``createrepo .``
6. Create an archive of your bundle with ``-bundle.tar.gz`` appended to the name of your bundle.  For example, ````tar czf acme_drivers-bundle.tar.gz *.rpm meta repodata````

**Warning:**
> Do not create bundles with the same name as the built-in bundles, as these will be overwritten by updates to MIntel® Manager for Lustre* software

Installing a Bundle
-------------------

To install a bundle, it must first be unpacked on the management server, and then registered.

Unpack a bundle like this:


   
```bash
mkdir /var/lib/chroma/repo/mybundle
tar zxf mybundle.tar.gz /var/lib/chroma/repo/mybundle/
```



Register a bundle like this:



```bash
chroma-config bundle register /var/lib/chroma/repo/mybundle/
```


Server Profiles
---------------

A server profile is metadata describing the packaging and deployment options for a class of storage
servers.  Where bundles contain collections of packages, server profiles contain the instruction
for the packages to be deployed to a particular class of servers.

Creating a Server Profile
-------------------------

A server profile is simply a JSON file defining various options.  For example, the JSON below is the default profile for a managed storage server:


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
  "bundles": [
    "iml-agent",
    "external"
  ],
  "ui_description": "A storage server suitable for creating new HA-enabled filesystem targets",
  "packages": {
    "iml-agent": [
      "chroma-agent-management"
    ],
    "external": [
      "kernel-devel-lustre",
      "lustre-ldiskfs-zfs"
    ]
  },
  "validation": [
    {"test": "distro_version < 8 and distro_version >= 7", "description": "The profile is designed for version 7 of EL"}
  ]
}
```


* **name:**
  An ID.  This must be unique within a Intel® Manager for Lustre* software installation. To avoid name collisions, it is recommended
  to include the name of your organization.

* **bundles:**
  A list of strings referencing installed bundles.  A storage server using this profile will have access
  to packages in all the bundles referenced here.

* **packages:**
  A dict wherein the keys are the names of a bundle, and the values are a list of names of associated RPM packages.  These are the packages to be installed on storage servers using this profile.  Note that it is usually not necessary to list all packages: ``yum`` is used to install packages, so dependencies are respected.  For example, when installing ``lustre`` we do not also name ``e2fsprogs`` because it is a dependency of ``lustre`` and therefore installed automatically.  The reason we name ``lustre-modules`` even though it too is a dependency of ``lustre`` is that naming a package here causes any exact-version dependencies (such as the dependency on a particular version of ``kernel`` to be respected even if they involve installing a downgraded package).  This mechanism is an ML modification to the default ``yum`` behaviour, included to handle Lustre*'s need for older kernel versions.

* **ui_name:**
  A string for presentation to users of the web interface and command line interface to ML.  This should be short (a few words at most) and meaningful to system administrators.

* **ui_description:**
  A string containing a more detailed explanation of what this profile includes and what it is for.  Like ``ui_name``, this may be presented to users.

* **managed:**
  A boolean.  If true, servers using this profile will be fully managed by ML, including the creation and modification of filesystems.  If false, servers using this profile will only be able to report monitoring data to ML.

Installing a server profile
---------------------------

1. Copy your profile to the ML management server, e.g. copy ``myprofile.json`` to ``/tmp/``
2. Register your profile using ``chroma-config profile register /tmp/myprofile.json``
3. Remove ``myprofile.json``, as it has now been loaded into the database.

Setting a server profile as the default
---------------------------------------

You may wish to make a custom server profile the default, if all storage servers managed by the
installation should be of that type.

To make a named storage profile the default, enter this command on the ML management server:
  
```bash
 chroma-config profile default <profile name>
```

Example: deploying a custom build of Lustre* and some additional drivers
-----------------------------------------------------------------------

For this example, we will create:

- A bundle containing the custom Lustre* packages
- A bundle containing the additional driver packages
- A server profile referencing packages in the custom bundles

Assuming that this profile is for use with Acme storage servers, our custom bundles might
be called acme_lustre and acme_drivers.  The acme_lustre bundle would contain packages with
the usual Lustre* package names, while the acme_drivers bundle would contain some new packages, which
might be called acme-core and acme-scsi.
   
```json
{
  "name": "acme_storage",
  "bundles": ["acme_lustre", "acme_drivers", "chroma-agent", "e2fsprogs"],
  "packages": {"acme_lustre": ["lustre-modules", "lustre"],
              "acme_drivers": ["acme-core", "acme-scsi"]},
  "ui_name": "Acme storage server",
  "ui_description": "A storage server using Acme SCSI drivers, using Acme Lustre* extensions",
  "managed": true
}
```

## <a name="1.9"></a>Legal Information


Copyright (c) 2017 Intel® Corporation. All rights reserved.
 Use of this source code is governed by a MIT-style
 license that can be found in the LICENSE file.

\* Other names and brands may be claimed as the property of others.
This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)

[Top of page](#1.0)
