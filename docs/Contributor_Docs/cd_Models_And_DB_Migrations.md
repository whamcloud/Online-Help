# <a name="Top"></a>Models and Database Migrations

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![Models and Database Migrations](md_Graphics/gears_sm.jpg)

## Overview:

Models exist in the chroma-manager/chroma_core/models/ directory. Once a model is created, a database migration file must be generated such that the tables reflecting the model will be created in the database. The procedure below shows how to create a migration file for *rsyslog* as an example, but the steps are the same for all models.

1. import the model into chroma-manager/chroma_core/models/\_\_init\_\_.py
```
from rsyslog import *
```
1. Run the schema migration from the `chroma-manager` directory.
```
./manage.py schemamigration chroma_core --auto
```

This will create the migration file. Optionally, this migration may be applied by running the following in the `chroma-manager` directory:

```
./manage.py migrate
```

---
[Top of page](#Top)