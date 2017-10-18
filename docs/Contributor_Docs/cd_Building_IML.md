# <a name="Top"></a>Building IML

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

## Prerequisites

Clone of the [intel-manager-for-lustre repository](https://github.com/intel-hpdd/intel-manager-for-lustre)
```
git clone git@github.com:intel-hpdd/intel-manager-for-lustre.git
```
Install the YUM Copr plugin:
```
# yum -y install yum-plugin-copr
```
Install the manager-for-lustre and DNF YUM repositories:
```
# yum copr enable managerforlustre/manager-for-lustre
# yum copr enable ngompa/dnf-el7
```
Install needed software packages:
```
# yum -y install python-virtualenv systemd-devel postgresql-devel graphviz-devel createrepo epel-release npm python-sphinx python-django gcc
```

## How does one build IML?

From the top-level directory in the repository clone:
```
$ make
```
The result of the above command will be source tarballs and RPMs in the `dist/` subdirectory and a `iml-<version>.tar.gz` tarball in the `chroma-bundles/` subdirectory containing everything needed to install IML on a cluster.

---
[Top of page](#Top)
