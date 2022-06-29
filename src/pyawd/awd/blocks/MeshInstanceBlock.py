from typing import IO

from pyawd.awd.types import NumAttrList, UserAttrList, Field, SceneHeader, BlockAddr


class MeshInstanceBlock:
    def __init__(self, scene_header: SceneHeader, mesh_block_id, material_ids, properties, user_attributes):
        self.scene_header: SceneHeader = scene_header
        self.mesh_block_id = mesh_block_id
        self.material_ids = material_ids
        self.properties = properties
        self.user_attributes = user_attributes
        pass

    def __str__(self):
        return f"""===MeshInstance Block===
    scene_header: {self.scene_header}
    mesh_block_id: {self.mesh_block_id}
    material_ids: {self.material_ids}
    properties: {self.properties}
    user_attributes: {self.user_attributes}"""


def decode(data: IO):
    scene_header = SceneHeader.decode(data)
    mesh_data_block_id = BlockAddr.decode(data)
    num_of_materials = Field.decode_uint16(data)
    material_ids = []
    for _ in range(num_of_materials):
        material_ids.append(BlockAddr.decode(data))
    mesh_instance_properties = NumAttrList.decode(data)[0]
    user_attributes = UserAttrList.decode(data)[0]
    return MeshInstanceBlock(scene_header, mesh_data_block_id, material_ids, mesh_instance_properties, user_attributes)
