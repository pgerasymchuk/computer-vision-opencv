# Variant 4
# Figure - parallelepiped

import numpy as np
from graphics import *

def generate_colors(start_color, end_color, steps):
    start_r = int(start_color[1:3], 16)
    start_g = int(start_color[3:5], 16)
    start_b = int(start_color[5:7], 16)

    end_r = int(end_color[1:3], 16)
    end_g = int(end_color[3:5], 16)
    end_b = int(end_color[5:7], 16)

    color_list = []
    for i in range(steps):
        r = round(start_r + (end_r - start_r) * i / (steps - 1))
        g = round(start_g + (end_g - start_g) * i / (steps - 1))
        b = round(start_b + (end_b - start_b) * i / (steps - 1))

        color_list.append(f'#{r:02x}{g:02x}{b:02x}')

    return color_list


class FigureOperations:
    def translate(self, coords, dx, dy, dz):
        matrix = np.array([ [1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1] ]).T
        new_coords = coords.dot(matrix)
        return new_coords

    def rotate_around_x_axis(self, coords, theta):
        matrix = np.array([[1, 0, 0, 0],
                           [0, np.cos(theta), np.sin(theta), 0],
                           [0, -np.sin(theta),  np.cos(theta), 0],
                           [0, 0, 0, 1]]
                          ).T
        return coords.dot(matrix)

    def rotate_around_y_axis(self, coords, phi):
        matrix = np.array([[np.cos(phi), 0 , -np.sin(phi), 0],
                           [0, 1, 0, 0],
                           [np.sin(phi), 0, np.cos(phi), 0],
                           [0, 0, 0, 1]]
                          ).T
        return coords.dot(matrix)

    def axonometric_projection(self, coords, phi, theta):
        return self.rotate_around_y_axis(self.rotate_around_x_axis(coords, theta), phi)


class Parallelepiped:
    def __init__(self, win, figure_op, x_A, y_A, z_A, side1, side2, side3):
        self.win = win
        self.figure_op = figure_op
        self.coords = np.array(
            [[x_A,      y_A,        z_A,        1],
             [x_A+side1, y_A,        z_A,        1],
             [x_A+side1, y_A+side2,  z_A,        1],
             [x_A,       y_A+side2,  z_A,        1],
             [x_A,       y_A,        z_A+side3,  1],
             [x_A+side1, y_A,        z_A+side3,  1],
             [x_A+side1, y_A+side2,  z_A+side3,  1],
             [x_A,       y_A+side2,  z_A+side3,  1]])

        self.faces = []
        self.edges = []
        self.colors = (generate_colors("#FFFF00", "#00FFFF", 16) +
                       generate_colors("#00FFFF", "#FFFFFF", 16) +
                       generate_colors("#FFFFFF", "#FFFF00", 16))
        self.current_color_num = 0

    def draw(self, remove_old_drawing = True):
        if remove_old_drawing:
            for obj in self.faces:
                obj.undraw()
            for obj in self.edges:
                obj.undraw()
        Ax = self.coords[0, 0];  Ay = self.coords[0, 1]
        Bx = self.coords[1, 0];  By = self.coords[1, 1]
        Ix = self.coords[2, 0];  Iy = self.coords[2, 1]
        Mx = self.coords[3, 0];  My = self.coords[3, 1]

        Dx = self.coords[4, 0];  Dy = self.coords[4, 1]
        Cx = self.coords[5, 0];  Cy = self.coords[5, 1]
        Fx = self.coords[6, 0];  Fy = self.coords[6, 1]
        Ex = self.coords[7, 0];  Ey = self.coords[7, 1]

        self.faces = [Polygon(Point(Ax, Ay), Point(Bx, By), Point(Ix, Iy), Point(Mx, My)),
                        Polygon(Point(Dx, Dy), Point(Cx, Cy), Point(Fx, Fy), Point(Ex, Ey)),
                        Polygon(Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy)),
                        Polygon(Point(Mx, My), Point(Ix, Iy), Point(Fx, Fy), Point(Ex, Ey)),
                        Polygon(Point(Ax, Ay), Point(Mx, My), Point(Ex, Ey), Point(Dx, Dy)),
                        Polygon(Point(Bx, By), Point(Ix, Iy), Point(Fx, Fy), Point(Cx, Cy))]
        self.edges = [Line(Point(Ax, Ay), Point(Bx, By)),
                      Line(Point(Bx, By), Point(Ix, Iy)),
                      Line(Point(Ix, Iy), Point(Mx, My)),
                      Line(Point(Mx, My), Point(Ax, Ay)),
                      Line(Point(Dx, Dy), Point(Cx, Cy)),
                      Line(Point(Cx, Cy), Point(Fx, Fy)),
                      Line(Point(Fx, Fy), Point(Ex, Ey)),
                      Line(Point(Ex, Ey), Point(Dx, Dy)),
                      Line(Point(Ax, Ay), Point(Dx, Dy)),
                      Line(Point(Bx, By), Point(Cx, Cy)),
                      Line(Point(Ix, Iy), Point(Fx, Fy)),
                      Line(Point(Mx, My), Point(Ex, Ey))]

        self.current_color_num = (self.current_color_num + 1) % len(self.colors)

        for obj in self.faces:
            obj.draw(self.win)
            obj.setFill(self.colors[self.current_color_num])

        for obj in self.edges:
            obj.draw(self.win)

    def rotate_around_x(self, theta):
        self.coords = self.figure_op.rotate_around_x_axis(self.coords, theta)
        self.draw()

    def rotate_around_y(self, phi):
        self.coords = self.figure_op.rotate_around_y_axis(self.coords, phi)
        self.draw()

    def rotate_around_centre_y_axis(self, phi):
        x_centre, y_centre, z_centre, _ = (self.coords[0] + self.coords[6]) / 2
        self.coords = self.figure_op.translate(self.coords, -x_centre, -y_centre, -z_centre)
        self.coords = self.figure_op.rotate_around_y_axis(self.coords, phi)
        self.coords = self.figure_op.translate(self.coords, x_centre, y_centre, z_centre)

        old_coords = self.coords
        self.coords = self.figure_op.axonometric_projection(self.coords, 0.1, 0.2)
        self.draw()
        self.coords = old_coords


width = 500         # width of the window
height = 500        # height of the window
x0 = 200            # x coordinate of the first vertex
y0 = 100            # y coordinate of the first vertex
z0 = 200            # y coordinate of the first vertex
a = 100             # the length of a side
b = 150             # the length of b side
c = 250             # the length of c side



window = GraphWin("3-D parallelepiped", width, height)
window.setBackground('white')

p = Parallelepiped(window, FigureOperations(), x0, y0, z0, a, b, c)

while 1:
    time.sleep(0.05)
    p.rotate_around_centre_y_axis(0.2)
