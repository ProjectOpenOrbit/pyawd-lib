import os
import struct
import sys

from pyawd.PyAwdLogger import logger
from pyawd.awd import AWDDocument

# 1 int8 Numeric
# 2 int16
# 3 int32
# 4 uint8
# 5 uint16
# 6 uint32
# 11 float32
# 12 float64
# 21 bool Derived numeric
# 22 color
# 23 BlockAddr
# 31 ConstString Array types
# 32 ByteArray
# 41 Vector2x1 Math types
# 42 Vector3x1
# 43 Vector4x1
# 51 Matrix3x2
# 52 Matrix3x3
# 53 Matrix4x3
# 54 Matrix4x4
from pyawd.awd.blocks.MeshInstanceBlock import MeshInstanceBlock
from pyawd.awd.blocks.TriangleGeometryBlock import TriangleGeometryBlock
from pyawd.awd.types.streams.FaceIndexStream import FaceIndexStream
from pyawd.awd.types.streams.UVCoordinatesStream import UVCoordinatesStream
from pyawd.awd.types.streams.VertexPositionsStream import VertexPositionsStream

f_offset = 1


def build_obj(block):
    ret = ""
    cnt = 0
    global f_offset
    for mesh in block.sub_meshes:
        for geo in mesh.geometry_data_blocks:
            if isinstance(geo, VertexPositionsStream):
                for vertex in geo.vertices:
                    ret += f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"
                    cnt += 1
            elif isinstance(geo, FaceIndexStream):
                for face in geo.faces:
                    ret += f"f {face[0] + f_offset}/{face[0] + f_offset} {face[1] + f_offset}/{face[1] + f_offset} {face[2] + f_offset}/{face[2] + f_offset}\n"
            elif isinstance(geo, UVCoordinatesStream):
                for coordinate in geo.coordinates:
                    ret += f"vt {coordinate[0]} {1.0 - coordinate[1]}\n"
    f_offset += cnt
    return ret


def convert_to_obj(path_to_input_file, path_to_output_file):
    global f_offset
    f_offset = 1
    file = open(path_to_input_file, 'rb')
    document = AWDDocument.decode(file)
    filename = os.path.splitext(os.path.basename(file.name))[0]
    output_string = f"o {filename}\n"
    for block_id in document.blocks:
        header, block = document.blocks[block_id]
        if isinstance(block, MeshInstanceBlock):
            block_body = document.blocks[block.mesh_block_id][1]
            if isinstance(block_body, str):
                logger.error(f"Could not parse mesh '{filename}' because of this error: {block_body}")
                raise RuntimeError()
            lookup_name = block.scene_header.lookup_name
            output_string += f"g {lookup_name}\n"
            output_string += build_obj(block_body)
    o = open(path_to_output_file, 'w')
    o.write(output_string)
    pass


def assert_dir_exists(path):
    if not os.path.exists(path):
        print(f"ERROR: '{path}' does not exist")
        exit(1)

    if not os.path.isdir(path):
        print(f"ERROR: '{path}' is not a directory")
        exit(1)


def parse_args():
    if len(sys.argv) != 3:
        print("ERROR: invalid arguments. Run me like this: main.py <AWD-Directory> <Target-OBJ-Directory>")
        exit(1)

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    assert_dir_exists(in_dir)
    assert_dir_exists(out_dir)

    return in_dir, out_dir


def main():
    print("AWD to OBJ batch converter")
    awd_path, obj_path = parse_args()

    failed_files = []
    for cur_file in os.listdir(awd_path):
        if cur_file.endswith(".awd"):
            logger.info(f"Convert {cur_file}")
            try:
                convert_to_obj(awd_path + "/" + cur_file, obj_path + "/" + cur_file.replace(".awd", ".obj"))
            except (RuntimeError, struct.error, KeyError, AttributeError):
                failed_files.append(cur_file)

    logger.info(f"Failed files: {failed_files}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
