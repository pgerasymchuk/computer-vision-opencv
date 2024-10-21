from graphics import *
import numpy as np

def axonometric_projection(coords, phi, theta):
    matrix_y = np.array(
        [[np.cos(phi), 0 , -np.sin(phi), 0],
         [0, 1, 0, 0],
         [np.sin(phi), 0, np.cos(phi), 1],
         [0, 0, 0, 0]]).T
    new_coords = coords.dot(matrix_y)

    matrix_x = np.array(
        [[1, 0, 0, 0],
         [0, np.cos(theta), np.sin(theta), 0],
         [0, -np.sin(theta),  np.cos(theta), 0],
         [0, 0, 0, 1]]).T
    new_coords = new_coords.dot(matrix_x)

    return new_coords

def projection_xy(coords):
    matrix = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 1]]).T
    return coords.dot(matrix)

def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1
    error, t = el / 2, 0

    x_coords = []
    y_coords = []
    x_coords.append(x)
    y_coords.append(y)

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1

        x_coords.append(x)
        y_coords.append(y)

    return (x_coords, y_coords)

def bezier_curve(x1, y1, x2, y2, n_steps=100):
    p0 = (x1, y1)
    p1 = ((x1 + x2) / 2, (y1 + y2) / 2)
    p2 = (x2, y2)

    x_coords = []
    y_coords = []
    for i in range(n_steps + 1):
        t = i / n_steps
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]

        x_coords.append(x)
        y_coords.append(y)

    return (x_coords, y_coords)

def draw_line(coords, window, color):
    x_coords, y_coords = coords
    if len(x_coords) != len(y_coords):
        print('Length of x_coords and y_coords must be equal')
        return

    for i in range(len(x_coords)):
        obj = Point(x_coords[i], y_coords[i])
        obj.setFill(color)
        obj.draw(window)

def draw_parallelepiped(coords, approx_function, window, color):
    Ax1 = coords[0, 0]
    Ay1 = coords[0, 1]
    Bx1 = coords[1, 0]
    By1 = coords[1, 1]
    Ix1 = coords[2, 0]
    Iy1 = coords[2, 1]
    Mx1 = coords[3, 0]
    My1 = coords[3, 1]

    Dx1 = coords[4, 0]
    Dy1 = coords[4, 1]
    Cx1 = coords[5, 0]
    Cy1 = coords[5, 1]
    Fx1 = coords[6, 0]
    Fy1 = coords[6, 1]
    Ex1 = coords[7, 0]
    Ey1 = coords[7, 1]

    lines = [
        (Ax1, Ay1, Bx1, By1),
        (Bx1, By1, Ix1, Iy1),
        (Ix1, Iy1, Mx1, My1),
        (Mx1, My1, Ax1, Ay1),

        (Dx1, Dy1, Cx1, Cy1),
        (Cx1, Cy1, Fx1, Fy1),
        (Fx1, Fy1, Ex1, Ey1),
        (Ex1, Ey1, Dx1, Dy1),

        (Ax1, Ay1, Bx1, By1),
        (Bx1, By1, Cx1, Cy1),
        (Cx1, Cy1, Dx1, Dy1),
        (Dx1, Dy1, Ax1, Ay1),

        (Mx1, My1, Ix1, Iy1),
        (Ix1, Iy1, Fx1, Fy1),
        (Fx1, Fy1, Ex1, Ey1),
        (Ex1, Ey1, Mx1, My1),

        (Ax1, Ay1, Mx1, My1),
        (Mx1, My1, Ex1, Ey1),
        (Ex1, Ey1, Dx1, Dy1),
        (Dx1, Dy1, Ax1, Ay1),

        (Bx1, By1, Ix1, Iy1),
        (Ix1, Iy1, Fx1, Fy1),
        (Fx1, Fy1, Cx1, Cy1),
        (Cx1, Cy1, Bx1, By1)]

    for line in lines:
        draw_line(approx_function(*line), window, color)


def painter_alg_drawer(faces, approx_function, window, color):
    def avg_z(face):
        return sum(vertex[2] for vertex in face) / len(face)

    sorted_faces = sorted(faces, key=avg_z)

    for face in sorted_faces:
        polygon_points = [Point(point[0], point[1]) for point in face]
        polygon_lines = [
            (face[0][0], face[0][1], face[1][0], face[1][1]),
            (face[1][0], face[1][1], face[2][0], face[2][1]),
            (face[2][0], face[2][1], face[3][0], face[3][1]),
            (face[3][0], face[3][1], face[0][0], face[0][1])
        ]

        polygon = Polygon(polygon_points)
        polygon.setFill("gray")
        polygon.draw(window)

        for line in polygon_lines:
            draw_line(approx_function(*line), window, color)


if __name__ == '__main__':

    width = 500         # width of the window
    height = 500        # height of the window
    x_A = 200           # x coordinate of the first vertex
    y_A = 100           # y coordinate of the first vertex
    z_A = 200           # y coordinate of the first vertex
    side1 = 250         # the length of a side
    side2 = 150         # the length of b side
    side3 = 300         # the length of c side

    win = GraphWin("3D parallelepiped", width, height)
    win.setBackground('white')

    parallelepiped = np.array(
        [[x_A,      y_A,        z_A,        1],
         [x_A+side1, y_A,        z_A,        1],
         [x_A+side1, y_A+side2,  z_A,        1],
         [x_A,       y_A+side2,  z_A,        1],
         [x_A,       y_A,        z_A+side3,  1],
         [x_A+side1, y_A,        z_A+side3,  1],
         [x_A+side1, y_A+side2,  z_A+side3,  1],
         [x_A,       y_A+side2,  z_A+side3,  1]])

    parallelepiped = axonometric_projection(parallelepiped, 0.1, 0.2)
    parallelepiped_xy = projection_xy(parallelepiped)

    faces = [
        (parallelepiped[0], parallelepiped[1], parallelepiped[2], parallelepiped[3]),
        (parallelepiped[4], parallelepiped[5], parallelepiped[6], parallelepiped[7]),
        (parallelepiped[0], parallelepiped[1], parallelepiped[5], parallelepiped[4]),
        (parallelepiped[2], parallelepiped[3], parallelepiped[7], parallelepiped[6]),
        (parallelepiped[0], parallelepiped[3], parallelepiped[7], parallelepiped[4]),
        (parallelepiped[1], parallelepiped[2], parallelepiped[6], parallelepiped[5])
    ]

    draw_parallelepiped(parallelepiped, bresenham, win, 'orange')
    win.getMouse()

    draw_parallelepiped(parallelepiped, bezier_curve, win, 'blue')
    win.getMouse()

    painter_alg_drawer(faces, bresenham, win, 'red')
    win.getMouse()



