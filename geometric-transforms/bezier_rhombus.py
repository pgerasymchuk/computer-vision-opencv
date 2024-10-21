from graphics import *
import numpy as np



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

def bezier_curve(x1, y1, x2, y2, n_steps=500):
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

def draw_polygon(coords, approx_function, window, color):
    lines = [
        (coords[0][0], coords[0][1], coords[1][0], coords[1][1]),
        (coords[1][0], coords[1][1], coords[2][0], coords[2][1]),
        (coords[2][0], coords[2][1], coords[3][0], coords[3][1]),
        (coords[3][0], coords[3][1], coords[0][0], coords[0][1])
    ]

    for line in lines:
        draw_line(approx_function(*line), window, color)


if __name__ == '__main__':

    width = 500             # width of the window
    height = 500            # height of the window
    x_A = 50; y_A = 310     # rhombus coordinates
    x_B = 170; y_B = 150
    x_C = 370; y_C = 150
    x_D = 250; y_D = 310

    win = GraphWin("2D rhombus", width, height)
    win.setBackground('white')

    rhombus = np.array([[x_A, y_A, 1],
                        [x_B, y_B, 1],
                        [x_C, y_C, 1],
                        [x_D, y_D, 1]])

    draw_polygon(rhombus, bresenham, win, 'orange')
    win.getMouse()

    draw_polygon(rhombus, bezier_curve, win, 'blue')
    win.getMouse()
