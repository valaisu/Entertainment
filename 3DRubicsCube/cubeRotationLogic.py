# Rubik's cube rotation logic

# Colors   :   red, blue, green, white, yellow, orange
# Numbers  :    3    2     6      1      4       5
# Positions:    U    L     B      F      R       D
#
# Solved Rubik's cube, and the order of squares within the sides
#
#       1 2 R
#       R R R
#       R R 9
# 1 2 B 1 2 W 1 2 Y 1 2 G
# B B B W W W Y Y Y G G G
# B B 9 W W 9 Y Y 9 G G 9
#       1 2 O
#       O O O
#       O O 9

# ordering of sides
#   3
# 2 1 4 6
#   5

#
# The order of squares on a side:
#
# 1 2 3
# 4 5 6
# 7 8 9
#
# Possible moves
# 6*2 + 3*2 = 18
# Edges (6*2):
# Dcw Dccw Ucw Uccw Lcw Lccw Rcw Rccw Bcw Bccw Fcw Fccw
# Dcw = Down clockwise
# Middles (3*2):
# xcw xccw ycw yccw zcw zccw


def reverseList(rev):
    for i in range(int(len(rev)/2)):
        rev[i], rev[-i-1] = rev[-i-1], rev[i]


def printCube(kuutio):

    print("")
    for i in range(3):
        temp = "        "
        for j in range(3):
            temp += str(kuutio[2][3*i+j]) + " "
        print(temp)

    list = [1,0,3,5]
    for i in range(3):
        temp = " "
        for j in range(4):
            for k in range(3):
                temp += " " + str(kuutio[list[j]][3*i+k])
        print(temp)

    for i in range(3):
        temp = "        "
        for j in range(3):
            temp += str(kuutio[4][3*i+j]) + " "
        print(temp)


def dcw(kuutio):
    kuutio[1][6:9], kuutio[0][6:9], kuutio[3][6:9], kuutio[5][6:9] = kuutio[5][6:9], kuutio[1][6:9], kuutio[0][6:9], kuutio[3][6:9]
    rotate = [7,4,1,8,5,2,9,6,3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[4][rotate[i]-1])
    kuutio[4] = tempEdge


def dccw(kuutio):
    kuutio[1][6:9], kuutio[0][6:9], kuutio[3][6:9], kuutio[5][6:9] = kuutio[0][6:9], kuutio[3][6:9], kuutio[5][6:9], kuutio[1][6:9]
    # 1->3 2->6 3->9 4->2 5->5 6->8 7->1 8->4 9->7
    # ((n)%3+1)*3-(n).floor()/3 cool but quite useless
    # 369 258 147
    rotate = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[4][rotate[i] - 1])
    kuutio[4] = tempEdge

def ucw(kuutio):
    kuutio[1][0:3], kuutio[0][0:3], kuutio[3][0:3], kuutio[5][0:3] = kuutio[0][0:3], kuutio[3][0:3], kuutio[5][0:3], kuutio[1][0:3]
    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[2][rotate[i] - 1])
    kuutio[2] = tempEdge


def uccw(kuutio):
    kuutio[1][0:3], kuutio[0][0:3], kuutio[3][0:3], kuutio[5][0:3] = kuutio[5][0:3], kuutio[1][0:3], kuutio[0][0:3], kuutio[3][0:3]
    rotate = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[2][rotate[i] - 1])
    kuutio[2] = tempEdge

def lcw(kuutio):
    toBot, fromBot = kuutio[4][0::3], kuutio[5][2::3]
    reverseList(toBot), reverseList(fromBot)
    kuutio[0][0::3], kuutio[4][0::3], kuutio[5][2::3], kuutio[2][0::3] = kuutio[2][0::3], kuutio[0][0::3], toBot, fromBot
    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[1][rotate[i] - 1])
    kuutio[1] = tempEdge

def lccw(kuutio):
    toBot, fromBot = kuutio[2][0::3], kuutio[5][2::3]
    reverseList(toBot), reverseList(fromBot)
    kuutio[0][0::3], kuutio[4][0::3], kuutio[5][2::3], kuutio[2][0::3] = kuutio[4][0::3], fromBot, toBot, kuutio[0][0::3]
    rotate = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[1][rotate[i] - 1])
    kuutio[1] = tempEdge

def rcw(kuutio):
    toBack, fromBack = kuutio[2][2::3], kuutio[5][0::3]
    reverseList(toBack), reverseList(fromBack)
    kuutio[0][2::3], kuutio[2][2::3], kuutio[5][0::3], kuutio[4][2::3] = kuutio[4][2::3], kuutio[0][2::3], toBack, fromBack
    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[3][rotate[i] - 1])
    kuutio[3] = tempEdge

def rccw(kuutio):
    toBack, fromBack = kuutio[4][2::3], kuutio[5][0::3]
    reverseList(toBack), reverseList(fromBack)
    kuutio[0][2::3], kuutio[2][2::3], kuutio[5][0::3], kuutio[4][2::3] = kuutio[2][2::3], fromBack, toBack, kuutio[0][2::3]
    rotate = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[3][rotate[i] - 1])
    kuutio[3] = tempEdge

def bcw(kuutio):
    fromTop, fromBot = kuutio[2][0:3], kuutio[4][6:9]
    reverseList(fromTop), reverseList(fromBot)
    kuutio[3][2::3], kuutio[2][0:3], kuutio[1][0::3], kuutio[4][6:9] = fromBot, kuutio[3][2::3], fromTop, kuutio[1][0::3]
    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[5][rotate[i] - 1])
    kuutio[5] = tempEdge

def bccw(kuutio):
    toTop, toBot = kuutio[1][0::3], kuutio[3][2::3]
    reverseList(toBot), reverseList(toTop)
    kuutio[3][2::3], kuutio[2][0:3], kuutio[1][0::3], kuutio[4][6:9] = kuutio[2][0:3], toTop, kuutio[4][6:9], toBot
    rotate = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[5][rotate[i] - 1])
    kuutio[5] = tempEdge

def fcw(kuutio):
    toBot, toTop = kuutio[3][0::3], kuutio[1][2::3]
    reverseList(toBot), reverseList(toTop)
    kuutio[1][2::3], kuutio[2][6:9], kuutio[3][0::3], kuutio[4][0:3] = kuutio[4][0:3], toTop, kuutio[2][6:9], toBot
    rotate = [7, 4, 1, 8, 5, 2, 9, 6, 3]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[0][rotate[i] - 1])
    kuutio[0] = tempEdge

def fccw(kuutio):
    fromBot, fromTop = kuutio[4][0:3], kuutio[2][6:9]
    reverseList(fromBot), reverseList(fromTop)
    kuutio[1][2::3], kuutio[2][6:9], kuutio[3][0::3], kuutio[4][0:3] = fromTop, kuutio[3][0::3], fromBot, kuutio[1][2::3]
    rotate = [3, 6, 9, 2, 5, 8, 1, 4, 7]
    tempEdge = []
    for i in range(9):
        tempEdge.append(kuutio[0][rotate[i] - 1])
    kuutio[0] = tempEdge

# TODO: implement the rotation of the middles

cols = ['W', 'B', 'R', 'Y', 'O', 'G']
cube = []
for i in range(6):
    side = []
    for j in range(9):
        side.append(cols[i])
    cube.append(side)

# testing
cube[4] = [1,2,3,4,5,6,7,8,9]
cube[5] = [1,2,3,4,5,6,7,8,9]
printCube(cube)
bccw(cube)
printCube(cube)
bccw(cube)
bccw(cube)
bccw(cube)

printCube(cube)
