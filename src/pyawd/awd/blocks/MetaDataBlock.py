from datetime import datetime
from typing import IO
from pyawd.awd.types import NumAttrList


class MetaDataBlock:
    def __init__(self, dt_created, encoder_name, encoder_version, generator_name, generator_version):
        self.dt_created = dt_created
        self.encoder_name = encoder_name
        self.encoder_version = encoder_version
        self.generator_name = generator_name
        self.generator_version = generator_version

    def __str__(self):
        return f"""===Meta-Data Block===
    Unix Time: {datetime.fromtimestamp(self.dt_created)}
    Encoder: {self.encoder_name} v{self.encoder_version}
    Generator: {self.generator_name} v{self.generator_version}"""


def decode(data: IO):
    lst, bytes_read = NumAttrList.decode(data)
    # probably broken. I cannot get plausible values from sample files
    unix_time = int.from_bytes(lst[1], "little")
    encoder_name = bytes.decode(lst[2])
    encoder_version = bytes.decode(lst[3])

    generator_name = bytes.decode(lst[4])
    generator_version = bytes.decode(lst[5])

    return MetaDataBlock(unix_time, encoder_name, encoder_version, generator_name, generator_version)
