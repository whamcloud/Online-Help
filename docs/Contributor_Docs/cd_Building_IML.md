# Building IML

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

1. Clone the [integrated-manager-for-lustre repository](https://github.com/whamcloud/integrated-manager-for-lustre)

   ```sh
   # git clone git@github.com:whamcloud/integrated-manager-for-lustre.git
   ```

1. Install the YUM Copr plugin:

   ```sh
   # yum install -y yum-plugin-copr
   ```

1. Install the `manager-for-lustre-devel` repository:

   ```sh
   # yum copr enable -y managerforlustre/manager-for-lustre-devel
   ```

1. Install needed software packages:

   ```sh
   # yum install -y rpmdevtools git ed epel-release python-setuptools
   ```

1. From the top-level directory in the repository clone:

   ```sh
   $ make rpms
   ```

The result of the above commands will be RPMs in the `_topdir/` subdirectory containing everything needed to install IML on a cluster.

---

[Top of page](#building-iml)
