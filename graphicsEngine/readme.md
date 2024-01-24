A system for displaying blender objects in Python.

BlenderToText.py needs to be run in blender code editor. It creates a file, that main.py is able to read.

Main.py applies transformations to the triangles and calculates in which order they should be drawn so that they can be drawn on 2D surface. 
The drawing isdone with pygame. 

This project aims to be a proof of concept, as it is maybe one of the most inefficient ways to make a graphics engine

NOTE: The algorithm for deciding in which order to draw the triangles (that make up the object) is a bit unstable
with low-poly meshes. 
