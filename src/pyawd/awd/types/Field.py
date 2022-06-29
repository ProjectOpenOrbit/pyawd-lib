import struct
from typing import IO

# 1 int8 Numeric
# 2 int16
# 3 int32
# 4 uint8
# 5 uint16
# 6 uint32
# 11 float32
# 12 float64
# 21 bool Derived numeric
#
# 22 color
# 23 BlockAddr
# 31 ConstString Array types
# 32 ByteArray
# 41 Vector2x1 Math types
# 42 Vector3x1
# 43 Vector4x1
# 51 Matrix3x2
# 52 Matrix3x3
# 53 Matrix4x3
# 54 Matrix4x4


def decode_int8(data: IO):
    return struct.unpack("<b", data.read(1))[0]


def decode_int16(data: IO):
    return struct.unpack("<h", data.read(2))[0]


def decode_int32(data: IO):
    return struct.unpack("<i", data.read(4))[0]


def decode_uint8(data: IO):
    return struct.unpack("<B", data.read(1))[0]


def decode_uint16(data: IO):
    return struct.unpack("<H", data.read(2))[0]


def decode_uint32(data: IO):
    return struct.unpack("<I", data.read(4))[0]


def decode_float32(data: IO):
    return struct.unpack("<f", data.read(4))[0]


def decode_float64(data: IO):
    return struct.unpack("<d", data.read(8))[0]


def decode_bool(data: IO):
    return struct.unpack("<?", data.read(1))[0]


decoders = {
    1:  decode_int8,
    2:  decode_int16,
    3:  decode_int32,
    4:  decode_uint8,
    5:  decode_uint16,
    6:  decode_uint32,
    11:  decode_float32,
    12:  decode_float64,
    21:  decode_bool
}


def decode(field_type, data: IO):
    if field_type not in decoders:
        raise RuntimeError(f"Cannot parse field type: {field_type}")
    return decoders[field_type](data)
