from typing import IO

from pyawd.awd.types import VarString, NumAttrList, SubMesh, UserAttrList, Field


class TriangleGeometryBlock:
    def __init__(self, lookup_name, sub_geometry_count, geometry_properties, sub_meshes, user_attributes):
        self.lookup_name = lookup_name
        self.sub_geometry_count = sub_geometry_count
        self.geometry_properties = geometry_properties
        self.sub_meshes = sub_meshes
        self.user_attributes = user_attributes
        pass

    def __str__(self):
        return f"""===TriangleGeometry Block===
    LookupName: {self.lookup_name}
    SubGeometry Count: {self.sub_geometry_count}
    Geometry Properties: {self.geometry_properties}
    SubMeshes: { len(self.sub_meshes) }
    User Attributes: {self.user_attributes}"""


def decode(data: IO):
    lookup_name = VarString.decode(data)
    sub_geometry_count = Field.decode_uint16(data)
    geometry_properties, bytes_read = NumAttrList.decode(data)
    sub_meshes = []
    for _ in range(sub_geometry_count):
        sub_meshes.append(SubMesh.decode(data))
    user_attributes = UserAttrList.decode(data)[0]
    return TriangleGeometryBlock(lookup_name, sub_geometry_count, geometry_properties, sub_meshes, user_attributes)
