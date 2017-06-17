"""
    Author: John Noonan
    Purpose: shapes contains the Edge and Triangle class utilized in main.py
"""
import cv2
import numpy as np
import point as p

# Edge class used to store and draw lines between two Point objects stored in
# a Triangle object
class Edge:
    # init takes 2 Point objects
    def __init__(self, a, b):
        self.points = (a, b)

    def draw_edge(self, img, color):
        cv2.line(img, self.points[0].get_coord(), self.points[1].get_coord(), color)

    def __str__(self):
        return str((str(self.points[0]), str(self.points[1])))

# Triangle stores three Point objects and is used to create a mesh
class Triangle:
    # init takes list of 3 Point objects
    def __init__(self, v_in):
        self.verts = v_in
        # calculate circumcenter and circumradius
        self.center, self.radius = self.get_circle()
        # store edges in list
        self.edges = self.create_edges()

    # function to calculate circumcenter and circum radius
    def get_circle(self):
        # temp variables for coordinates
        aX, aY = self.verts[0].get_xy()
        bX, bY = self.verts[1].get_xy()
        Cx, Cy = self.verts[2].get_xy()

        d = 2 * (aX * (bY - Cy) + bX * (Cy - aY) + Cx * (aY - bY))
        norm_A = aX**2 + aY**2
        norm_B = bX**2 + bY**2
        norm_C = Cx**2 + Cy**2

        uX = norm_A * (bY - Cy) + norm_B * (Cy - aY) + norm_C * (aY - bY)
        uY = -(norm_A * (bX - Cx) + norm_B * (Cx - aX) + norm_C * (aX - bX))

        center = p.Point(uX/d, uY/d)

        radius = center.distance(self.verts[0])
        return center, radius

    # boolean function to determine if a given point is inside the circumcircle
    def in_circle(self, p):
        return p.distance(self.center) <= self.radius

    # creates edges to store
    def create_edges(self):
        list_of_edges = []
        list_of_edges.append(Edge(self.verts[0], self.verts[1]))
        list_of_edges.append(Edge(self.verts[1], self.verts[2]))
        list_of_edges.append(Edge(self.verts[2], self.verts[0]))
        return list_of_edges

    def draw_edges(self, img, color):
        for i in self.edges:
            i.draw_edge(img, color)
