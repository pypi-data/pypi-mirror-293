# pyeilcd

[![PyPI](https://img.shields.io/pypi/v/pyeilcd.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pyeilcd)][pypi status]

[pypi status]: https://pypi.org/project/pyeilcd/

pyeilcd is a Python package that provides a simple interface to validate extended-ILCD (eILCD) XML files against the ILCD schemas based on the [pyilcd](https://github.com/brightway-lca/pyilcd) library.

## Installation

You can install _pyeilcd_ via [pip] from [PyPI]:

```console
$ pip install pyeilcd
```

## Usage

```python
from pyeilcd import validate_file_contact_dataset, Defaults

# Override defaults if needed, else skip. Defaults are already set.
Defaults.config_defaults("config.ini")  # Replace with your own config file

# Validate the ContactDataset class against the ContactDataset schema.
validate_file_contact_dataset("data/invalid/sample_contact_invalid.xml")  # Replace with your own XML file
>> data/contact/sample_contact_invalid.xml:17:0:ERROR:SCHEMASV:SCHEMAV_CVC_DATATYPE_VALID_1_2_1: Element '{http://lca.jrc.it/ILCD/Common}class', attribute 'level': 'a' is not a valid value of the atomic type '{http://lca.jrc.it/ILCD/Common}LevelType'. data/contact/sample_contact_invalid.xml:17:0:ERROR:SCHEMASV:SCHEMAV_CVC_IDC: Element '{http://lca.jrc.it/ILCD/Common}class', attribute 'level': Warning: No precomputed value available, the value was either invalid or something strange happened.
```


## License

Distributed under the terms of the GPL 3.0 license,
_pyeilcd_ is free and open source software.


[pip]: https://pip.pypa.io/en/stable/
[PyPI]: https://pypi.org/project/pyeilcd/
