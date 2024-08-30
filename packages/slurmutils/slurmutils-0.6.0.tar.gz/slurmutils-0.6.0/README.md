# slurmutils

![PyPI - Version](https://img.shields.io/pypi/v/slurmutils)
![PyPI - Downloads](https://img.shields.io/pypi/dm/slurmutils)
![GitHub License](https://img.shields.io/github/license/charmed-hpc/slurmutils)
[![Matrix](https://img.shields.io/matrix/ubuntu-hpc%3Amatrix.org?logo=matrix&label=ubuntu-hpc)](https://matrix.to/#/#hpc:ubuntu.com)

Utilities and APIs for interfacing with the Slurm workload manager.

slurmutils is a collection of various utilities that make it easier 
for you and your friends to interface with the Slurm workload manager, especially if you 
are orchestrating deployments of new and current Slurm clusters. Gone are the days of
seething over incomplete Jinja2 templates. Current utilities shipped in the 
slurmutils package include:

#### `from slurmutils.editors import ...`

* `slurmconfig`: An editor for _slurm.conf_ configuration files.
* `slurmdbdconfig`: An editor for _slurmdbd.conf_ configuration files.

For more information on how to use or contribute to slurmutils, 
check out the [Getting Started](#-getting-started) and [Development](#-development) 
sections below 👇

## ✨ Getting Started

### Installation

#### Option 1: Install from PyPI

```shell
$ python3 -m pip install slurmutils
```

#### Option 2: Install from source

We use the [Poetry](https://python-poetry.org) packaging and dependency manager to
manage this project. It must be installed on your system if installing slurmutils
from source.

```shell
$ git clone https://github.com/canonical/slurmutils.git
$ cd slurmutils
$ poetry install
```

### Usage

#### Editors

##### `slurmconfig`

This module provides an API for editing both _slurm.conf_ and _Include_ files,
and can create new configuration files if they do not exist. Here's some common Slurm
lifecycle management operators you can perform using this editor:

###### Edit a pre-existing _slurm.conf_ configuration file

```python
from slurmutils.editors import slurmconfig

# Open, edit, and save the slurm.conf file located at _/etc/slurm/slurm.conf_.
with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
    del config.inactive_limit
    config.max_job_count = 20000
    config.proctrack_type = "proctrack/linuxproc"
```

###### Add a new node to the _slurm.conf_ file

```python
from slurmutils.editors import slurmconfig
from slurmutils.models import Node

with slurmconfig.edit("/etc/slurm/slurm.conf") as config:
    node = Node(
        NodeName="batch-[0-25]", 
        NodeAddr="12.34.56.78", 
        CPUs=1, 
        RealMemory=1000, 
        TmpDisk=10000,
    )
    config.nodes.update(node.dict())
```

##### `slurmdbdconfig`

This module provides and API for editing _slurmdbd.conf_ files, and can create new
_slurmdbd.conf_ files if they do not exist. Here's some operations you can perform
on the _slurmdbd.conf_ file using this editor:

###### Edit a pre-existing _slurmdbd.conf_ configuration file

```python
from slurmutils.editors import slurmdbdconfig

with slurmdbdconfig.edit("/etc/slurm/slurmdbd.conf") as config:
    config.archive_usage = "yes"
    config.log_file = "/var/spool/slurmdbd.log"
    config.debug_flags = ["DB_EVENT", "DB_JOB", "DB_USAGE"]
    del config.auth_alt_types
    del config.auth_alt_parameters
```

## 🤔 What's next?

If you want to learn more about all the things you can do with slurmutils, 
here are some further resources for you to explore:

* [Open an issue](https://github.com/charmed-hpc/slurmutils/issues/new?title=ISSUE+TITLE&body=*Please+describe+your+issue*)
* [Ask a question on Github](https://github.com/orgs/charmed-hpc/discussions/categories/q-a)

## 🛠️ Development

This project uses [tox](https://tox.wiki) as its command runner, which provides 
some useful commands that will help you while hacking on slurmutils:

```shell
tox run -e fmt   # Apply formatting standards to code.
tox run -e lint  # Check code against coding style standards.
tox run -e unit  # Run unit tests.
```

If you're interested in contributing your work to slurmutils, 
take a look at our [contributing guidelines](./CONTRIBUTING.md) for further details.

## 🤝 Project and community

slurmutils is a project of the [Ubuntu High-Performance Computing community](https://ubuntu.com/community/governance/teams/hpc).
Interested in contributing bug fixes, new editors, documentation, or feedback? Want to join the Ubuntu HPC community? You’ve come to the right place 🤩

Here’s some links to help you get started with joining the community:

* [Ubuntu Code of Conduct](https://ubuntu.com/community/ethos/code-of-conduct)
* [Contributing guidelines](./CONTRIBUTING.md)
* [Join the conversation on Matrix](https://matrix.to/#/#hpc:ubuntu.com)
* [Get the latest news on Discourse](https://discourse.ubuntu.com/c/hpc/151)
* [Ask and answer questions on GitHub](https://github.com/orgs/charmed-hpc/discussions/categories/q-a)

## 📋 License

slurmutils is free software, distributed under the GNU Lesser General Public License, v3.0.
See the [LGPL-3.0 LICENSE](./LICENSE) file for further details.
