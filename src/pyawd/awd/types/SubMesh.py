from typing import IO

from pyawd.PyAwdConfig import ENDIANNESS
from pyawd.awd.types import NumAttrList, UserAttrList
from pyawd.awd.types.streams import DataStream


class SubMesh:
    def __init__(self, sub_mesh_properties, geometry_data_blocks, user_attributes):
        self.sub_mesh_properties = sub_mesh_properties
        self.geometry_data_blocks = geometry_data_blocks
        self.user_attributes = user_attributes

    def __str__(self):
        return f"""===SubMesh Block===
    SubMesh Properties: {self.sub_mesh_properties}
    Geometry Data Blocks: {self.geometry_data_blocks}
    User Attributes: {self.user_attributes}"""

    pass


def decode(data: IO):
    byte_count = int.from_bytes(data.read(4), ENDIANNESS)
    sub_mesh_properties, bytes_read = NumAttrList.decode(data)
    cur_bytes_read = bytes_read
    geometry_data_blocks = []
    while cur_bytes_read < byte_count:
        geometry_data, bytes_read = DataStream.decode(data)
        geometry_data_blocks.append(geometry_data)
        cur_bytes_read += bytes_read
    user_attributes = UserAttrList.decode(data)[0]
    return SubMesh(sub_mesh_properties, geometry_data_blocks, user_attributes)
