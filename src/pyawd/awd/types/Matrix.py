from typing import IO

from pyawd.awd.types import Field


def decode(data: IO, cols: int, rows: int):
    matrix = []
    for row in range(rows):
        next_col = []
        for col in range(cols):
            next_col.append(Field.decode_float32(data))
        matrix.append(next_col)
    return matrix
