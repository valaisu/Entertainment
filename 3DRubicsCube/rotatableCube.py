import math
import pygame

# combines the drawing and rotating of rubiks cube.
# The idea is to firs convert the fundamental data structure
# to be faces instead of points. Each face has
#   points on 3d space
#   a middle used for deciding the drawing order.
#   SIDENOTE: While the logic of drawing the planes in order
#   defined by the distance form the middle point of the plane
#   to viewpoint, in the case of rubiks cube no problems should emerge.


# the coordinates of faces are defined by the place of the face
# in the cube.

# The cube:
# ordering of sides
#   3       /   2     \
# 2 1 4 6  |  1 0 3 5  |
#   5       \   4     /

# The order of squares on a side:
# 1 2 3
# 4 5 6
# 7 8 9

# so for example face at position side 1, square 1 always has same coords and middlecoord

# ds faces(color, pos)
#   init color, pos
#   def update pos

class square:
    def __init__(self, color, points, middle):
        self.color = color
        self.points = points
        self.middle = middle

    def updatePos(self, points, middle):
        self.points = points
        self.middle = middle


# def create position list with coords and middles, dimensions: [6][9][4+1]

def createCubeSides(center, squareSize):
    RGB_Palette = ((0, 155, 72), (255, 255, 255), (183, 18, 52), (255, 213, 0), (0, 70, 173), (255, 88, 0))
    sides = []
    for i in range(2):
        sideTemp = []
        for j in range(3):
            for k in range(3):
                sideTemp.append(square(RGB_Palette[i],
                    [[center[i]+3*(i-0.5)*squareSize, center[j]+(j-1.5)*squareSize, center[k]+(k-0.5)*squareSize],
                    [center[i]+3*(i-0.5)*squareSize, center[j]+(j-0.5)*squareSize, center[k]+(k-0.5)*squareSize],
                    [center[i]+3*(i-0.5)*squareSize, center[j]+(j-0.5)*squareSize, center[k]+(k-1.5)*squareSize],
                    [center[i]+3*(i-0.5)*squareSize, center[j]+(j-1.5)*squareSize, center[k]+(k-1.5)*squareSize]],
                    [center[i]+3*(i-0.5)*squareSize, center[j]+(j-1)*squareSize, center[k]+(k-1)*squareSize]
                ))
        sides.append(sideTemp)

    for i in range(2):
        sideTemp = []
        for j in range(3):
            for k in range(3):
                sideTemp.append(square(RGB_Palette[i+2],
                    [[center[j]+(j-1.5)*squareSize, center[k]+(k-0.5)*squareSize, center[i]+3*(i-0.5)*squareSize],
                    [center[j]+(j-0.5)*squareSize, center[k]+(k-0.5)*squareSize, center[i]+3*(i-0.5)*squareSize],
                    [center[j]+(j-0.5)*squareSize, center[k]+(k-1.5)*squareSize, center[i]+3*(i-0.5)*squareSize],
                    [center[j]+(j-1.5)*squareSize, center[k]+(k-1.5)*squareSize, center[i]+3*(i-0.5)*squareSize]],
                    [center[j]+(j-1)*squareSize, center[k]+(k-1)*squareSize, center[i]+3*(i-0.5)*squareSize]
                ))
        sides.append(sideTemp)

    for i in range(2):
        sideTemp = []
        for j in range(3):
            for k in range(3):
                sideTemp.append(square(RGB_Palette[i+4],
                    [[center[k]+(k-0.5)*squareSize, center[i]+3*(i-0.5)*squareSize, center[j]+(j-1.5)*squareSize],
                    [center[k]+(k-0.5)*squareSize, center[i]+3*(i-0.5)*squareSize, center[j]+(j-0.5)*squareSize],
                    [center[k]+(k-1.5)*squareSize, center[i]+3*(i-0.5)*squareSize, center[j]+(j-0.5)*squareSize],
                    [center[k]+(k-1.5)*squareSize, center[i]+3*(i-0.5)*squareSize, center[j]+(j-1.5)*squareSize]],
                    [center[k]+(k-1)*squareSize, center[i]+3*(i-0.5)*squareSize, center[j]+(j-1)*squareSize]
                ))
        sides.append(sideTemp)
    # sides: 2, 4, 5, 3, 6, 1
    #   3       /   2     \
    # 2 1 4 6  |  1 0 3 5  |
    #   5       \   4     /
    return [sides[5],sides[0],sides[3],sides[1],sides[2], sides[4]]


# def create cube, a list of squares
def createCubeList(kuutio):
    cubelistL = []
    for i in range(6):
        for j in range(9):
            cubelistL.append(kuutio[i][j].points + [kuutio[i][j].middle] + [kuutio[i][j].color])
    return cubelistL


def distance(viewpoint, point):
    return math.sqrt((viewpoint[0]-point[0])**2+(viewpoint[1]-point[1])**2+(viewpoint[2]-point[2])**2)


#def updatePoints():

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
        xCoord = (pz * (point1[0] / delta[0] * delta[2] - point1[2]) + py * (point1[0] / delta[0] * delta[1] - point1[1])) / (px + py * delta[1] / delta[0] + pz * delta[2] / delta[0])
        yCoord = (-px * xCoord + pz * (point1[1] * delta[2] / delta[1] - point1[2])) / (py + pz * delta[2] / delta[1])
        zCoord = -(px * xCoord + py * yCoord) / pz
        return [xCoord, yCoord, zCoord]
    except ZeroDivisionError:
        # this error should be rare, and when it occurs, nothing should be drawn anyways.
        return [0, 0, 0]

