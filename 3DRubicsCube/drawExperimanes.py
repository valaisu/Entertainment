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

# Define some functions

def inversion2D(coordList, height):
    for i in range(len(coordList)):
        coordList[i] = [coordList[i][0], height-coordList[i][1]]
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
        return [betweenX, betweenY]
    else:
        multiplier = point[2] / (viewpoint[2] - point[2])
        newX = point[0] + (point[0] - viewpoint[0]) * multiplier
        newY = point[1] + (point[1] - viewpoint[1]) * multiplier
        return [newX, newY]


# list = PointList
def updatePoints(list, viewpoint):
    for i in range(len(list)):
        list[i].coords2D = coords3Dto2D_XYPlane(viewpoint, list[i].coords)
        list[i].distance = distance(viewPoint, list[i].coords)

# The data structure

class point:
    def __init__(self, coords, order):
        self.coords = coords
        self.drawable = False
        self.distance = 0
        self.coords2D = [0, 0] #remember to set these!
        self.order = order


class face:
    def __init__(self, points, color):
        self.hasBeenDrawn = False
        self.points = points
        self.color = color

    def drawable(self):
        return all([i.drawable for i in self.points])

    def point2DCoords(self):
        p = []
        for i in range(len(self.points)):
            p.append(self.points[i].coords2D)
        return p


class cube:
    def __init__(self, faces):
        self.faces = faces

RGB_Palette = ((0, 155, 72), (255, 255, 255), (183, 18, 52), (255, 213, 0), (0, 70, 173), (255, 88, 0))

def createCube(center, size, viewpoint):
    loop = [[center[0]-0.5*size, center[1]-0.5*size], [center[0]-0.5*size, center[1]+0.5*size], [center[0]+0.5*size, center[1]+0.5*size], [center[0]+0.5*size, center[1]-0.5*size]]
    pointList = []
    for i in range(2):
        for j in range(4):
            pointList.append(point(loop[j] + [center[2]+(i-0.5)*size], j + 4 * i))
    faceList = []
    for i in range(2):
        faceList.append(face(pointList[(i * 4):(i * 4 + 4)], RGB_Palette[i]))
    for i in range(4):
        faceList.append(face([pointList[0 + i], pointList[(1 + i) % 4], pointList[(5 + i) % 8], pointList[4 + i]], RGB_Palette[i+2]))
    updatePoints(pointList, viewpoint)
    return pointList, faceList


# later faces are added here farthest from nearest to the viewpoint
drawQueue = []

# prep image
im = Image.open("BlankImage.png")
draw = ImageDraw.Draw(im)

viewPoint = [2048+1024, 2048+1024, 4096+1024]
pointList, faceList = [],[]

# creates the famous mushroom thing
for i in range(3):
    for j in range(3):
        for k in range(3):
            if not (j == k == 1 or i == j == 1 or i == k == 1):

                tempP, tempL = createCube((i*1024-512, j*1024-512, k*1024-512), 1024, viewPoint)
                pointList += tempP
                faceList += tempL


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
    # calculates how far the points of each face are on average from the viewpoint, decides drawing order based on that
    newDrawables.sort(key=lambda x: sum([faceList[x].points[k].distance for k in range(4)]), reverse=True)
    drawQueue += newDrawables

zoom = 0.1
shift = (128*3, 128*3)

for i in range(len(drawQueue)):
    temp = faceList[drawQueue[i]].points
    points = [temp[k].coords2D for k in range(len(temp))]

    draw.polygon(
        ((points[0][0] * zoom + shift[0], points[0][1] * zoom + shift[1]),
         (points[1][0] * zoom + shift[0], points[1][1] * zoom + shift[1]),
         (points[2][0] * zoom + shift[0], points[2][1] * zoom + shift[1]),
         (points[3][0] * zoom + shift[0], points[3][1] * zoom + shift[1])),
        fill=(faceList[drawQueue[i]].color),
        outline=(0, 0, 0))

im.show()
