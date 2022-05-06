# Python-PKSUID

[![PyPI version fury.io](https://badge.fury.io/py/pksuid.svg)](https://pypi.python.org/pypi/pksuid/)

### (Prefixed K-Sortable Unique IDentifier)

This library provides an enhancement to the KSUID identifier
first proposed and used by Segment.io, whose reference implementation
exists here:

[https://github.com/segmentio/ksuid](https://github.com/segmentio/ksuid)

This library extends the KSUID specification as the `PKSUID` specification
with a prefix, inspired by the Stripe prefixed IDs, such as `txn_1032HU2eZvKYlo2CEPtcnUvl`.

This in turn makes it easy for developers to see at a glance the underlying type of the
resource that the identifier refers to, and makes for easier reading/tracing of resources
in various locations, such as log files.

## Installation

The package is available on PyPi, simply install with:

`pip install pksuid`

## Usage

This package is tested working with `Python 3.6+`

An example of how to use this library is as follows:

```python
from pksuid import PKSUID

# generate a new unique identifier with the prefix usr
uid = PKSUID('usr')

# returns 'usr_24OnhzwMpa4sh0NQmTmICTYuFaD'
print(uid)

# returns: usr
print(uid.get_prefix())

# returns: 1643510623
print(uid.get_timestamp())

# returns: 2022-01-30 02:43:43
print(uid.get_datetime())

# returns: b'\x81>*\xccDJT\xf1\xbe\xa9\xf3&\xe8\xa5\xb2\xc1'
print(uid.get_payload())

# convert from a str representation back to PKSUID
uid_from_string = PKSUID.parse('usr_24OnhzwMpa4sh0NQmTmICTYuFaD')

# this can now be used as usual
# returns: 1643510623
print(uid_from_string.get_timestamp())

# conversion to and parsing from bytes is also possible
uid_as_bytes = uid.bytes()
uid_from_bytes = PKSUID.parse_bytes(uid_as_bytes)

# returns: 2022-01-30 02:43:43
print(uid_from_bytes.get_datetime())

# all the standard comparison operators are available
import time
ts = int(time.time())

lesser_uid, greater_uid = PKSUID('usr', timestamp = ts), PKSUID('usr', timestamp=ts + 5)

# returns True
print(lesser_uid < greater_uid)

# except for the case of equivalence operators (eq, ne), the prefix is not taken into account when comparing
prefixed_uid_1, prefixed_uid_2 = PKSUID('diff', timestamp = ts), PKSUID('prefix', timestamp=ts + 5)

# returns True
print(prefixed_uid_1 < prefixed_uid_2)
```

## Testing

Run the unit tests with `poetry run pytest`.
