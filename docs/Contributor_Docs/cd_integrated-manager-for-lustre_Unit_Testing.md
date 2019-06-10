# Running Unit Tests for [integrated-manager-for-lustre](https://github.com/whamcloud/integrated-manager-for-lustre)

![Unit Testing](md_Graphics/test.png)

## Overview

The easiest way to get iml unit tests running locally is to start a postgres docker container with a volume that links to the IML repo. The unit tests can then be run inside the volume directory.

## Loading the docker container

### Initializing the docker container

In a local terminal, navigate to the IML repo and run the following:

```sh
docker run -dit --name unit-test -e POSTGRES_PASSWORD=lustre -v "$(pwd)":/root/iml postgres
```

### Setting up the docker container

Log into the docker container:

```sh
docker exec -it unit-test /bin/bash
```

Setting up the container:

```sh
apt-get update
apt-get install -y ed
apt-get install -y python-pip
cd ~/iml
pip install -r requirements.txt
pip install -r requirements.test
psql -c "CREATE USER chroma;" -U postgres
psql -c "ALTER USER chroma CREATEDB;" -U postgres
psql -c "CREATE DATABASE chroma OWNER chroma;" -U postgres
export IML_DISABLE_THREADS=1
echo "CRYPTO_FOLDER='./'" > local_settings.py
echo -e "/^DEBUG =/s/= .*$/= True/\nwq" | ed settings.py 2>/dev/null
```

## Run the Desired Unit Tests

All test commands should be run in the ~/iml directory.

### To Run all the tests under chroma_manager:

```sh
python -W always manage.py test tests/unit/
```

### Running a subset of tests

```sh
python -W always manage.py test tests/unit/chroma_core/models
```

### Running tests in a single file

```sh
python -W always manage.py test tests/unit/chroma_core/models/test_host.py
```

### Running a specific test

```sh
python -W always manage.py test tests/unit/chroma_core/models/test_host.py:TestHostListMixin:test_cached_hosts
```

[Top of page](#running-unit-tests-for-integrated-manager-for-lustre)
