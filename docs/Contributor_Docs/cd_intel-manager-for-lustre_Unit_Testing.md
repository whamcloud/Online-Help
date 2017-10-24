#  <a name="Top"></a>Running Unit Tests for [intel-manager-for-lustre](https://github.com/intel-hpdd/intel-manager-for-lustre)

![Unit Testing](md_Graphics/test.png)

## Prerequisites
* To run the python unit tests for the [intel-manager-for-lustre](https://github.com/intel-hpdd/intel-manager-for-lustre) repo, it will be necessary to install a working version of IML.

* Create a **Vagrant** virtual cluster outlined here: [Install IML on a Vagrant Virtual Cluster](cd_Installing_IML_On_Vagrant.md).

## Log into the **adm** node
Change directory to the location of the Vagrantfile and become the root user.

    # vagrant ssh adm
    # sudo -i

## Install Necessary Tools
Install pip, virtualenv and other packages.

    # yum -y install python-pip systemd-devel libpqxx-devel graphviz-devel.x86_64

    # pip install -U pip psycopg2
    # pip install virtualenv

## Create a Virtual environment
This is an optional step if the desire is to build up the test area and then to eliminate the test area. Virtual environments are about isolation, and not polluting the system namespace. 

Activate the virtual environment where dependencies will be added.

    # virtualenv myenv
    # cd myenv
    
    # source bin/activate
    (myenv) # 

To **deactivate** the virtual environment, type "deactivate":

    (myenv) # deactivate
    #

## Clone the [intel-manager-for-lustre](https://github.com/intel-hpdd/intel-manager-for-lustre) code.

    # git clone git@github.com:intel-hpdd/intel-manager-for-lustre.git

## Or, copy the [intel-manager-for-lustre](https://github.com/intel-hpdd/intel-manager-for-lustre) code from the /vagrant shared drive:

    # cp -r /vagrant/intel-manager-for-lustre .

## Generate the list of Necessary Dependencies

    # cd intel-manager-for-lustre
    # make requirements

## Install the Necessary Dependencies

    # cd chroma-manager
    # pip install -r requirements.txt

**Note:** This may take a while to finish, i.e., tens of minutes. Be patient and allow the install to run to completion.

## Run the Desired Unit Tests

### To Run all the tests under chroma_manager:

    # python manage.py test tests/unit

### To Run a Subset of Tests, Specify the Correct Path

    # python manage.py test tests/unit/chroma_core/models

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

## If the Unit Tests are not Behaving

Evaluating database transactions will not work as expected if multiple threads are operating on the same database instance. 
To remedy this, disable threading for the manager unit tests.

    # export IML_DISABLE_THREADS=1

    Run the tests here.
    For example,

    # python manage.py test tests/unit

    # unset IML_DISABLE_THREADS

## Other tests

### Test 1

    # export IML_DISABLE_THREADS=1

    # mkdir -p /tmp/test_reports
    # export WORKSPACE=/tmp/myworkspace

    # python manage.py test --with-xunit --xunit-file=$WORKSPACE/test_reports/chroma-manager-unit-test-results.xml --with-coverage tests/unit/ <<EOC
    yes
    EOC

    # unset IML_DISABLE_THREADS

### Test 2

    # export IML_DISABLE_THREADS=1

    # mkdir -p /tmp/test_reports
    # export WORKSPACE=/tmp/myworkspace

    # python manage.py test --with-xunit --xunit-file=$WORKSPACE/test_reports/chroma-manager-unit-test-results.xml tests/unit/ <<EOC
    yes
    EOC

    # unset IML_DISABLE_THREADS

---
[Top of page](#Top)