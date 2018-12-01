# How to create offline repos for IML {{site.version}}

[**Online Help Table of Contents**](IML_Help_TOC.md)

The following is a procedure for creating local repos using a CentOS 7 VM.

1.  Install git and createrepo if they are not present:

    ```bash
    yum install -y git createrepo
    ```

1.  Check out a local copy of [IML from github](https://github.com/whamcloud/integrated-manager-for-lustre).

1.  Navigate to the IML project dir.

1.  Switch to the tag or branch you want to create offline repos for. For example, if building offline repos for IML 4.0.6:

    ```bash
    git checkout v4.0.6.0
    ```

1.  Copy the `storage_server.repo` to `etc.yum.repos.d`:

    ```bash
    cp ./chroma-manager/storage_server.repo  /etc/yum.repos.d/
    ```

1.  Create a dir to hold local repos and navigate to it:

    ```bash
    mkdir local_repos;
    cd local_repos
    ```

1.  Run `reposync` for the repos we want to sync (You will see a few kmod-\* repos fail, this is expected):

    ```bash
    reposync -n --repoid=ngompa-dnf-el7 --repoid=e2fsprogs --repoid=managerforlustre-manager-for-lustre --repoid=lustre-client --repoid=lustre
    ```

1.  (Optional) You may want to sync EPEL and or CentOS Extras as well if you don't have them where you are deploying to:

    ```bash
    reposync -n --repoid=epel --repoid=extras
    ```

1.  Use `createrepo` to create repomd (xml-rpm-metadata) repositories:

    ```bash
    createrepo ./ngompa-dnf-el7/
    createrepo ./e2fsprogs/
    createrepo ./lustre -x '*kmod-spl*' -x '*kmod-zfs*'
    createrepo ./lustre-client
    createrepo ./managerforlustre-manager-for-lustre/
    ```

1.  (Optional) use `createrepo` for EPEL and CentOS Extras if you ran `reposync` for them earlier:

    ```bash
    createrepo ./epel
    createrepo ./extras
    ```

1.  Navigate out of local_repos and tar the resulting dir:

    ```bash
    tar -czvf local_repos.tar.gz ./local_repos
    ```

1.  Take the IML tarball + the `local_repos.tar.gz` and move them onto the node planned for install.

1.  Expand the IML tarball and the local_repos tarball. Once expanded, cd to the expanded IML dir and update the `chroma_support.repo` so that each `baseurl` points to its corresponding `local_repos` subdir.

1.  Install the manager as usual. Do not deploy agents.

1.  Once installed, move the local_repos subdirs into `/var/lib/chroma/repo`.

1.  Update `/usr/share/chroma-manager/storage_server.repo` so that each repo `baseurl` points back to the url of the manager node, and ssl props are put in place. Example for `e2fsprogs`:

    ```bash
    [e2fsprogs]
    name=Lustre e2fsprogs
    baseurl=https://<MANAGER-URL-HERE>/repo/e2fsprogs/
    enabled=1
    gpgcheck=0
    sslverify = 1
    sslcacert = /var/lib/chroma/authority.crt
    sslclientkey = /var/lib/chroma/private.pem
    sslclientcert = /var/lib/chroma/self.crt
    proxy=_none_
    ```

1.  Deploy agents as usual.

---

[Top of page](#how-to-create-offline-repos-for-iml-{{site.version | remove: '.'}})
