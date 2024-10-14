# Variant 4
# Figure - rhombus

from graphics import *
import numpy as np

class PolygonOperations:
    def translate_polygon(self, coords, dx, dy):
        matrix = np.array([ [1, 0, dx], [0, 1, -dy], [0, 0, 1] ])
        matrix_t = matrix.T
        new_coords = coords.dot(matrix_t)
        return new_coords

    def rotate_polygon(self, coords, theta):
        matrix = np.array([ [np.cos(theta), -np.sin(theta), 0],
                            [np.sin(theta), np.cos(theta), 0],
                            [0, 0, 1]])
        matrix_t = matrix.T
        new_coords = coords.dot(matrix_t)
        return new_coords

    def scale_polygon(self, coords, scale_x, scale_y):
        matrix = np.array([[scale_x, 0, 0],
                           [0, scale_y, 0],
                           [0, 0, 1]])
        matrix_t = matrix.T
        new_coords = coords.dot(matrix_t)
        return new_coords

class Rhombus:
    def __init__(self, win, polygon_op, x_center, y_center, side, alphaR):
        # half of the diagonal, opposite to the alpha angle
        d1_half = side * np.sin(alphaR / 2)
        # half of the diagonal, adjacent to the alpha angle
        d2_half = side * np.cos(alphaR / 2)

        self.win = win
        self.polygon_op = polygon_op
        self.coords = np.array([[x_center - d1_half, y_center, 1],
                                [x_center, y_center - d2_half, 1],
                                [x_center + d1_half, y_center, 1],
                                [x_center, y_center + d2_half, 1]])

        self.obj = Polygon([Point(x, y) for x, y, _ in self.coords])

    def draw(self, remove_old_drawing = False):
        if remove_old_drawing:
            self.obj.undraw()
        self.obj = Polygon([Point(x, y) for x, y, _ in self.coords])
        self.obj.draw(self.win)

    def translate(self, dx, dy):
        self.coords = self.polygon_op.translate_polygon(self.coords, dx, dy)
        self.draw()

    def rotate(self, theta):
        self.coords = self.polygon_op.rotate_polygon(self.coords, theta)
        self.draw()

    def scale(self, scale):
        self.coords = self.polygon_op.scale_polygon(self.coords, scale, scale)
        self.draw()


width = 1000        # width of the window
height = 1000       # height of the window
x0 = width / 4      # x coordinate of the rhombus centre
y0 = height / 4     # y coordinate of the rhombus centre
a = 50              # the length of the rhombus side
alphaR = 2.5        # the angle of the rhombus in radians

window = GraphWin("2-D rhombus", width, height)
window.setBackground("white")
r = Rhombus(window, PolygonOperations(), x0, y0, a, alphaR)
r.draw()

iterations = 5

for i in range(iterations):
    time.sleep(0.3)
    r.scale(1.2)

for i in range(iterations):
    time.sleep(0.3)
    r.rotate(-0.1)

for i in range(iterations):
    time.sleep(0.3)
    r.translate(-10, 20)


window.getMouse()
window.close()


