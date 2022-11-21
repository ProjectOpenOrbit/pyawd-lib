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

## Purpose for OpenOrbit

DarkOrbit distributes their 3D models as AWD files on web servers. The game client downloads them on demand.
AWD files are uncommon and thus are unusable in Unity, Blender, Unreal, etc.

This library is used to convert the AWD files to a more common format such as OBJ, so we can use the 3D models in Unity.
