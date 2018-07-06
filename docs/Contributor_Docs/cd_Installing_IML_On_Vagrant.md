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

You should now be able to see IML when navigating to [https://localhost:8443](https://localhost:8443). Click on the login link at the top right and log in as the admin user (password: lustre). After logging in, go to the servers page by selecting the following:

> Configuratin -> Servers

Click the `Add Servers` button and enter the following pdsh expression:

```bash
mds[1,2].local,oss[1,2].local
```

Click the `Next` button and all servers will be verified for installation. After verifying all servers, proceed to the profile selection screen. Select the appropriate profile based on the setup type:

{% include profile-list.md %}

Finally, select the `Proceed` button and the servers will be configured based upon the selected profile.

## Configuring Interfaces

Once all servers have been added, each server will need to know which interface should be assigned the lustre network. This can be done manually or automated by a provisioning script. Select one of the methods below.

### 1. Manually Configure Interfaces

On the servers page, navigate to each server's detail page by clicking on the server link. Scroll to the bottom of the server detail page where you will see a list of network interfaces. Click on the `Configure` button and you will be given the option to change the network driver and the network for each interface.

The vagrant file indicates that the lustre network will run on 10.73.20.x. If `Lustre Network 0` is specified for a different IP address, you will need to change its interface to `Not Lustre Network` and update the network for 10.73.20.x to use `Lustre Network 0`. It is very important that Lustre Network 0 is specified on the correct interface; otherwise, creating a filesystem will fail. Make sure that all servers have been updated where appropriate.

### 2. Automatically Configure Interfaces with Provisioning Script

The interfaces can be configured automatically by running the following script:

```bash
 vagrant provision mds1 mds2 oss1 oss2 --provision-with configure-lustre-network
```

---

[Top of page](#installing-iml-on-vagrant)
