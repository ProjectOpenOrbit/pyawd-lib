from typing import IO, Tuple

from pyawd.PyAwdConfig import ENDIANNESS
from pyawd.awd.types import VarString, Field


class UserAttribute:
    def __init__(self, namespace, key, value):
        self.namespace = namespace
        self.key = key
        self.value = value
        pass


def parse_user_attribute(data: IO):
    namespace = int.from_bytes(data.read(1), ENDIANNESS)
    key = VarString.decode(data)
    field_type = int.from_bytes(data.read(1), ENDIANNESS)
    field_len = int.from_bytes(data.read(4), ENDIANNESS)
    raw_data = data.read(field_len)
    value = Field.decode(field_type, raw_data)
    return UserAttribute(namespace, key, value)


def decode(data: IO) -> Tuple[dict, int]:
    list_len_in_bytes = int.from_bytes(data.read(4), ENDIANNESS)

    byte_pointer = 0

    user_attr_list = {}
    while byte_pointer < list_len_in_bytes:
        (key, value) = parse_user_attribute(data)
        value = bytes(value)
        user_attr_list[key] = value
        byte_pointer += 6 + len(value)

    return user_attr_list, byte_pointer + 4
