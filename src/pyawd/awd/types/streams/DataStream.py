import io
import struct
from typing import IO

# 1 Vertex positions
# 2 Face indices
# 3 UV coordinates
# 4 Vertex normals
# 5 Vertex tangents
# 6 Joint index
# 7 Joint weight

# function table for decoding specific streams by type id
from pyawd.PyAwdLogger import logger
from pyawd.awd.types.streams import VertexPositionsStream, FaceIndexStream, UVCoordinatesStream

stream_decoders = {
    1: VertexPositionsStream.decode,
    2: FaceIndexStream.decode,
    3: UVCoordinatesStream.decode
}


def decode(data: IO):
    stream_type, content_data_type, stream_length = struct.unpack("<BBI", data.read(6))
    stream_data = io.BytesIO(data.read(stream_length))
    if stream_type not in stream_decoders:
        logger.debug(f"[?] Unimplemented Stream type: {stream_type}")
        return f"Unimplemented Stream type: {stream_type}", 6 + stream_length
    return stream_decoders[stream_type](stream_data, stream_length), 6 + stream_length
