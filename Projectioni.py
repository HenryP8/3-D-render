import pygame
import numpy as np
import math

HEIGHT = 500
WIDTH = 500
black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
running = True
clock = pygame.time.Clock()

triangles = []

PROJECTION_ARRAY = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 0]])

theta = 0.1   # In degrees
ROTATION_X_ARRAY = np.array([[1, 0, 0],
                             [0, math.cos(theta), -math.sin(theta)],
                             [0, math.sin(theta), math.cos(theta)]])
ROTATION_Y_ARRAY = np.array([[math.cos(theta), 0, math.sin(theta)],
                             [0, 1, 0],
                             [-math.sin(theta), 0, math.cos(theta)]])
ROTATION_Z_ARRAY = np.array([[math.cos(theta), -math.sin(theta), 0],
                             [math.sin(theta), math.cos(theta), 0],
                             [0, 0, 1]])


class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.v = np.array([x, y, z])

    def project(self):
        self.v = np.matmul(PROJECTION_ARRAY, self.v)

    def rotate_x(self):
        self.v = np.matmul(ROTATION_X_ARRAY, self.v)
        self.x = self.v[0]
        self.y = self.v[1]
        self.z = self.v[2]

    def rotate_y(self):
        self.v = np.matmul(ROTATION_Y_ARRAY, self.v)
        self.x = self.v[0]
        self.y = self.v[1]
        self.z = self.v[2]

    def rotate_z(self):
        self.v = np.matmul(ROTATION_Z_ARRAY, self.v)
        self.x = self.v[0]
        self.y = self.v[1]
        self.z = self.v[2]

    def return_coord(self):
        return self.v[0], self.v[1]

    def center(self):
        self.v[0] += WIDTH / 2
        self.v[1] += HEIGHT / 2

    def to_origin(self):
        self.v[0] = self.x
        self.v[1] = self.y
        self.v[2] = self.z


class Triangle:

    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        triangles.append(self)

    def rotate_x(self):
        self.v1.rotate_x()
        self.v2.rotate_x()
        self.v3.rotate_x()

    def rotate_y(self):
        self.v1.rotate_y()
        self.v2.rotate_y()
        self.v3.rotate_y()

    def rotate_z(self):
        self.v1.rotate_z()
        self.v2.rotate_z()
        self.v3.rotate_z()

    def project(self):
        self.v1.project()
        self.v2.project()
        self.v3.project()

    def center(self):
        self.v1.center()
        self.v2.center()
        self.v3.center()

    def to_origin(self):
        self.v1.to_origin()
        self.v2.to_origin()
        self.v3.to_origin()


def create_triangle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    v_temp1 = Vector(x1, y1, z1)
    v_temp2 = Vector(x2, y2, z2)
    v_temp3 = Vector(x3, y3, z3)

    triangle = Triangle(v_temp1, v_temp2, v_temp3)


create_triangle(100, 100, 0, -100, -100, 0, 140, -140, 0)
create_triangle(100, 100, 0, -100, -100, 0, 100, -100, 140)
create_triangle(100, 100, 0, 140, -140, 0, 100, -100, 140)
create_triangle(-100, -100, 0, 140, -140, 0, 100, -100, 140)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    for t in triangles:
        t.to_origin()
        t.rotate_x()
        t.rotate_y()
        t.rotate_z()
        t.project()
        t.center()
        pygame.draw.polygon(screen, white, [t.v1.return_coord(), t.v2.return_coord(), t.v3.return_coord()], 1)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
