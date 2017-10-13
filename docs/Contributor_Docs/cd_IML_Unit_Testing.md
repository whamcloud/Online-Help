#  <a name="Top"></a>Running IML Unit Tests

![Unit Testing](md_Graphics/test.png)

## Prerequisites
* To run the python unit tests for IML, it will be necessary to install a working version of IML.
    * Create a **Vagrant** virtual cluster outined here: [Install IML on a Vagrant Virtual Cluster](cd_Installing_IML_On_Vagrant.md).

    * Create a Shared Mount from the guest machine to the vagrant virtual machine.
        * Follow these [Instructions](cd_Create_Vagrant_Mount.md)

## Log into the **adm** node
Change directory to the location of the Vagrantfile and become the root user.

    vagrant ssh adm
    su -

## Install Necessary Tools
Install the extra packages for enterprise linux, pip, git and virtualenv.

    yum --enablerepo=extras install epel-release -y
    yum install python-pip -y
    yum install git -y

    pip install virtualenv


## Install Extra Items
Add the systemd-devel package.

    yum install systemd-devel -y

Add the systemd python package

    yum install systemd-python -y

Add the python development package

    yum install python2-devel -y

Add the C++ client API for Postgress, libpqxx.

    yum list libpq*
    yum install libpqxx-devel -y

Add the graphviz package.

    yum install graphviz -y
    yum list available 'graphviz*'
    yum install graphviz-devel.x86_64 -y

## Create a Virtual environment
This is an optional step if the desire is to build up the test area and then to eliminate the test area.

Activate the virtual environment where dependencies will be added.

    virtualenv myenv
    cd myenv
    source bin/activate

## Clone the IML code.

    git clone git@github.com:intel-hpdd/intel-manager-for-lustre.git

## Or, copy IML code from the /vagrant shared drive:

    cp -r /vagrant/intel-manager-for-lustre .

## Generate the list of Necessary Dependencies

    cd intel-manager-for-lustre
    make requirements

## Install the Necessary Dependencies

    cd chroma-manager
    pip install -r requirements.txt

**Note:** This may take a while to finish, i.e., tens of minutes. Be patient and allow the install to run to completion.

## Run the Desired Unit Tests

### To Run all the tests under chroma_manager:

    python manage.py test tests/unit

### To Run a Subset of Tests, Specify the Correct Path

    python manage.py test tests/unit/chroma_core/models

```
(myenv) root@adm>python manage.py test tests/unit/chroma_core/models
nosetests tests/unit/chroma_core/models --logging-filter=-south --verbosity=1
Creating test database for alias 'default'...
Loaded 13 default power device types.
Creating groups...
***
***
***
*** SECURITY WARNING: You are running in DEBUG mode and default users have been created
***
***
***

..........................SS...S...
----------------------------------------------------------------------
Ran 35 tests in 28.240s

OK (SKIP=3)
Destroying test database for alias 'default'...
(myenv) root@adm>
```

---
[Top of page](#Top)