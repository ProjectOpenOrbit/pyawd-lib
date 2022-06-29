import struct
from typing import IO


class UVCoordinatesStream:
    def __init__(self, coordinates):
        self.coordinates = coordinates


def decode(data: IO, length: int):
    coords = []
    i = 0
    while i < length:
        x, y = struct.unpack("ff", data.read(8))
        coords.append([x, y])
        i += 8
    return UVCoordinatesStream(coords)
