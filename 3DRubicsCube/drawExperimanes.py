#import sys
from PIL import Image, ImageDraw
import math
import copy

# Program in progress

# Aim is to create a rubics cube, that user can rotate realistically.
# Currently draws a single 3D cube from certain viewpoint on a 2D plane.

#TODO: -Design and create a proper datastructure for describing the cube CHECK
#      -Change to a 2D display library, that allows user interaction
#      -Make the viewpoint movable, then allow the user control it
#      -Add more cubes, make them rotatable around x y and z axis
#      -Add keybinds for each rubics cube move



def inversion2D(coordList, height):
    for i in range(len(coordList)):
        coordList[i] = [coordList[i][0], height-coordList[i][1]]
    return coordList

def inversion3D(coordList, height):
    for i in range(len(coordList)):
        coordList[i] = [coordList[i][0], height-coordList[i][1], coordList[i][2]]
    return coordList


def distance(viewpoint, point):
    return math.sqrt((viewpoint[0]-point[0])**2+(viewpoint[1]-point[1])**2+(viewpoint[2]-point[2])**2)


def coords3Dto2D_XYPlane(viewpoint, point):
    # draw a line via viewpoint and 3D coordinate, and see where it
    # intersects with the XY plane
    # viewpoint and point both are in [x, y, z] format

    if viewpoint[2] * point[2] < 0:
        distZ = abs(viewpoint[2] - point[2])
        betweenX = point[0] * abs(viewpoint[2] / distZ) + viewpoint[0] * abs(point[2] / distZ)
        betweenY = point[1] * abs(viewpoint[2] / distZ) + viewpoint[1] * abs(point[2] / distZ)
        print([betweenX, betweenY, 0])
        return [betweenX, betweenY]
    else:
        multiplier = point[2] / (viewpoint[2] - point[2])
        newX = point[0] + (point[0] - viewpoint[0]) * multiplier
        newY = point[1] + (point[1] - viewpoint[1]) * multiplier
        print([newX, newY, 0])
        return [newX, newY]



class point:
    def __init__(self, coords, order):
        self.coords = coords
        self.drawable = False
        self.distance = 0
        self.coords2D = [0, 0] #remember to set these!
        self.order = order


class face:
    def __init__(self, points):
        self.hasBeenDrawn = False
        self.points = points
    def drawable(self):
        return all([i.drawable for i in self.points])
    #Returns True if if all the points of this face are drawable
    #and the face has not already been drawn
    #once this returns True, status id changed to be drawn

    def point2DCoords(self):
        p = []
        for i in range(len(self.points)):
            p.append(self.points[i].coords2D)
        return p



class cube:
    def __init__(self, faces):
        self.faces = faces



loop = [[0,0],[0,1024],[1024,1024],[1024,0]]

#lisätään kaikki 8 pistettä
pointList = []
for i in range(2):
    for j in range(4):
        pointList.append(point(loop[j] + [i*1024], j+4*i))
        #print([loop[j] + [i*1024]])



#ja sit viel 6 naamaa
faceList = []
for i in range(2):
    faceList.append(face(pointList[(i*4):(i*4+4)]))

for i in range(4):
    faceList.append(face([pointList[0+i], pointList[(1+i)%4], pointList[(5+i)%8], pointList[4+i]]))

for i in range(len(faceList)):
    points = []
    for j in range(4):
        points.append(faceList[i].points[j].coords)
    print(points)

print("------")


# later faces are added here farthest from nearest to the viewpoint
drawQueue = []


# prep image
im = Image.open("BlankImage.png")
draw = ImageDraw.Draw(im)



viewPoint = [2048, 2048, 4096]

# set distance and 2D coordinate attributes
for i in range(len(pointList)):
    pointList[i].distance = distance(viewPoint, pointList[i].coords)
    pointList[i].coords2D = coords3Dto2D_XYPlane(viewPoint, pointList[i].coords)

# sort the points by distance
tempOrder = pointList.copy()
tempOrder.sort(key=lambda x: x.distance, reverse=True)
distanceOrder = [pointList.index(tempOrder[i]) for i in range(len(tempOrder))]


for i in range(len(pointList)):
    pointList[distanceOrder[i]].drawable = True
    newDrawables = []
    for j in range(len(faceList)):
        if faceList[j].drawable() and not faceList[j].hasBeenDrawn:
            faceList[j].hasBeenDrawn = True
            newDrawables.append(j)
    #calculates how far the points of each face are on average from the viewpoint, decides drawing order based on that
    newDrawables.sort(key=lambda x: sum([faceList[x].points[k].distance for k in range(4)]), reverse=True)
    drawQueue += newDrawables
    #print(newDrawables)
#print(drawQueue)
#drawQueue tells in which order tha faces of facelist should be drawn
for i in range(len(drawQueue)):
    #points = [faceList[drawQueue[i]].points[j].coords2D for j in range(4)]
    temp = faceList[drawQueue[i]].points
    points = [temp[k].coords2D for k in range(len(temp))]
    n = []
    n.append([temp[k].coords for k in range(len(temp))])
    #print(n, points)
    #print(points, temp)
    draw.polygon(
        ((points[0][0] / 2 + 128 * 3, points[0][1] / 2 + 128 * 3),
         (points[1][0] / 2 + 128 * 3, points[1][1] / 2 + 128 * 3),
         (points[2][0] / 2 + 128 * 3, points[2][1] / 2 + 128 * 3),
         (points[3][0] / 2 + 128 * 3, points[3][1] / 2 + 128 * 3)),
        fill=(255, 20, 20),
        outline=(0, 0, 0))
