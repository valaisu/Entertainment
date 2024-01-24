import numpy as np


def to_coordinates(text: str):
    """
    Converts a row produced by BlenderSaveData.py to list(s) of coordinates. A row
    might have more than 3 coordinate points, so the amount of list[float, float, float]'s
    produced is (the amount of coordinate points on the row - 2)
    :param text:
    :return points: list[list[float, float, float]]
    """
    nums = []
    points = []

    # parses each line to n*3 floats
    end = len(text)-1
    prev = 17
    while text[prev] != ":":
        prev+=1
    prev+=1
    loc = prev+2
    while True:
        if loc >= end:
            nums.append(float(text[prev:loc]))
            break
        if text[loc] == ",":
            nums.append(float(text[prev+1:loc]))
            prev=loc+1
            loc += 4
        loc += 1

    for i in range(int(len(nums)/3)):
        points.append([nums[i*3], nums[i*3+1], nums[i*3+2]])
        #print("Data type: ", [nums[i*3], nums[i*3+1], nums[i*3+2]])
    return points


def read_data(path: str, max_triangles: int):
    """
    Converts text by BlenderSaveData.py to list of triangles
    :param path: path to the file.txt
    :param max_triangles: reads at most max_triangles
    :return: list[float, float, float]
    """

    triangles = []
    f = open(path, "r")
    count = 0
    for i in f:
        edge = to_coordinates(i)
        if len(edge) < 4:
            triangles.append(edge)
        elif len(edge) == 4:
            triangles.append(edge[0:3])
            triangles.append([edge[0],edge[2],edge[3]])
        count += 1
        if count == max_triangles: break
    return triangles

