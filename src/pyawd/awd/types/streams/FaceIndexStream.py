import struct
from typing import IO


class FaceIndexStream:
    def __init__(self, faces):
        self.faces = faces


# Face index data streams define triangles as triplets of index integers. The indices refer to vertices defined in
# the vertex stream, where index zero refers to the vertex defined by the first triplet in the vertex stream. An
# index i in the face index data stream refers to the vertex defined by the three subsequent floating point
# numbers starting at index 3i in the vertex stream
def decode(data: IO, length: int):
    faces = []
    i = 0
    while i < length:
        v1, v2, v3 = struct.unpack('HHH', data.read(6))
        faces.append([v1, v2, v3])
        i += 6
    return FaceIndexStream(faces)
