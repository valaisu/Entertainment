# A datastructude for 3D objects ment to be
# displayed on 3D.

# Program currently in progress

class cube:
    def __init__(self, faces):
        self.faces = faces

class face:
    def __init__(self, edges):
        self.edges = edges
    def draw(self):
        for i in range(len(self.edges)):
            if not self.edges[i].points[0].draw:
                return False
        return True

class edge:
    def __init__(self, points):
        self.points = points
    def draw(self):
        return self.points[0].draw & self.points[1].draw

class point:
    def __init__(self, coords):
        self.coords = coords
        self.draw = False

loop = [[0,0],[0,1],[1,1],[1,0]]

pointList = []
for i in range(2):
    for j in range(4):
        pointList.append(point([loop[j] + [i]]))

edgeList = []
for i in range(2):
    for j in range(4):
        edgeList.append(edge([pointList[j+i*4], pointList[(j+1)%4+i*4]]))

for i in range(4):
    edgeList.append(edge([pointList[i], pointList[i+4]]))

'''for i in range(len(pointList)):
    print(pointList[i].coords)
print("------------------")
for i in range(len(edgeList)):
    print(edgeList[i].points[0].coords, edgeList[i].points[1].coords)
'''

faceList = []
for i in range(2):
    faceList.append(face(edgeList[(i*4):(i*4+4)]))

for i in range(4):
    placeholder = []
    placeholder.append(edgeList[0+i])
    placeholder.append(edgeList[(9+i)%12])
    placeholder.append(edgeList[5+i])
    placeholder.append(edgeList[8+i])
    faceList.append(face(placeholder))

for i in range(6):
    print(faceList[i].draw())


for i in range(8):
    pointList[i].draw = True


print("--------------")


for i in range(6):
    print(faceList[i].draw())
