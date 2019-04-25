# How to create offline repos for IML {{site.version}}

[**Software Installation Guide Table of Contents**](ig_TOC.md)

The following is a procedure for creating local repos using a CentOS 7 VM or container.

1. Install `createrepo` and `yum-plugin-copr` if they are not present:

   ```sh
   yum install -y createrepo yum-plugin-copr
   ```

1. Add upstream repos needed for IML to you work node:

   ```sh
   yum copr enable -y managerforlustre/manager-for-lustre
   yum-config-manager --add-repo https://downloads.whamcloud.com/public/lustre/lustre-{{site.lustre_version}}/el7/client/
   yum-config-manager --add-repo https://downloads.whamcloud.com/public/lustre/lustre-{{site.lustre_version}}/el7/server/
   yum-config-manager --add-repo https://downloads.whamcloud.com/public/e2fsprogs/latest/el7/
   ```

1. Create a dir to hold local repos and navigate to it:

   ```sh
   mkdir local_repos;
   cd local_repos
   ```

1. Run `reposync` for the repos we want to sync:

   ```sh
   reposync -n --repoid=downloads.whamcloud.com_public_e2fsprogs_latest_el7_  \
   --repoid=managerforlustre-manager-for-lustre \
   --repoid=downloads.whamcloud.com_public_lustre_lustre-2.12.0_el7_client_ \
   --repoid=downloads.whamcloud.com_public_lustre_lustre-2.12.0_el7_server_
   ```

1. (Optional) You may want to sync EPEL and or CentOS Extras as well if you don't have them where you are deploying to. Make sure you are syncing versions that match your OS, you may need to use the CentOS vault for this.

   ```sh
   reposync -n --repoid=epel --repoid=extras
   ```

1. Use `createrepo` to create repomd (xml-rpm-metadata) repositories:

   ```sh
   createrepo ./downloads.whamcloud.com_public_e2fsprogs_latest_el7_
   createrepo ./downloads.whamcloud.com_public_lustre_lustre-2.12.0_el7_server_
   createrepo ./downloads.whamcloud.com_public_lustre_lustre-2.12.0_el7_client_
   createrepo ./managerforlustre-manager-for-lustre/
   ```

1. (Optional) use `createrepo` for EPEL and CentOS Extras if you ran `reposync` for them earlier:

   ```sh
   createrepo ./epel
   createrepo ./extras
   ```

1. Navigate out of local_repos and tar the resulting dir:

   ```sh
   tar -czvf local_repos.tar.gz ./local_repos
   ```

1. Take the `local_repos.tar.gz` and move it to the manager node.

1. Fetch the IML manager install repo as described in [The install guide](ig_ch_05_install.md#installing-integrated-manager-for-lustre-software). Do not install yet.

1. Expand the local_repos tarball. Update the `chroma_support.repo` so that each `baseurl` points to its corresponding `local_repos` subdir.

1. Install the manager as usual. Do not deploy agents.

1. Once installed, move the local_repos subdirs into `/var/lib/chroma/repo`.

1. Update `/usr/share/chroma-manager/base.repo`, `/usr/share/chroma-manager/lustre-server.repo`, and `/usr/share/chroma-manager/lustre-client.repo` so that each `baseurl` points back to the url of the manager node, and ssl props are put in place. Example for `e2fsprogs`:

   ```text
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

[Top of page](#how-to-create-offline-repos-for-iml-{{site.version | remove: '.'}})
