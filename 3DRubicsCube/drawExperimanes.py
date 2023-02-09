import pygame
import math

# Aim is to create a Rubik's cube, that user can rotate realistically.
# Currently draws a single 3D cube from certain viewpoint on a 2D plane.

#TODO: -Design and create a proper datastructure for describing the cube CHECK
#      -Change to a 2D display library, that allows user interaction CHECK
#      -Make the viewpoint movable, then allow the user control it CHECK
#           -Make the plane plane the cube is drawn on orthogonal to the viewpoint
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

# MOVING THE VIEWPOINT

def betaInc(amount, b):
    return (b + amount) % 360

def betaDec(amount, b):
    return (b - amount) % 360

def alphaInc(amount, a):
    return (a + amount) % 360

def alphaDec(amount, a):
    return (a - amount) % 360

def carthesian(r, a, b):
    x = r * math.sin(a / 180 * math.pi)*math.cos(b / 180 * math.pi)
    y = r * math.sin(a / 180 * math.pi)*math.sin(b / 180 * math.pi)
    z = r * math.cos(a / 180 * math.pi)
    return [x, y, z]

# more advanced drawing functions

def pointOntoPlane(point1, point2, plane):
    # materials used:
    # https://math.stackexchange.com/questions/1429131/find-an-equation-of-the-plane-perpendicular-to-vector-v-and-passing-through-the
    # https://www.geeksforgeeks.org/equation-of-a-line-in-3d/

    # returns where a line defined by 2 points intersects a plane in 3d space
    # the plane always intersects the 0,0,0

    # example:
    # point1 = 1,2,3
    # point2 = 4,5,6
    # plane  = 1,1,2 <- later referred as px, py, pz

    # (line orthogonal to plane equation: x = y = 1/2 z) not needed here
    # plane equation: x + y + 2*z = 0
    # 1, 2, 3 -> 4, 5, 6    the direction does not matter
    # delta = 4-1, 5-2, 6-3 = 3,3,3

    delta = [point1[0] - point2[0], point1[1] - point2[1], point1[2] - point2[2]]

    # line equation: (x-1)/3 = (y-2)/3 = (z-3)/3
    # line equation: (x-point1[0])/delta[0] = (y-point1[1])/delta[1] = (z-point1[2])/delta[2]

    # solving y as x:
    # (x-1)/3 = (y-2)/3
    # (x - point1[0]) / delta[0] = (y - point1[1]) / delta[1]
    # (x - point1[0]) / delta[0] * delta[1] = (y - point1[1])
    # y = (x - point1[0]) / delta[0] * delta[1] + point1[1]
    # =>
    # y = x / delta[0] * delta[1] - point1[0] / delta[0] * delta[1] + point1[1]

    # solving z as x:
    # works the same way
    # z = (x - point1[0]) / delta[0] * delta[2] + point1[2]
    # z = x / delta[0] * delta[2] - point1[0] / delta[0] * delta[2] + point1[2]

    # The whole equation
    # solve x:
    # the plane equation: px * x + py * y + pz * z = 0
    # =>
    # px * x + py * y + pz * z = 0
    # px * x + py * x * delta[1] / delta[0] + pz * x * delta[2] / delta[0] =
    # pz * (point1[0] / delta[0] * delta[2] - point1[2]) + py * (point1[0] / delta[0] * delta[1] - point1[1]) =>
    # x * (px + py * delta[1] / delta[0]+ pz * delta[2] / delta[0]) =
    # pz * (point1[0] / delta[0] * delta[2] - point1[2]) + py * (point1[0] / delta[0] * delta[1] - point1[1]) =>
    # x = (pz * (point1[0] / delta[0] * delta[2] - point1[2]) + py * (point1[0] / delta[0] * delta[1] - point1[1])) / (px + py * delta[1] / delta[0]+ pz * delta[2] / delta[0])

    # solving z as y:
    # z = (y - point1[1]) / delta[1] * delta[2] + point1[2]
    # z = y / delta[1] * delta[2] - point1[1] / delta[1] * delta[2] + point1[2]

    # solve y:
    # px * x + py * y + pz * z = 0
    # pz * (y / delta[1] * delta[2]) + py * y = -px * x + pz * (point1[1] * delta[2] / delta[1] - point1[2])
    # y * (py + pz * delta[2] / delta[1]) = -px * x + pz * (point1[1] * delta[2] / delta[1] - point1[2])
    # y = (-px * x + pz * (point1[1] * delta[2] / delta[1] - point1[2])) / (py + pz * delta[2] / delta[1])

    # solve z:
    # px * x + py * y + pz * z = 0
    # z = -(px * x + py * y) / pz

    px, py, pz = plane[0], plane[1], plane[2]
    try:
        xCoord = (pz * (point1[0] / delta[0] * delta[2] - point1[2]) + py * (point1[0] / delta[0] * delta[1] - point1[1])) / (px + py * delta[1] / delta[0]+ pz * delta[2] / delta[0])
        yCoord = (-px * xCoord + pz * (point1[1] * delta[2] / delta[1] - point1[2])) / (py + pz * delta[2] / delta[1])
        zCoord = -(px * xCoord + py * yCoord) / pz
        return [xCoord, yCoord, zCoord]
    except ZeroDivisionError:
        # this error should be rare, and when it occurs, nothing should be drawn anyways.
        # I will deal with this properly (temporally) later.
        return [0, 0, 0]


