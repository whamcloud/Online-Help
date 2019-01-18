# Building Rust RPMs

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

## Overview

Building Rust RPMs is still an early topic, and this document is subject to change over time.

## Generating a spec

Creating a specfile can be sped up by using [`rust2rpm`](https://pagure.io/fedora-rust/rust2rpm/).

### Steps (Assuming RHEL 7)

1. Install Python 3 and activate:

   ```bash
    yum install centos-release-scl
    yum install rh-python36
    scl enable rh-python36 bash
   ```

1. Create a virtualenv and activate:

   ```bash
   python -m venv my_project_venv
   source my_project_venv/bin/activate
   ```

1. Pull the [latest rust2rpm release](https://releases.pagure.org/fedora-rust/rust2rpm/).

1. Install the rust2rpm package locally with pip

1. Run:

   ```bash
   rust2rpm <PATH/TO/RUST/PROJECT>
   ```

1. The generated spec will contain a number of crates listed as `[dependencies]` under `BuildRequires` and `Requires`. We won't be using those directly; delete all those lines. In addition, remove `BuildRequires: rust-packaging`, and replace `ExclusiveArch: %{rust_arches}` with `ExclusiveArch: x86_64` or whatever arches you plan to support.

1. If the package you are working with is part of a workspace, there are a few more edits. Add the following after the `Source0:` line:

   ```spec
   Source1:        Cargo.lock
   %cargo_bundle_crates -l 1
   ```

### Building the SRPM

1. Install the [`rust-bundled-packaging`](https://github.com/awslabs/rust-bundled-packaging) RPM, built on iml copr:

   ```bash
   yum -y copr enable managerforlustre/manager-for-lustre-devel
   ```

1. If the package being used is in a workspace, you will need to copy the dir elsewhere. This is so the package is built in a standalone way. If so, copy the dir outside the tree so it's not associated with the workspace. If you are not in a workspace, skip this step.

1. Generate a local crate if the project you are building is not on crates.io:

   ```bash
   cargo package
   ```

1. Take the resulting crate and put it into the rpmbuild `SOURCES` dir.

1. grab all the deps. In the `SOURCES` dir:

   ```bash
   spectool -g <(rpmspec -P name.spec)
   ```

1. build the spec:

   ```bash
   rpmbuild -bs <SPEC_NAME_HERE.spec>
   ```

---

[Top of page](#building-rust-rpms)
