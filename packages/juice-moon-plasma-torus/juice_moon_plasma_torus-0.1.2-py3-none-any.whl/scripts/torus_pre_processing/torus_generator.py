"""
Created on 2020

@author: Rafa Andres (ESAC)

Python module to calculate Jupiter Moon Plasma Torus intercept by a ray spacecraft-to-body
"""

import math
from numpy import ndarray
import sys


class TorusGenerator:

    def __init__(self, torus_radius, circle_radius, sag):
        self.torus_radius = torus_radius
        self.circle_radius = circle_radius
        self.theta = math.sqrt(sag / self.circle_radius)
        self.phi = math.sqrt(sag / self.torus_radius)
        self.n_vertex_per_circle = int(math.floor(2 * math.pi / self.theta) + 1)
        self.n_circles = int(math.floor(2 * math.pi / self.phi) + 1)
        self.theta = 2 * math.pi / self.n_vertex_per_circle
        self.phi = 2 * math.pi / self.n_circles
        self.vertices = ndarray((3 * self.n_circles * self.n_vertex_per_circle,), float)
        self.normals = ndarray((3 * self.n_circles * self.n_vertex_per_circle,), float)
        self.skip_normals = True

    def __str__(self):
        return 'Torus {}'.format(self.torus_radius)

    def generate(self):
        """
        Creation of the torus representation thanks to the 3d facets.
        We can build a mesh made of nCircles triangles strips, each one
        made of 2*nVertexPerCircle vertices. Indeed, by joining, with strips, the torus circles
        two by two, we can describe the entire torus.
        
        We have to build an array containing the vertices indices, sorted inorder to be parsed as strips vertices.
        """

        for i in range(0, self.n_circles):
            for j in range(0, self.n_vertex_per_circle):

                # vertex  XYZ coordinates
                self.vertices[3 * (self.n_vertex_per_circle * i + j)] = (self.torus_radius + self.circle_radius * math.cos(j * self.theta)) * math.sin(i * self.phi)
                self.vertices[3 * (self.n_vertex_per_circle * i + j) + 1] = self.circle_radius * math.sin(j * self.theta)
                self.vertices[3 * (self.n_vertex_per_circle * i + j) + 2] = (self.torus_radius + self.circle_radius * math.cos(j * self.theta)) * math.cos(i * self.phi)

                # normal vector XYZ components
                self.normals[3 * (self.n_vertex_per_circle * i + j)] = math.cos(j * self.theta) * math.sin(i * self.phi)
                self.normals[3 * (self.n_vertex_per_circle * i + j) + 1] = math.sin(j * self.theta)
                self.normals[3 * (self.n_vertex_per_circle * i + j) + 2] = math.cos(j * self.theta) * math.cos(i * self.phi)

    def to_obj(self, output):
        for vindex in range(0, len(self.vertices), 3):
            output.write('v {} {} {}\n'.format(self.vertices[vindex], self.vertices[vindex+1], self.vertices[vindex+2]))

        for vindex in range(0, len(self.vertices), 3):
            output.write('vn {} {} {}\n'.format(self.normals[vindex], self.normals[vindex + 1], self.normals[vindex + 2]))

        for i in range(0, self.n_circles):
            vertex = ((i * self.n_vertex_per_circle)  + 1)
            output.write('# Circle {} (Init Vertex {}) \n'.format(i, vertex))
            for j in range(0, self.n_vertex_per_circle):
                v1 = vertex if j % 2 == 0 else vertex + self.n_vertex_per_circle
                v2 = vertex if j % 2 == 1 else vertex + self.n_vertex_per_circle
                v3 = vertex if j % 2 == 0 else vertex + self.n_vertex_per_circle
                output.write('f {} {} {} \n'.format(v1 + j, v2 + (j + 1) % self.n_vertex_per_circle, v3 + (j + 2) % self.n_vertex_per_circle))

    def to_mkdsk(self, output):
        for vindex in range(0, len(self.vertices), 3):
            output.write(
                'v {} {} {}\n'.format(self.vertices[vindex], self.vertices[vindex + 1], self.vertices[vindex + 2]))

        for i in range(0, self.n_circles):
            vertex = ((i * self.n_vertex_per_circle) + 1)
            for j in range(0, self.n_vertex_per_circle):
                v1 = vertex if j % 2 == 0 else vertex + self.n_vertex_per_circle
                v2 = vertex if j % 2 == 1 else vertex + self.n_vertex_per_circle
                v3 = vertex if j % 2 == 0 else vertex + self.n_vertex_per_circle
                output.write('f {} {} {} \n'.format(v1 + j, v2 + (j + 1) % self.n_vertex_per_circle,
                                                    v3 + (j + 2) % self.n_vertex_per_circle))


if __name__ == '__main__':
    tg = TorusGenerator(6, 2, 0.065)
    tg.generate()
    with open('torus.txt', 'w+') as f:
        out = sys.stdout
        out = f
        tg.to_mkdsk(f)
