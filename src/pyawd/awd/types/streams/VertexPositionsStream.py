import struct
from typing import IO


class VertexPositionsStream:
    def __init__(self, vertices):
        self.vertices = vertices


def decode(data: IO, length: int):
    cnt = int(length / 12)
    vertices = []
    for _ in range(cnt):
        x, y, z = struct.unpack('fff', data.read(12))
        vertices.append([x, y, z])
    return VertexPositionsStream(vertices)
