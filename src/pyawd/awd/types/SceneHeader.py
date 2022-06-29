from typing import IO

from pyawd.awd.types import BlockAddr, VarString, Matrix4x3


class AWDSceneHeader:
    def __init__(self, parent_id, transform, lookup_name):
        self.parent_id = parent_id
        self.transform = transform
        self.lookup_name = lookup_name

    def __str__(self):
        return f"""===AWDSceneHeader===
    Parent ID: {self.parent_id}
    Transform: {self.transform}
    LookupName: {self.lookup_name}"""


def decode(data: IO):
    parent_id = BlockAddr.decode(data)
    transform = Matrix4x3.decode(data)
    lookup_name = VarString.decode(data)
    return AWDSceneHeader(parent_id, transform, lookup_name)
