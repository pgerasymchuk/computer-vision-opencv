import os
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def load_obj(filename):
    vertices = []
    textures = []
    normals = []
    faces = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vt '):
                textures.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                face = [list(map(int, part.split('/'))) for part in line.strip().split()[1:]]
                for k in range(1, len(face) - 1):
                    faces.append([face[0], face[k], face[k + 1]])

    return vertices, textures, normals, faces

def load_mtl(filename):
    materials = {}
    current_material = None

    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if parts[0] == 'newmtl':
                current_material = parts[1]
                materials[current_material] = {}
            elif parts[0] == 'Ka':
                materials[current_material]['Ka'] = list(map(float, parts[1:]))
            elif parts[0] == 'Kd':
                materials[current_material]['Kd'] = list(map(float, parts[1:]))
            elif parts[0] == 'Ks':
                materials[current_material]['Ks'] = list(map(float, parts[1:]))
            elif parts[0] == 'map_Kd':
                materials[current_material]['map_Kd'] = parts[1]

    return materials

def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)

    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

def draw_model(vertices, textures, faces, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_TRIANGLES)

    for face in faces:
        for i in range(len(face)):
            vertex = vertices[face[i][0] - 1]
            texture = textures[face[i][1] - 1] if face[i][1] - 1 < len(textures) else [0.0, 0.0]
            glTexCoord2f(*texture)
            glVertex3f(*vertex)

    glEnd()

def animate():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-3, 0.0, -8)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    obj_file = os.path.join(base_dir, "model.obj")
    mtl_file = os.path.join(base_dir, "model.mtl")
    texture_file = os.path.join(base_dir, "texture.jpg")

    vertices, textures, normals, faces = load_obj(obj_file)
    materials = load_mtl(mtl_file)
    texture_id = load_texture(texture_file)

    clock = pygame.time.Clock()
    glRotatef(80, 0, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glTranslate(0, 0, 0.05)
        glRotatef(0.5, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_model(vertices, textures, faces, texture_id)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    animate()
