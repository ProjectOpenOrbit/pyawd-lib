import io
from typing import IO

from pyawd.PyAwdConfig import ENDIANNESS
from pyawd.PyAwdLogger import logger
from .blocks import BLOCK_DATA_TYPES, TriangleGeometryBlock, MeshInstanceBlock, MetaDataBlock, NamespaceBlock


class AwdBlockHeader:
    def __init__(self, block_id, namespace, data_type, flags, size):
        self.block_id: int = block_id
        self.namespace: int = namespace
        self.data_type: int = data_type

        self.flags: int = flags
        self.flag_msp: bool = False
        self.flag_gsp: bool = False
        self.flag_psp: bool = False
        self.flag_compressed: bool = False
        self.flag_lzma: bool = False

        self.size = size
        self.process()

    def process(self):
        self.flag_msp = bool(self.flags & 0b00001)
        self.flag_gsp = bool(self.flags & 0b00010)
        self.flag_psp = bool(self.flags & 0b00100)
        self.flag_compressed = bool(self.flags & 0b01000)
        self.flag_lzma = bool(self.flags & 0b10000)
        pass

    def __str__(self):
        ret = f""" Block #{self.block_id}
    Size: {self.size}
    Namespace: {self.namespace}
    Data Type: {BLOCK_DATA_TYPES[self.data_type]}
    Flags:
        Storage precision:
            Matrix: {self.flag_msp}
            Geometry: {self.flag_gsp}
            Properties: {self.flag_psp}
        Compression:
            Compressed: {self.flag_compressed}
            LZMA: {self.flag_lzma}"""
        return ret


# Map of functions to decode respective blocks by ID
decoders = {
    1: TriangleGeometryBlock.decode,
    23: MeshInstanceBlock.decode,
    254: NamespaceBlock.decode,
    255: MetaDataBlock.decode
}


def decode_body(header, block):
    if header.data_type not in decoders:
        return "[!] WARNING: Unknown block type: {} - {}".format(header.data_type, BLOCK_DATA_TYPES[header.data_type])
    return decoders[header.data_type](io.BytesIO(block))


def decode(data: IO):
    block_id = int.from_bytes(data.read(4), ENDIANNESS)
    if block_id == 0:
        logger.debug("no more blocks...")
        return None, None

    logger.debug(f"\nBLOCK ID: {block_id}")
    namespace = int.from_bytes(data.read(1), ENDIANNESS)
    data_type = int.from_bytes(data.read(1), ENDIANNESS)
    flags = int.from_bytes(data.read(1), ENDIANNESS)
    size = int.from_bytes(data.read(4), ENDIANNESS)
    raw_data = data.read(size)

    header = AwdBlockHeader(block_id, namespace, data_type, flags, size)

    return decode_body(header, raw_data), header