def rotatePoints(vector, pointsRot):
    # the idea is to rotate points on a plane defined by orthogonal vector so, that
    # the vector points to dir 0,0,1.

    # Material used:
    # https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
    # https://matthew-brett.github.io/teaching/rotation_2d.html
    dir = [0,0,1]

    # angle between 2 vectors: cos(alpha) = a.b/(|a||b|)
    # xz plane
    dotProd = vector[0] * dir[0] + vector[2] * dir[2]
    lenProd = math.sqrt(vector[0] ** 2 + vector[2] ** 2) * math.sqrt(dir[0] ** 2 + dir[2] ** 2)
    beta = -math.acos(dotProd / lenProd)

    # rotation around y-axis:
    # | x cos θ + z sin θ| = |x'|
    # |−x sin θ + z cos θ| = |z'|
    for i in range(len(pointsRot)):
        pointsRot[i] = [pointsRot[i][0] * math.cos(beta) + pointsRot[i][2] * math.sin(beta), pointsRot[i][1],
                     -pointsRot[i][0] * math.sin(beta) + pointsRot[i][2] * math.cos(beta)]
    newVector = [vector[0] * math.cos(beta) + vector[2] * math.sin(beta), vector[1],
                 -vector[0] * math.sin(beta) + vector[2] * math.cos(beta)]

    # yz plane
    dotProd = newVector[1] * dir[1] + newVector[2] * dir[2]
    lenProd = math.sqrt(newVector[1] ** 2 + newVector[2] ** 2) * math.sqrt(dir[1] ** 2 + dir[2] ** 2)
    alpha = math.acos(dotProd / lenProd)

    # rotation around x-axis:
    # | y cos θ − z sin θ| = |y'|
    # | y sin θ + z cos θ| = |z'|
    for i in range(len(pointsRot)):
        pointsRot[i] = [pointsRot[i][0], pointsRot[i][1] * math.cos(alpha) - pointsRot[i][2] * math.sin(alpha),
                     pointsRot[i][1]*math.sin(alpha) + pointsRot[i][2]*math.cos(alpha)]

    # finalVector = [newVector[0], newVector[1] * math.cos(alpha) - newVector[2] * math.sin(alpha),
    #               newVector[1] * math.sin(alpha) + newVector[2] * math.cos(alpha)]

    return pointsRot

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


def poly(surf, color, coords):
    pygame.draw.polygon(surf, color, coords)
    pygame.draw.polygon(surf, (0,0,0), coords, 2)

moveInstructions = [0,0,0]
clockCounter = 0
a = 45
b = 60
alpha = 0
beta = 0
polygon = False
while not crashed:

    dist = 6000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                alpha -= 0.6
            if event.key == pygame.K_UP:
                alpha += 0.6
            if event.key == pygame.K_LEFT:
                beta += 0.6
            if event.key == pygame.K_RIGHT:
                beta -= 0.6

            if event.key == pygame.K_q:
                moveInstructions[2] += 100
            if event.key == pygame.K_a:
                moveInstructions[2] -= 100

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                alpha += 0.6
            if event.key == pygame.K_UP:
                alpha -= 0.6
            if event.key == pygame.K_LEFT:
                beta -= 0.6
            if event.key == pygame.K_RIGHT:
                beta += 0.6

            if event.key == pygame.K_q:
                moveInstructions[2] -= 100
            if event.key == pygame.K_a:
                moveInstructions[2] += 100

    a += alpha
    b += beta
    viewPoint = carthesian(dist, a, b)
    updatePoints(pointList, viewPoint)
    gameDisplay.fill(white)
    if polygon:
        poly(gameDisplay, (100, 100, 1), ((100, 140), (120, 120), (130, 160), (120, 200), (110, 180)))
    for i in range(len(faceList)):
        faceList[i].hasBeenDrawn = False
    updatePoints(pointList, viewPoint)

    drawQueue = calculateDrawOrder(pointList, faceList)
    for i in range(len(drawQueue)):
        temp = faceList[drawQueue[i]].points
        points = [pointOntoPlane(viewPoint, temp[k].coords, viewPoint) for k in range(len(temp))]
        points = rotatePoints(viewPoint, points)

        poly(gameDisplay, faceList[drawQueue[i]].color,
            ((points[0][0] * zoom + shift[0], points[0][1] * zoom + shift[1]),
             (points[1][0] * zoom + shift[0], points[1][1] * zoom + shift[1]),
             (points[2][0] * zoom + shift[0], points[2][1] * zoom + shift[1]),
             (points[3][0] * zoom + shift[0], points[3][1] * zoom + shift[1])))

    pygame.display.update()
    clockCounter += 1
    if clockCounter % 30 == 0: print(carthesian(dist, a, b))
    clock.tick(60)

pygame.quit()
quit()
