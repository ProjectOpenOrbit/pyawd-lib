# AWD library for Python

Library for handling AWD documents.

See awaytools.com

## Features
* decoding of AWD files and providing them in an object-oriented model
* No AWD writing, there are official tools for that
* Decoding of mesh instances, normals and UV coordinates

## TODOs
* Unit testing
* Support for precision levels other than float32
* Support for PrimitiveGeometry (Planes, Spheres, etc.) Export

## Purpose for OpenOrbit

DarkOrbit distributes their 3D models as AWD files on web servers. The game client downloads them on demand.
AWD files are uncommon and thus are unusable in Unity, Blender, Unreal, etc.

This library is used to convert the AWD files to a more common format such as OBJ, so we can use the 3D models in Unity.

## Usage
The `main.py` script provided in this repository can be used to batch convert AWD files to OBJ.

Usage: `python main.py <AWD-Directory> <Target-OBJ-Directory>`

Example: `python main.py ./awd_files ./obj_files`

This will convert all AWD files in the `awd_files` directory and output the corresponding OBJ files in the `obj_files` directory.
