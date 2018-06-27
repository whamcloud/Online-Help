# Installing IML on Vagrant

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![clustre](md_Graphics/installing_sm.jpg)

## Prerequisites

Please refer to [https://github.com/whamcloud/vagrantfiles](https://github.com/whamcloud/vagrantfiles) on how to create a virtual HPC storage cluster with vagrant before attempting to install IML.

1. Install Virtualbox and Vagrant

1. Verify that the following vagrant plugins are installed:

    ```bash
    vagrant plugin list

    vagrant plugin install vagrant-shell-commander
    vagrant plugin install vagrant-vbguest
    vagrant plugin install vagrant-proxyconf    <--- Optional, for example, this may be needed if behind corporate firewall.
    ```

1. Clone the Vagrantfiles repo from github

    ```bash
    git clone git@github.com:whamcloud/Vagrantfiles.git
    ```

1. navigate to the `Vagrantfiles/iml-sandbox` directory

1. Start the VM cluster

    ```bash
    vagrant up
    ```

## Installing IML

1. Login to the `adm` node

    ```bash
    vagrant ssh adm
    ```

1. Become the _root_ user

    ```bash
    su -
    ```

1. Install IML via `yum`

    ```bash
    yum-config-manager --add-repo=yum-config-manager --add-repo=https://raw.githubusercontent.com/whamcloud/integrated-manager-for-lustre/master/chroma_support.repo
    yum install -y python2-iml-manager
    ```

1. Run the setup command

    ```bash
    chroma-config setup admin lustre localhost
    ```

1. Test that a connection can be made to IML by going to the following link in your browser: [https://localhost:8443](https://localhost:8443)

## Adding Servers

You should now be able to see IML when navigating to [https://localhost:8443](https://localhost:8443). Click on the login link at the top right and log in as the admin user (password: lustre). Next, go to the server configuration page and add the following servers:

```bash
mds[1,2].local,oss[1,2].local
```

This will take some time (around 20 to 30 minutes) but all four servers should add successfully.

## Configuring Interfaces

Once all servers have been added, each server will need to know which interface should be assigned the lustre network. Navigate to each server detail page by clicking on the server link. Scroll to the bottom of the server detail page where you will see a list of network interfaces. Click on the `Configure` button and you will be given the option to change the network driver and the network for each interface.

The vagrant file indicates that the lustre network will run on 10.73.20.x. If `Lustre Network 0` is specified for a different IP address, you will need to change its interface to `Not Lustre Network` and update the network for 10.73.20.x to use `Lustre Network 0`. It is very important that Lustre Network 0 is specified on the correct interface; otherwise, creating a filesystem will fail. Make sure that all servers have been updated where appropriate.

## Setting up Power Control

[Follow these instructions to configure the Power Control.](cd_Setting_Up_Power_Control.md)

## Creating a Filesystem

To create a filesystem, simply navigate to `Configure->File Systems` and click the `Create` button. Make the following selections:

* Management Target / MGS -> mds1 (512 MB)
* Metadata Target / MDS -> mds2
* Object Storage Targets -> Select ALL OSS nodes

After the selections have been made, click the button to create the filesystem. If you have any issues creating the filesystem there is a good chance that the interface for 10.73.20.x is not assigned to Lustre Network 0. If this happens, stop the filesystem and update the interfaces accordingly.

## [Setting up Clients](cd_Setting_Up_Clients.md)

---

[Top of page](#Top)
