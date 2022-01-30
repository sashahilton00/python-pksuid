import time
from datetime import datetime

import pytest

from pksuid import BODY_LENGTH, PKSUID


def test_generation():
    pksuid = str(PKSUID('test'))
    # 4 character prefix, 1 character underscore, 27 character
    assert len(pksuid) == 32

    assert pksuid[4] == '_'

    # check lengths of each part are correct
    prefix, uid = str(pksuid).split('_')
    assert len(prefix) == 4
    assert len(uid) == 27


def test_get_timestamp():
    # we use a future timestamp to ensure default timestamp is not being used
    timestamp_now = int(time.time())
    timestamp_future = timestamp_now + 200

    pksuid = PKSUID('test', timestamp=timestamp_future)
    ts = pksuid.get_timestamp()

    assert ts == timestamp_future


def test_get_prefix():
    pksuid = PKSUID('test')

    assert pksuid.get_prefix() == 'test'


def test_get_datetime():
    # necessary to remove microseconds as these are not stored in the timestamp and thus the response would otherwise
    # not match
    dt_object = datetime.now()
    dt_object = dt_object.replace(microsecond=0)

    pksuid = PKSUID('test', timestamp=dt_object.timestamp())

    assert pksuid.get_datetime() == dt_object


def test_get_payload():
    pksuid = PKSUID('test')

    assert len(pksuid.get_payload()) == BODY_LENGTH


def test_parse_string():
    pksuid = PKSUID.parse('test_24OjYtVsP8hbCZ4difNIQmyUMf9')

    assert pksuid.get_timestamp() == 1643508577
    assert pksuid.get_prefix() == 'test'
    assert pksuid.get_datetime() == datetime(year=2022, month=1, day=30, hour=2, minute=9, second=37)
    assert pksuid.get_payload() == b'\x98\xec\xce\x1d\xf0\x9eok\x0cc\x18\xc9\xde\x0c%\x9f'


def test_parse_bytes():
    string_bytes = b'test_24OjYtVsP8hbCZ4difNIQmyUMf9'
    pksuid = PKSUID.parse_bytes(string_bytes)

    assert pksuid.get_timestamp() == 1643508577
    assert pksuid.get_prefix() == 'test'
    assert pksuid.get_datetime() == datetime(year=2022, month=1, day=30, hour=2, minute=9, second=37)
    assert pksuid.get_payload() == b'\x98\xec\xce\x1d\xf0\x9eok\x0cc\x18\xc9\xde\x0c%\x9f'


def test_get_bytes():
    pksuid = PKSUID.parse('test_24OjYtVsP8hbCZ4difNIQmyUMf9')

    assert pksuid.bytes() == b'test_24OjYtVsP8hbCZ4difNIQmyUMf9'


def test_invalid_characters():
    with pytest.raises(Exception):
        PKSUID.parse('sk_//24OjYtVsP8hbCZ4difNIQmyUMf9')


def test_invalid_ksuid_length():
    with pytest.raises(Exception):
        PKSUID.parse('sk_24OjYtVsP8hbCZ4difNIQmyUMf924')
