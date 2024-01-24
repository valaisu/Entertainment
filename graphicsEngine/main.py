# Basic idea #

# CREATE A PLANE

# Select viewpoint                  P
# Select view direction             Dw
# Select focus distance             Df

# Df and Dw give the focus point    FP

# Select view angles (let's at first assume that the camera
# cannot be tilted, so it is enough to choose two angles
# which are width*height            alpha, beta

# A plane orthogonal to the line between P and FP
# can be created, which will have dimensions of
# width/height =                    sin(alpha)/sin(beta)

# PROJECT POINTS ON THE PLANE

# The plane can be defined by 2 points:
# c = The center of the plane
# d = the "direction" of the plane, such that line
# c-d is orthogonal to the plane

# Should be able to be made with a single linear transformation
# Apply linear transformation


# Determine the drawing order #

# for each triangle
#   calculate np = the point nearest to the camera
# order triangles by np from farthest to closest and
# draw in that order

# Does not attain perfect results, but seems quick
# and in most cases reliable.

# improvement ideas: Use more numpy


import pygame
import numpy as np
from openData import read_data


def angle_between_vectors():
    pass


def plane_color(vectors: list[list[float, float, float]], sun: list[float, float, float]):
    """
    Calculates the color of the plane based on the angle between the
    normal vector of the plane and the sun.
    :param vectors: describe the plane
    :param sun: describe the sun
    :return color: tuple(int, int, int)
    """

    point1 = np.array(vectors[0])
    point2 = np.array(vectors[1])
    point3 = np.array(vectors[2])
    s = np.array(sun)

    # Calculate vectors A and B lying in the plane
    vector_A = point2 - point1
    vector_B = point3 - point1

    # Calculate the normal vector to the plane by taking the cross product of A and B
    normal_vector = np.cross(vector_A, vector_B)

    # Normalize the normal vector to obtain a unit vector
    normal_vector /= np.linalg.norm(normal_vector)
    dot_product = np.dot(normal_vector, s)

    # Calculate the magnitudes of the vectors
    magnitude_A = np.linalg.norm(normal_vector)
    magnitude_B = np.linalg.norm(s)

    # Calculate the angle in radians
    # Min necessary, as sometimes rounding errors cause
    # dot_product / (magnitude_A * magnitude_B) to be
    # over 1 (which is impossible)
    angle_rad = np.arccos(min(dot_product / (magnitude_A * magnitude_B),1))

    m = np.abs(np.cos(angle_rad))
    val = 50 + m*120
    color = (val, val, val)
    return color


def rotate_towards_pos_z(camera_vector: list[float], faces: list[list[list[float]]]):
    """
    Rotates the faces around the origo so that the camera points at positive z axis.
    Improvement idea: add param to control the point around which the points are rotated.
    :param camera_vector: the location of the camera
    :param faces: list of the faces
    :return:
    """

    # Calculate the rotation angles
    theta_x = np.arctan2(camera_vector[1], camera_vector[0])
    theta_y = np.arctan2(np.sqrt(camera_vector[0]**2 + camera_vector[1]**2), camera_vector[2])
    # Create rotation matrices
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(theta_x), -np.sin(theta_x)],
                   [0, np.sin(theta_x), np.cos(theta_x)]])
    Ry = np.array([[np.cos(theta_y), 0, np.sin(theta_y)],
                   [0, 1, 0],
                   [-np.sin(theta_y), 0, np.cos(theta_y)]])

    # Apply the rotations
    rotated_vectors = [[np.dot(np.dot(Ry, Rx), i) for i in vectors] for vectors in faces]
    return rotated_vectors


def move_to_xy_plane(camera_dist, triangles):
    """
    Moves particles on xy-plane. Before this triangles and the camera must
    have been rotated around origo so that camera is at [0, 0, dist]
    :param camera_dist: int
    :param triangles: list[float, float, float]
    :return: list[float, float, float]
    """
    #
    for i in range(len(triangles)):
        for j in range(3):
            triangles[i][j][0] += triangles[i][j][0] * triangles[i][j][2] / (camera_dist - triangles[i][j][2])
            triangles[i][j][1] += triangles[i][j][1] * triangles[i][j][2] / (camera_dist - triangles[i][j][2])
    return triangles


def drawing_order_m2(triangles: np.ndarray, camera_loc: list[float, float, float]):
    """
    Sorts the triangles based on the distance between the farthest point and the camera
    :param triangles:
    :param camera_loc:
    :return:
    """
    triangles = sorted(triangles, key=lambda x:
        np.power((x[0][0] + x[1][0] + x[2][0]) / 3 - camera_loc[0], 2) +
        np.power((x[0][1] + x[1][1] + x[2][1]) / 3 - camera_loc[1], 2) +
        np.power((x[0][2] + x[1][2] + x[2][2]) / 3 - camera_loc[2], 2)
    )
    return triangles


def move_and_scale(camera_height_angle: float, camera_width_angle: float, dist: float,
                   display_w: float, display_h: float, faces: list[list[list[float]]]):

    """
    Scales and moves the faces based on the camera location
    :param camera_height_angle: camera angle in radians
    :param camera_width_angle: camera angle in radians
    :param dist: camera distance from origo
    :param display_w: display width on screen
    :param display_h: display height on screen
    :param faces: list of the triangles/faces
    :return: list[list[list[float]]]
    """
    h = np.sin(camera_height_angle)*dist
    w = np.sin(camera_width_angle)*dist
    scale_h = display_h/h
    scale_w = display_w/w
    for row in faces:
        for tri in row:
            tri[0] = display_w/2+(tri[0])*scale_w
            tri[1] = display_h/2+(tri[1])*scale_h
    return faces


def drawing_list(camera_loc: list[float, float, float], camera_angle_w, camera_angle_h, triangles, display_w, display_h, sun_direction):
    """
    Runs all transformations needed to draw the faces on
    a 2D surface
    :param camera_loc: camera location in carthesian coordinates
    :param camera_angle_w: camera width in radians
    :param camera_angle_h: camera height in radians
    :param triangles: list of the triangles/faces
    :param display_w: display width on screen
    :param display_h: display height on screen
    :param sun_direction: vector describing the direction of the sun
    :return:
    """
    dist = np.sqrt(np.power(camera_loc[0], 2)+np.power(camera_loc[1], 2)+np.power(camera_loc[2], 2))
    ordered = drawing_order_m2(triangles, camera_loc)

    colors = [plane_color(i, sun_direction) for i in ordered]

    rotated = rotate_towards_pos_z(camera_loc, ordered)
    flattened = move_to_xy_plane(dist, rotated)
    scaled = move_and_scale(camera_angle_h, camera_angle_w, dist, display_w, display_h, flattened)
    return scaled, colors


# EDIT THE DISPLAY RESULTS HERE
drawObject = read_data("data.txt", 10000)
camera_location = [0,1,3]
camera_w = np.pi/6
camera_h = np.pi/6
display_width = 800
display_height = 800
center = [display_width/2, display_height/2]
sun_dir = [1, 3, 1]

draws, cols = drawing_list(camera_location, camera_w, camera_h, drawObject, display_width, display_height, sun_dir)

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("3D engine")

clock = pygame.time.Clock()

crashed = False
count = 0
while not crashed:
    if count < len(draws):
        count += 1
    gameDisplay.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    color_count = 0
    for i in draws[:count]:
        pygame.draw.polygon(gameDisplay, cols[color_count], [(i[0][0], i[0][1]), (i[1][0], i[1][1]), (i[2][0], i[2][1])])
        color_count += 1
    pygame.display.update()
    #clock.tick(1)

pygame.quit()
quit()
