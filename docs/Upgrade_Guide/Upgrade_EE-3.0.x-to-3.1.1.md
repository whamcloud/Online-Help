# Upgrading Intel® EE for Lustre 3.0.x to Intel® EE for Lustre 3.1.1

[**Upgrade Guide**](ug_TOC.md)

## Introduction

If you are on Intel® EE for Lustre 3.0.x or 3.1.0 you will first need to upgrade to Intel® EE for Lustre 3.1.1 before upgrading to Integrated Manager for Lustre {{site.version}}. This upgrade process does not require manual steps to be performed on the servers, but it does enforce a filesystem outage. The instructional video below describes the upgrade process.

<div style="margin: 0 auto; width: 640px;">
  <iframe src="https://player.vimeo.com/video/309949163" width="640" height="480" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
</div>

## Notes

After the updates complete on the server nodes, the manager will indicate that updates are still ready to be installed. You should be able to ignore this error. The upgrade can be verified by logging into the server node and running the following commands:

```bash
yum list installed | grep "lustre"
yum list installed | grep "chroma"
```

## Next Steps

[Upgrade to Integrated Manager for Lustre {{site.version}}](Upgrade_EE-3.1-el7_to_LU-LTS-el7.md)
