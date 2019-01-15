# Available Jenkins Pragmas

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

## Overview

There are pragmas available for Jenkins (EFS, SSI, Upgrade) testing that wil effect the test run.

### Using an additional repo on the agent

`COPR Module: owner/project`

This will add the given copr repo to each agent node during testing. The pragma is additive, it will not overwrite the default agent repos.

### Overwriting Environment vars

This will overwrite the passed environment variables in a test script. It is typically used to run a subset of testing. Here's and example to run a single SSI test.

```
Environment: NOSE_ARGS=-x TESTS=tests/integration/shared_storage_configuration/test_managed_filesystem_with_failover.py:TestManagedFilesystemWithFailover.test_create_filesystem_with_failover_mds'
```

---

[Top of page](#available-jenkins-pragmas)
