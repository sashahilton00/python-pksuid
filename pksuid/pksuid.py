import datetime
import os
import time

import base62

# Used instead of zero(January 1, 1970), so that the lifespan of pksuids
# will be considerably longer. Epoch starts on May 13th, 2014.
# See: https://github.com/segmentio/ksuid#how-do-ksuids-work
EPOCH_TIME = 1400000000

TIME_STAMP_LENGTH = 4  # number of bytes storing the timestamp
BODY_LENGTH = 16  # Number of bytes consisting of the UUID


class PKSUID:
    __prefix: str = None
    __uid: bytes = None
    """ The primary classes that encompasses pksuid functionality.
    When given optional timestamp argument, the pksuid will be generated
    with the given timestamp. Otherwise the current time is used.
    """

    def __init__(self, prefix, timestamp=None):
        payload = os.urandom(BODY_LENGTH)  # generates a random 16 byte payload
        if timestamp is None:
            current_time = int(time.time())
        else:
            current_time = timestamp

        if int(time.time()) >= EPOCH_TIME > current_time:
            # the unix epoch has looped, which would otherwise trigger an overflow. This will need to be handled
            #   by conversion a new timestamp standard that has yet to be determined.
            # For now, we throw an exception.
            raise Exception('the UNIX epoch has looped, an updated timestamp mechanism has yet to be implemented.')

        byte_encoding = int(current_time - EPOCH_TIME).to_bytes(4, "big")

        self.__prefix = prefix
        self.__uid = b''.join([byte_encoding, payload])

    def get_datetime(self):
        """
        getDatetime() returns a python date object which represents the approximate time (missing microseconds)
        that the pksuid was created
        """

        unix_time = self.get_timestamp()
        return datetime.datetime.fromtimestamp(unix_time)

    def get_timestamp(self):
        """
        Returns the value of the timestamp, as a unix timestamp
        """

        unix_time = int.from_bytes(self.__uid[:TIME_STAMP_LENGTH], 'big')

        if unix_time + EPOCH_TIME > 9999999999:
            # this occurs in the time between the end of the UNIX epoch nd the end of the extended epoch.
            # an alternative timestamp representation would need to be implemented at a later date.
            raise Exception('the UNIX epoch has looped, an updated timestamp mechanism has yet to be implemented.')

        return unix_time + EPOCH_TIME

    # Returns the payload without the unix timestamp
    def get_payload(self):
        """
        Returns the value of the payload, with the timestamp encoded portion removed
        Returns:
             list : An array of integers, that represent the bytes used to encode the UID
        """

        return self.__uid[TIME_STAMP_LENGTH:]

    def get_prefix(self):
        """
        Returns the value of the prefix as a str.
        """
        return self.__prefix

    def bytes(self):
        """
        Returns the PKSUID as raw bytes
        """
        return bytes('{}_{}'.format(self.__prefix, base62.encodebytes(self.__uid)), 'utf-8')

    @staticmethod
    def parse(value):
        try:
            prefix, b62_uid = value.split('_')
            uid = base62.decodebytes(b62_uid)
        except ValueError:
            raise Exception('value does not appear to be a valid PKSUID')

        if len(uid) != TIME_STAMP_LENGTH + BODY_LENGTH:
            raise Exception("the provided value has an incorrect UID length")

        res = PKSUID(prefix)
        res.__uid = uid

        return res

    @staticmethod
    def parse_bytes(value):
        """
        Initializes PKSUID from bytes
        """
        return PKSUID.parse(value.decode('utf-8'))

    def __str__(self):
        return str(self.bytes().decode('utf-8'))
