import sys
from PIL import Image, ImageDraw
import math

# Program in progress

# Aim is to create a rubics cube, that user can rotate realistically.
# Currently draws a single 3D cube from certain viewpoint on a 2D plane.

#TODO: -Design and create a proper datastructure for describing the cube
#      -Change to a 2D display library, that allows user interaction
#      -Make the viewpoint movable, then allow the user control it
#      -Add more cubes, make them rotatable around x y and z axis
#      -Add keybinds for each rubics cube move



def inversion(coordList, height):
    for i in range(len(coordList)):
        coordList[i] = [coordList[i][0], height-coordList[i][1], coordList[i][2]]
    return coordList


im = Image.open("BlankImage.png")

draw = ImageDraw.Draw(im)



viewPoint = [2048, 2048, 4096]
center = [512, 512, 0]
points = []

for k in range(2):
    for j in range(2):
        for i in range(2):
            points.append([i*1024, j*1024, k*1024])

newValues = []
for i in range(len(points)):
    dz0 = points[i][2]
    dz1 = viewPoint[2]-points[i][2]
    #dy0 = ???
    dy1 = viewPoint[1]-points[i][1]
    #dx0 = ???
    dx1 = viewPoint[0]-points[i][0]

    dy0 = dy1*dz0/dz1
    dx0 = dx1*dz0/dz1
    newValues.append([points[i][0]-dx0, points[i][1]-dy0, 0])
    print(newValues[-1])

for i in range(len(newValues)):
    newValues[i] = [newValues[i][0]/2+256+128, newValues[i][1]/2+256+128, 0]

newValues = inversion(newValues, 1024)

for i in range(len((newValues))):
    print(newValues[i])

print("__________________________")

#print([(points[4][0], points[4][1]), (points[5][0], points[5][1]), (points[6][0], points[6][1]), (points[7][0], points[7][1])])
draw.polygon(
       ((newValues[4][0], newValues[4][1]), (newValues[5][0], newValues[5][1]), (newValues[7][0], newValues[7][1]), (newValues[6][0], newValues[6][1])),
       fill=(255, 20, 20),
       outline=(0, 0, 0))

draw.polygon(
       ((newValues[2][0], newValues[2][1]), (newValues[3][0], newValues[3][1]), (newValues[7][0], newValues[7][1]), (newValues[6][0], newValues[6][1])),
       fill=(20, 255, 20),
       outline=(0, 0, 0))

draw.polygon(
       ((newValues[1][0], newValues[1][1]), (newValues[3][0], newValues[3][1]), (newValues[7][0], newValues[7][1]), (newValues[5][0], newValues[5][1])),
       fill=(20, 20, 255),
       outline=(0, 0, 0))

im.show()
