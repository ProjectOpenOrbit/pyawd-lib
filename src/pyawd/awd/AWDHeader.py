from typing import IO

from pyawd.PyAwdConfig import ENDIANNESS
from pyawd.awd import CompressionType
from pyawd.awd.types import Field

AWD_MAGIC_STRING = "AWD"


class AWDDocumentFlags:
    def __init__(self,
                 streaming,
                 matrix_storage_precision,
                 geometry_storage_precision,
                 properties_precision,
                 precision_per_block):
        self.streaming = streaming
        self.matrix_storage_precision = matrix_storage_precision
        self.geometry_storage_precision = geometry_storage_precision
        self.properties_precision = properties_precision
        self.precision_per_block = precision_per_block

    def __str__(self):
        ret = f"""        Streaming: {"yes" if self.streaming else "no"}
        Storage precision: {"enabled" if self.precision_per_block else "disabled"}"""
        if self.precision_per_block:
            ret += f"""
            MatrixSP: {self.matrix_storage_precision}
            GeometrySP: {self.geometry_storage_precision}
            PropertiesSP: {self.properties_precision}"""
        return ret
    pass


class AWDHeader:
    def __init__(self, magic_string, version_major, version_minor, document_flags, compression_type, body_length):
        self.magic_string = magic_string
        self.version_major = version_major
        self.version_minor = version_minor
        self.document_flags = document_flags
        self.compression_type = compression_type
        self.body_length = body_length

    def __str__(self):
        return f"""===AWDHeader===
    Magic string: {self.magic_string}
    Version: {self.version_major}.{self.version_minor}
    Flags:
{self.document_flags}
    Compression: {self.compression_type}
    (Compressed) body length: {self.body_length}"""

    pass


def decode_magic_string(data: IO) -> str:
    magic_string = data.read(3).decode()
    if magic_string != AWD_MAGIC_STRING:
        raise RuntimeError(f"Magic string invalid. Should be '{AWD_MAGIC_STRING}', is {magic_string}")
    return magic_string


def decode_version(data: IO):
    ver_major = Field.decode_uint8(data)
    ver_minor = Field.decode_uint8(data)
    return [ver_major, ver_minor]


def decode_document_flags(data: IO):
    flags = Field.decode_uint16(data)

    streaming = bool(flags & 0b00001)
    matrix_storage_precision = bool(flags & 0b00010)
    geometry_storage_precision = bool(flags & 0b00100)
    properties_storage_precision = bool(flags & 0b01000)
    precision_per_block = bool(flags & 0b10000)

    return AWDDocumentFlags(streaming,
                            matrix_storage_precision,
                            geometry_storage_precision,
                            properties_storage_precision,
                            precision_per_block)


def decode_compression_type(data: IO) -> CompressionType:
    compression_type = CompressionType.decode(int.from_bytes(data.read(1), ENDIANNESS))
    return compression_type
    pass


def decode_body_length(data: IO) -> int:
    body_len = Field.decode_uint32(data)
    return body_len


def decode(data: IO) -> AWDHeader:
    magic_string = decode_magic_string(data)
    version_major, version_minor = decode_version(data)
    document_flags = decode_document_flags(data)
    compression_type = decode_compression_type(data)
    body_length = decode_body_length(data)

    return AWDHeader(magic_string, version_major, version_minor, document_flags, compression_type, body_length)
