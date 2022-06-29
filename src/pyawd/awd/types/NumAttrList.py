from typing import IO, Tuple

from pyawd.PyAwdConfig import ENDIANNESS
from pyawd.awd.types import Field


def parse_numeric_attribute(data: IO):
    key = int.from_bytes(data.read(2), ENDIANNESS)
    val_len = int.from_bytes(data.read(4), ENDIANNESS)
    value = data.read(val_len)
    return [key, value]


def decode(data: IO) -> Tuple[dict, int]:
    list_len_in_bytes = Field.decode_uint32(data)

    byte_pointer = 0

    num_attr_list = {}
    while byte_pointer < list_len_in_bytes:
        (key, value) = parse_numeric_attribute(data)
        value = bytes(value)
        num_attr_list[key] = value
        # logger.debug(f"        AttributeList: {key} => {value}")
        byte_pointer += 6 + len(value)

    return num_attr_list, byte_pointer+4
