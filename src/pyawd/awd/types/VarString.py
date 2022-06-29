from typing import IO

from pyawd.PyAwdConfig import ENDIANNESS


def decode(raw_data: IO) -> str:
    len_of_str = int.from_bytes(raw_data.read(2), ENDIANNESS)
    str_value = raw_data.read(len_of_str).decode()
    return str_value
