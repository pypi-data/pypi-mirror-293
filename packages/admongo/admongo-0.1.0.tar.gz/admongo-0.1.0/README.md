## About

This code automates MongoDB administrative tasks without knowledge of mongo shell language (JavaScript).

This repository contains scripts to automate adminstrative tasks on MongoDB.

* A Python module using PyMongo, the Python API for MongoDB. Detailed usage instructions can be found [here](docs/pymongo_admin.md).
* A bash script using the native JavaScript-based `mongo` client from the mongodb package.
  This interface is not further maintained and is deprecated.

## How to install

From the PyPI repository:
```
pip install admongo
```

From the Gitlab repository:
```
pip install git+https://gitlab.kit.edu/ivan.kondov/mongo-admin.git
```

## How to use

A short help can be obtained with the command:

```
mongo_admin --help
```

See the [detailed usage instructions](docs/pymongo_admin.md).
