import pygame
import math

# Aim is to create a Rubik's cube, that user can rotate realistically.
# Currently draws a single 3D cube from certain viewpoint on a 2D plane.

#TODO: -Design and create a proper datastructure for describing the cube CHECK
#      -Change to a 2D display library, that allows user interaction CHECK
#      -Make the viewpoint movable, then allow the user control it
#      -Add more cubes, make them rotatable around x y and z axis
#      -Add keybinds for each rubics cube move

# CREATING THE CUBE

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
        faceList.append(face([pointList[0 + i], pointList[(1 + i) % 4], pointList[4 + (1 + i) % 4], pointList[4 + i]], RGB_Palette[i+2]))
    updatePoints(pointList, viewpoint)
    return pointList, faceList


# later faces are added here farthest from nearest to the viewpoint
drawQueue = []

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

def calculateDrawOrder(pointlist, facelist):

    # sort the points by distance
    tempOrder = pointlist.copy()
    tempOrder.sort(key=lambda x: x.distance, reverse=True)
    distanceOrder = [pointlist.index(tempOrder[i]) for i in range(len(tempOrder))]
    queue = [] #defining length beforehand would make this faster
    for i in range(len(pointlist)):
        pointlist[distanceOrder[i]].drawable = True
        newDrawables = []
        for j in range(len(facelist)):
            if facelist[j].drawable() and not facelist[j].hasBeenDrawn:
                facelist[j].hasBeenDrawn = True
                newDrawables.append(j)
        # calculates how far the points of each face are on average from the viewpoint, decides drawing order based on that
        newDrawables.sort(key=lambda x: sum([facelist[x].points[k].distance for k in range(4)]), reverse=True)
        queue += newDrawables
    return queue

zoom = 0.1
shift = (128*3, 128*3)

drawQueue = calculateDrawOrder(pointList, faceList)




# CREATING THE DISPLAY

pygame.init()

display_width = 800
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tests')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('img.jpg')

def rect(surf, color):
    pygame.draw.rect(surf, color, pygame.Rect(30, 30, 60, 60))
    pygame.draw.rect(surf, (0,0,0), pygame.Rect(30, 30, 60, 60), 2)

def poly(surf, color, coords):
    pygame.draw.polygon(surf, color, coords)
    pygame.draw.polygon(surf, (0,0,0), coords, 2)


polygon = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                polygon = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                viewPoint[1] -= 100
                updatePoints(pointList, viewPoint)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                viewPoint[1] += 100
                updatePoints(pointList, viewPoint)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                viewPoint[0] += 100
                updatePoints(pointList, viewPoint)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                viewPoint[0] -= 100
                updatePoints(pointList, viewPoint)

    gameDisplay.fill(white)
    rect(gameDisplay, (250, 50, 50))
    if polygon:
        poly(gameDisplay, (100, 100, 1), ((100, 140), (120, 120), (130, 160), (120, 200), (110, 180)))
    for i in range(len(faceList)):
        faceList[i].hasBeenDrawn = False
    updatePoints(pointList, viewPoint)
    drawQueue = calculateDrawOrder(pointList, faceList)
    for i in range(len(drawQueue)):
        temp = faceList[drawQueue[i]].points
        points = [temp[k].coords2D for k in range(len(temp))]
        poly(gameDisplay, faceList[drawQueue[i]].color,
            ((points[0][0] * zoom + shift[0], points[0][1] * zoom + shift[1]),
             (points[1][0] * zoom + shift[0], points[1][1] * zoom + shift[1]),
             (points[2][0] * zoom + shift[0], points[2][1] * zoom + shift[1]),
             (points[3][0] * zoom + shift[0], points[3][1] * zoom + shift[1])))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
