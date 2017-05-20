"""
    Author: John Noonan
    Purpose: shapes contains the Edge and Triangle class utilized in experiment.py
"""
from operator import attrgetter, methodcaller
import cv2

class Edge:
    # init takes 2 Point objects
    def __init__(self, a, b):
        self.points = (a, b)
    def draw_edge(self, img, color):
        #print str(self.points[0]) + ': ' + str(self.points[1])
        cv2.line(img, self.points[0].coord, self.points[1].coord, color)
class Triangle:
    # init takes list of 3 or 2 Point objects
    def __init__(self, verts_input):
        # assign vertices
        self.verts = [None, None, None]
        self.verts[0] = verts_input[0]
        if len(verts_input) == 2:
            self.verts[1] = verts_input[1]
            self.verts[2] = None
        else:
            self.verts[1] = max(verts_input[1], verts_input[2], key=attrgetter('x','y'))
            if self.verts[1] == verts_input[1]:
                self.verts[2] = verts_input[2]
            else:
                self.verts[2] = verts_input[1]
        # store edges
        self.edges = self.create_edges()
        self.edge_size = len(self.edges)
    # creates edges to store
    def create_edges(self):
        list_of_edges = []
        if len(self.verts) == 3:
            list_of_edges.append(Edge(self.verts[0], self.verts[1]))
            list_of_edges.append(Edge(self.verts[1], self.verts[2]))
            list_of_edges.append(Edge(self.verts[2], self.verts[0]))
        else:
            list_of_edges.append(Edge(self.verts[0], self.verts[1]))
        return list_of_edges
    def draw_edges(self, img, color):
        for i in self.edges:
            i.draw_edge(img, color)
