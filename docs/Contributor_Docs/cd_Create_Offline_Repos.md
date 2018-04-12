# <a name="Top"></a>How to create offline repos for IML {{site.version}}

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![zfs](md_Graphics/installing_sm.jpg)

The following is a procedure for creating local repos using a CentOS 7 VM.

1. Check out a local copy of IML from github.

1. Copy the `storage_server.repo` to `etc.yum.repos.d`:

    ```
    cp ./intel-manager-for-lustre/chroma-manager/storage_server.repo  /etc/yum.repos.d/
    ```

1. Create a dir to hold local repos and cd to it:

    ```
    mkdir local_repos;
    cd local_repos
    ```

1. Run `reposync` for the repos we want to sync (You will see a few kmod-* repos fail, this is expected):

    ```
    sudo reposync -n --repoid=ngompa-dnf-el7 --repoid=e2fsprogs --repoid=managerforlustre-manager-for-lustre --repoid=lustre-client --repoid=lustre
    ```

1. (Optional) You may want to sync EPEL and or CentOS Extras as well if you don't have them where you are deploying to:

    ```
    sudo reposync -n --repoid=epel --repoid=extras
    ```

1. Use `createrepo` to create repomd (xml-rpm-metadata) repositories:

    ```
    sudo createrepo ./ngompa-dnf-el7/
    sudo createrepo ./e2fsprogs/
    sudo createrepo ./lustre -x '*kmod-spl*' -x '*kmod-zfs*'
    sudo createrepo ./lustre-client
    sudo createrepo ./managerforlustre-manager-for-lustre/
    ```

1. (Optional) use `createrepo` for EPEL and CentOS Extras if you ran `reposync` for them earlier:

    ```
    sudo createrepo ./epel
    sudo createrepo ./extras
    ```

1. Tar the resulting dir:

    ```
    tar -czvf ../local_repos.tar.gz ./
    ```

1. Take the IML tarball + the `local_repos.tar.gz` and move them onto the node planned for install.

1. Expand the IML tarball and the local_repos tarball. Once expanded, cd to the expanded IML dir and update the `chroma_support.repo` so that each `baseurl` points to its corresponding `local_repos` subdir.

1. Install the manager as usual. Do not deploy agents.

1. Once installed, move the local_repos subdirs into `/var/lib/chroma/repo`.

1. Update `/usr/share/chroma-manager/storage_server.repo` so that each repo `baseurl` points back to the url of the manager node, and ssl props are put in place. Example for `e2fsprogs`:

    ```
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

1. Deploy agents as usual.


---
[Top of page](#Top)