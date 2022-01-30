from pksuid import PKSUID


def main():
    uid = PKSUID('eg')

    print(uid)
    print(uid.get_prefix())
    print(uid.get_timestamp())
    print(uid.get_datetime())
    print(uid.get_payload())

    uid_bytes = uid.bytes()

    uid_from_string = PKSUID.parse(str(uid))
    uid_from_bytes = PKSUID.parse_bytes(uid_bytes)

    print(uid_from_string.get_payload(), uid_from_bytes.get_payload(), '\n')

    uid_from_string = PKSUID.parse('eg_24OjYtVsP8hbCZ4difNIQmyUMf9')

    print(uid_from_string)
    print(uid_from_string.get_prefix())
    print(uid_from_string.get_timestamp())
    print(uid_from_string.get_datetime())
    print(uid_from_string.get_payload())


main()
