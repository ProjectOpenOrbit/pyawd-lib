from typing import IO

from pyawd.awd.types import Field


def decode(data: IO):
    return Field.decode_uint32(data)
