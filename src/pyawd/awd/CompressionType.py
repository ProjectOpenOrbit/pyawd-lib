from enum import Enum


class CompressionType(Enum):
    UNCOMPRESSED = 0
    ZLIB = 1
    LZMA = 2


def decode(num: int):
    if num == 1:
        return CompressionType.ZLIB
    elif num == 2:
        return CompressionType.LZMA
    else:
        return CompressionType.UNCOMPRESSED
