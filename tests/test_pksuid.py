import time
from datetime import datetime

import pytest

from pksuid import BODY_LENGTH, PKSUID, PKSUIDParseError, PKSUIDTimestampError


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

    assert pksuid.prefix == 'test'


def test_get_datetime():
    # necessary to remove microseconds as these are not stored in the timestamp and thus the response would otherwise
    # not match
    dt_object = datetime.now()
    dt_object = dt_object.replace(microsecond=0)

    pksuid = PKSUID('test', timestamp=dt_object.timestamp())

    assert pksuid.get_datetime() == dt_object


def test_get_payload():
    pksuid = PKSUID('test')

    assert len(pksuid.payload) == BODY_LENGTH


def test_parse_string():
    pksuid = PKSUID.parse('test_24OjYtVsP8hbCZ4difNIQmyUMf9')

    assert pksuid.get_timestamp() == 1643508577
    assert pksuid.prefix == 'test'
    assert pksuid.get_datetime() == datetime(year=2022, month=1, day=30, hour=2, minute=9, second=37)
    assert pksuid.payload == b'\x98\xec\xce\x1d\xf0\x9eok\x0cc\x18\xc9\xde\x0c%\x9f'


def test_parse_bytes():
    string_bytes = b'test_24OjYtVsP8hbCZ4difNIQmyUMf9'
    pksuid = PKSUID.parse_bytes(string_bytes)

    assert pksuid.get_timestamp() == 1643508577
    assert pksuid.prefix == 'test'
    assert pksuid.get_datetime() == datetime(year=2022, month=1, day=30, hour=2, minute=9, second=37)
    assert pksuid.payload == b'\x98\xec\xce\x1d\xf0\x9eok\x0cc\x18\xc9\xde\x0c%\x9f'


def test_get_bytes():
    pksuid = PKSUID.parse('test_24OjYtVsP8hbCZ4difNIQmyUMf9')

    assert pksuid.bytes() == b'test_24OjYtVsP8hbCZ4difNIQmyUMf9'


def test_invalid_characters():
    with pytest.raises(PKSUIDParseError):
        PKSUID.parse('sk_//24OjYtVsP8hbCZ4difNIQmyUMf9')


def test_invalid_ksuid_length():
    with pytest.raises(PKSUIDParseError):
        PKSUID.parse('sk_24OjYtVsP8hbCZ4difNIQmyUMf924')


def test_epoch_loop_exception():
    # this raises an exception as function expects a timestamp that has been created after 13 May 2014.
    # (ie. >= 1400000000)
    with pytest.raises(PKSUIDTimestampError):
        PKSUID('test', timestamp=0)


def test_timestamp_epoch_interstitial_exception():
    with pytest.raises(PKSUIDTimestampError):
        # the timestamp here is 1 second after the last available UNIX timestamp, which should raise an error when
        # attempting to convert back to a UNIX timestamp
        invalid_pksuid = PKSUID('test', timestamp=2147483648)
        invalid_pksuid.get_timestamp()


def test_comparison():
    ts = int(time.time())
    pksuid_1, pksuid_2 = PKSUID('test', timestamp=ts), PKSUID('test', timestamp=ts + 5)

    assert pksuid_1 < pksuid_2
    assert (pksuid_1 > pksuid_2) is False
    assert (pksuid_1 == pksuid_2) is False
    assert pksuid_1 != pksuid_2
    assert pksuid_1 <= pksuid_1
    assert pksuid_1 >= pksuid_1

    pksuid_3, pksuid_4 = PKSUID('abc', timestamp=ts), PKSUID('def', timestamp=ts + 5)

    assert pksuid_3 < pksuid_4
    assert (pksuid_3 >= pksuid_4) is False

def test_eq_false_incompatible_type():
    not_a_pksuid = Exception('testing')
    pksuid = PKSUID('test')

    # should return False due to not being able to parse exception to pksuid
    assert not pksuid == not_a_pksuid
    assert pksuid != not_a_pksuid