def rotatePoints(vector, points):
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
    beta = -math.acos(dotProd / lenProd)*(vector[0]/abs(vector[0]))
    #print("beta: ", beta*180/math.pi)
    # rotation around y-axis:
    # | x cos θ + z sin θ| = |x'|
    # |−x sin θ + z cos θ| = |z'|
    for i in range(len(points)):
        points[i] = [points[i][0] * math.cos(beta) + points[i][2] * math.sin(beta), points[i][1],
                     -points[i][0] * math.sin(beta) + points[i][2] * math.cos(beta)]
    newVector = [vector[0] * math.cos(beta) + vector[2] * math.sin(beta), vector[1],
                 -vector[0] * math.sin(beta) + vector[2] * math.cos(beta)]

    # yz plane
    dotProd = newVector[1] * dir[1] + newVector[2] * dir[2]
    lenProd = math.sqrt(newVector[1] ** 2 + newVector[2] ** 2) * math.sqrt(dir[1] ** 2 + dir[2] ** 2)
    alpha = math.acos(dotProd / lenProd)*(newVector[1]/abs(newVector[1]))
    # rotation around x-axis:
    # | y cos θ − z sin θ| = |y'|
    # | y sin θ + z cos θ| = |z'|
    for i in range(len(points)):
        points[i] = [points[i][0], points[i][1] * math.cos(alpha) - points[i][2] * math.sin(alpha),
                     points[i][1]*math.sin(alpha) + points[i][2]*math.cos(alpha)]

    # finalVector = [newVector[0], newVector[1] * math.cos(alpha) - newVector[2] * math.sin(alpha),
    #               newVector[1] * math.sin(alpha) + newVector[2] * math.cos(alpha)]

    return points


# def order the faces based on middle point distance from the viewpoint
'''def drawOrderList(viewpoint, cubel):
    ret = cubel
    ret.sort(key=lambda x: distance(x[4], viewpoint), reverse=True)
    return ret'''


# the rotation logic it self
#   all 18 rotations
#   make them call the updating of positions for the involved faces

def flatten(l):
    return [item for sublist in l for item in sublist]


def reverseList(rev):
    for i in range(int(len(rev)/2)):
        rev[i], rev[-i-1] = rev[-i-1], rev[i]


def dcw(kuutio):
    l1 = flatten([kuutio[1][6:9], kuutio[0][6:9], kuutio[3][6:9], kuutio[5][6:9]])
    l2 = flatten([kuutio[5][6:9], kuutio[1][6:9], kuutio[0][6:9], kuutio[3][6:9]])
    colors = [l2[i].color for i in range(len(l2))]
    for i in range(len(colors)):
        l1[i].color = colors[i]

    rotate = [7,4,1,8,5,2,9,6,3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[4][rotate[i]-1])
    kuutio[4] = tempEdge

def ucw(kuutio):
    l1 = flatten([kuutio[1][0:3], kuutio[0][0:3], kuutio[3][0:3], kuutio[5][0:3]])
    l2 = flatten([kuutio[0][0:3], kuutio[3][0:3], kuutio[5][0:3], kuutio[1][0:3]])
    colors = [l2[i].color for i in range(len(l2))]
    for i in range(len(colors)):
        l1[i].color = colors[i]

    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[2][rotate[i] - 1])
    kuutio[2] = tempEdge


def lcw(kuutio):
    toBot, fromBot = kuutio[4][0::3], kuutio[5][2::3]
    reverseList(toBot), reverseList(fromBot)
    l1 = flatten([kuutio[0][0::3], kuutio[4][0::3], kuutio[5][2::3], kuutio[2][0::3]])
    l2 = flatten([kuutio[2][0::3], kuutio[0][0::3], toBot, fromBot])
    colors = [l2[i].color for i in range(len(l2))]
    for i in range(len(colors)):
        l1[i].color = colors[i]

    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[1][rotate[i] - 1])
    kuutio[1] = tempEdge


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

# draws polygon
def poly(surf, color, coords):
    pygame.draw.polygon(surf, color, coords)
    pygame.draw.polygon(surf, (0,0,0), coords, 2)


# CREATE THE CUBE


cube = createCubeSides([0,0,0], 100)
cubeList = createCubeList(cube) # created also in the game loop
viewpoint = [6000, 0, 0]
zoom = 1
shift = (128*3, 128*3)

# RUN THE GAME


pygame.init()

display_width = 800
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Rubik's cube")

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False







moveInstructions = [0,0,0]
clockCounter = 0
a = 45
b = 60
alpha = 0
beta = 0
polygon = False
while not crashed:
    gameDisplay.fill(white)
    cubeList = createCubeList(cube)
    dist = 6000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                dcw(cube)
            if event.key == pygame.K_r:
                ucw(cube)
            if event.key == pygame.K_t:
                lcw(cube)

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
    viewpoint = carthesian(dist, a, b)
    drawQueue = (createCubeList(cube))
    drawQueue.sort(key=lambda x: distance(viewpoint, x[4]), reverse=True)

    for i in range(len(drawQueue)):
        #
        points = drawQueue[i][0:4]
        points = [pointOntoPlane(viewpoint, points[k], viewpoint) for k in range(4)]
        points = rotatePoints(viewpoint, points)

        poly(gameDisplay, drawQueue[i][5],
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