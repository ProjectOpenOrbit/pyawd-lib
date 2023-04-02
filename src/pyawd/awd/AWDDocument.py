import io
import lzma
import zlib
from io import BytesIO
from typing import IO

from pyawd.PyAwdLogger import logger
from pyawd.awd import AWDHeader, AWDBlock
from pyawd.awd.CompressionType import CompressionType


class AWDDocument:
    def __init__(self, header: AWDHeader, blocks: {}):
        self.header = header
        self.blocks = blocks

    pass


def decompress_body(data: IO, length: int, compression_type: CompressionType) -> tuple[BytesIO, int]:
    body = data.read(length)
    if compression_type == CompressionType.ZLIB:
        new_body = zlib.decompress(body)
    elif compression_type == CompressionType.LZMA:
        new_body = lzma.decompress(body)
    else:
        new_body = body
    return io.BytesIO(new_body), len(new_body)


def decode_body(data: IO):
    blocks = {}
    while True:
        body, header = AWDBlock.decode(data)
        if body is None:
            break
        logger.debug(body)
        blocks[header.block_id] = [header, body]
    return blocks


def decode(data: IO) -> AWDDocument:
    header = AWDHeader.decode(data)
    logger.debug(header)

    decompressed_body, body_len = decompress_body(data, header.body_length, header.compression_type)

    blocks = decode_body(decompressed_body)

    document = AWDDocument(header, blocks)

    return document
