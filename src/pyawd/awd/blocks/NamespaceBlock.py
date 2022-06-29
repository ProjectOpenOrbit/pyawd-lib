from typing import IO

from pyawd.PyAwdConfig import ENDIANNESS
from pyawd.awd.types import VarString


class NamespaceBlock:
    def __init__(self, handle, namespace_uri):
        self.handle = handle
        self.namespace_uri = namespace_uri

    def __str__(self):
        return f"""===Namespace Block===
    ID: {self.handle}
    URI: {self.namespace_uri}"""


def decode(data: IO):
    namespace_handle = int.from_bytes(data.read(1), ENDIANNESS)
    namespace_uri = VarString.decode(data)

    return NamespaceBlock(namespace_handle, namespace_uri)
