# Using module-tools

IML is moving towards a service-oriented architecture.

As part of this, it's moving into repos that focus on a single area of responsibility.

These repos are generally hosted in [Copr](https://copr.fedorainfracloud.org/) in either our [prod](https://copr.fedorainfracloud.org/coprs/managerforlustre/manager-for-lustre/) or [devel](https://copr.fedorainfracloud.org/coprs/managerforlustre/manager-for-lustre-devel/) projects.

To accomodate this, we are currently using a meta repo [module-tools](https://github.com/whamcloud/module-tools), that seeks to abstract
common tasks when building / testing smaller repos.

## Tasks

### Running Builds from separate repos together

Sometimes we may want to test multiple changes together, where each change lives in a separate repo. To accomodate this workflow,
we currently need to build each RPM and indicate to the manager to use these repos in test. The following describes how to achieve this task.

1.  Sign up for a [Fedora account](https://admin.fedoraproject.org/accounts/user/new) if you don't have one and login to Copr.
1.  Get your api token info [here](https://copr.fedorainfracloud.org/api/), you will need this later.
1.  (Optional) Create a new project to hold your changes. If you don't do this `make copr_build` will create a project and build in it using the name of your project. Creating a new project by hand is useful if you want to batch multiple RPMs in a single repo.
1.  Once your project is created, navigate to the change you want to test locally.
1.  Create a `copr-local.mk` file at the top level of your project with `COPR_OWNER` and `COPR_PROJECT` set to your user and project created in step 3. Note that if you elected for module-tools to create the repo, you should omit `COPR_PROJECT`.
1.  (Optional) If you are running an OS that doesn't support copr-cli or make, start a docker container and mount the contents:

    ```shell
    docker run --privileged -dit -e "container=docker" --name=copr -v /sys/fs/cgroup:/sys/fs/cgroup -v "$(pwd)":"/build":rw centos:centos7 /usr/sbin/init
    ```

1.  Run the following commands (optionally inside docker if you performed the previous step):

    ```shell
    yum install -y epel-release
    yum install -y make copr-cli rpmdevtools git
    # create file at ~/.config/copr holding the contents from step 2.
    cd /build # if running in docker
    make DRYRUN=false copr_build # If building from spec
    # OR
    make DRYRUN=false UNPUBLISHED=true copr_build # If building from SRPM
    ```

1.  Check the builds in your Copr repo to make sure it was successful.
1.  Create a new PR in the [IML](https://github.com/whamcloud/integrated-manager-for-lustre) repo with the following pragma in the commit message:

    ```shell
    COPR Module: COPR_OWNER/COPR_PROJECT # can be specified more than once
    ```

    Where `COPR_OWNER` and `COPR_PROJECT` are the values specified in step 5.

1.  You should now see a build test run / with these substituted repos.
