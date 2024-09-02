"""
Created on 2020

@author: Rafa Andres (ESAC)

Python module to calculate Jupiter Moon Plasma Torus intercept by a ray spacecraft-to-body
"""

import pandas as pd
import numpy as np
import sys
import argparse
import os


class TorusGenerator:

    jupiter_radius = 69911

    def __init__(self, section_filename):
        self.section_filename = section_filename
        self.read_section()
        self.n_vertices = len(self.dataframe)
        self.n_sections = None
        self.vertices = list()
        self.facets = None

    def read_section(self):
        self.dataframe = pd.read_csv(self.section_filename, sep='\s+', names=['x','y'])

        # Symetric point
        symmetric_df = pd.DataFrame()
        symmetric_df['x'] = self.dataframe['x']
        symmetric_df['y'] = -1 * self.dataframe['y']
        symmetric_df.drop(symmetric_df.tail(1).index, inplace=True)  # drop last n rows
        symmetric_df.drop(symmetric_df.head(1).index, inplace=True)
        print(len(symmetric_df))

        # Reorder the points to get a proper section
        symmetric_df = symmetric_df[::-1]
        self.dataframe = pd.concat([self.dataframe, symmetric_df])
        self.dataframe['z'] = 0

        self.dataframe *= self.jupiter_radius

    @staticmethod
    def rotate_y_axis(vec, theta_rad):
        cos_func, sin_func = np.cos(theta_rad), np.sin(theta_rad)
        y_rotation = np.array(((cos_func, 0, sin_func), (0, 1, 0), (-sin_func, 0, cos_func)))
        new_vector = y_rotation.dot(vec)
        return new_vector[0], new_vector[1], new_vector[2]

    def get_vertices(self, ang_deg):
        return np.apply_along_axis(self.rotate_y_axis, 1, self.dataframe.values, np.radians(ang_deg))

    @staticmethod
    def next_index(n, max_index):
        if n > max_index:
            return n - max_index
        return n

    @staticmethod
    def get_facets(n_sections, n_vertices):
        facet_list = list()
        for section in range(0, int(n_sections)):
            for vertex in range(1, n_vertices + 1):
                v1 = section * n_vertices if vertex % 2 == 1 else ((section + 1) % n_sections) * n_vertices
                v2 = section * n_vertices if vertex % 2 == 0 else ((section + 1) % n_sections) * n_vertices
                v3 = section * n_vertices if vertex % 2 == 1 else ((section + 1) % n_sections) * n_vertices

                if vertex % 2 == 1:
                    facet_list.append((v1 + vertex,
                                   v2 + TorusGenerator.next_index(vertex + 1, n_vertices),
                                   v3 + TorusGenerator.next_index(vertex + 2, n_vertices)))
                else:
                    facet_list.append((v1 + vertex,
                                       v3 + TorusGenerator.next_index(vertex + 2, n_vertices),
                                       v2 + TorusGenerator.next_index(vertex + 1, n_vertices)
                                       ))


        return facet_list

    def generate_torus(self, ang_deg, n_sections=None):

        self.n_sections = np.floor(360 / ang_deg)
        if n_sections:
            self.n_sections = n_sections

        for section in range(0, int(self.n_sections)):
            self.vertices.append(self.get_vertices(section * ang_deg))

        self.facets = self.get_facets(self.n_sections, self.n_vertices)

    def dump_obj(self, out):

        vertices_spec = ""
        facets_spec = ""
        total_vertices = 0
        total_facets = 0
        total_section = 0
        for section in self.vertices:
            for vertex in section:
                # We switch the z and y components
                vertices_spec += 'v %f %f %f\n' % (vertex[0], vertex[2], vertex[1])
                total_vertices += 1

        for facet in self.facets:
            facets_spec += 'f %d %d %d\n' % (facet[0], facet[1], facet[2])
            total_facets += 1

        print('Vertices {vertices} Facets {facets} Sections {sections}'.format(vertices=total_vertices,
                                                                               facets=total_facets,
                                                                               sections=self.n_sections))

        out.write(vertices_spec)
        out.write(facets_spec)


if __name__ == '__main__':

    version = '0.0.1'
    parser = argparse.ArgumentParser(description='Torus generator %s' % version)

    parser.add_argument('-i', metavar='input',
                              help='Section file (Text file of x, y pairs separated with blanks)',
                              required=True)
    parser.add_argument('-a', metavar='angle',
                        help='[Optional] Angle separation in degrees for section revolution', default="5")
    parser.add_argument('-s', metavar='section',
                        help='[Optional] number of section revolution', default=None)
    parser.add_argument('-o', metavar='output',
                        help='[Optional] OBJ output file', default='torus.obj')

    args = parser.parse_args()

    input = args.i
    angle = args.a
    n_sections = args.s
    output = args.o

    if not os.path.exists(input):
        print("The section file does %s not exist" % input)
        exit()

    if angle.isdigit():
        angle = int(angle)
        print(angle)
        if 0 > angle > 120:
            print("The angle shall be an integer between 0 and 120")
            exit()
    else:
        print("The angle shall be an integer between 0 and 120; angle set to {}".format(angle))
        exit()

    if n_sections and not (n_sections.isdigit() and n_sections > 0):
        print("The number of sections shall be an integer great than 0")
        exit()

    t = TorusGenerator(input)

    if n_sections:
        t.generate_torus(angle, int(n_sections))
    else:
        t.generate_torus(angle)

    with open(output, 'w+') as obj_file:
        t.dump_obj(obj_file)