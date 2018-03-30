# Debugging a Running Nodejs Process In Vagrant

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

There are some cases where you'd like to debug a running nodejs process
running on a vagrant node.

This guide will walk through that process.

1.  Install `node-inspector` on the vagrant node.

    ```bash
    npm i -g node-inspector
    ```

1.  Put the process into debug mode by sending a `USR1` signal:

    ```bash
    systemctl kill -s SIGUSR1 SERVICE_NAME_HERE
    ```

1.  start `node-inspector`:

    ```bash
    node-inspector
    ```

1.  On the host, connect to `node-inspector` using the ip address the vagrant node is running on (likely 0.0.0.0) and the port node-inspector has started on (likely 8080) using chrome.

1.  This should load the app in an old version of devtools and will halt the code at first execution.
