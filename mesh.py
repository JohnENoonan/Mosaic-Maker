"""
    Author: John Noonan
    Purpose: mesh is the container class for storing triangles and edges
"""
import numpy as np
import cv2
import random
import sys
from operator import attrgetter, methodcaller
# import classes
import point as p
import grid2d, queue, shapes, mesh



# mesh is a container class with the methods to create a triangulated mesh used to create final image
class Mesh():
    # constructor takes width and height of image, minimum distance sampled points need to
    # be apart and the number of points to try fitting in the sample before exiting
    def __init__(self, w, h, min_distance, point_count):
        # image dimensions
        self.width = w
        self.height = h
        # store all sampled points and grid of them
        self.samples, self.grid = self.create_samples(min_distance, point_count)

        # dictionary to store triangles
        self.triangles = {}
        # add boundry triangle
        self.triangles['bound'] = shapes.Triangle([p.Point(0, h+1), p.Point(0, -1*h), p.Point(10*w, h+1)])


    # returns a list of points which constitute the random sampling of the image
    # takes the height and width of image, radius, and number of points to try before exiting
    # utilizes Poisson-disk sampling
    def create_samples(self, min_distance, point_count):
    	# create grid to store points for easy look up of collisions
    	grid = grid2d.Grid2d(self.width, self.height, min_distance)
    	# initialize containers
    	process_queue = queue.Queue() # processing queue
    	samples = list() # list of all sampled points
    	# grab first random point
    	first_point = p.Point(random.randint(0,self.width-1), random.randint(0,self.height-1))
    	# add first point to containers
    	process_queue.push(first_point)
    	samples.append(first_point)
    	grid.push(first_point)
    	# iterate through process_queue and add points to sampled. Run until there are no more
    	# points that can be added to sampled
    	while process_queue.not_empty():
    		# grab 1 random point from process_queue
    		point = process_queue.rand_pop()
    		# look for suitable points
    		for i in xrange(point_count):
    			new_point = point.rand_point(min_distance)
    			if new_point.in_image(self.width, self.height) and \
    			    	grid.no_collision(new_point, min_distance):
    				# if new_point is acceptable, both points can be put in process_queue
    				process_queue.push(new_point)
    				process_queue.push(point)
    				# new_point can be added to sampled list and grid
    				samples.append(new_point)
    				grid.push(new_point)
    				# break for loop as a point has been added
    				break
    	return samples, grid
    #TODO implement the add function and any necessary helper functions
    def add_point(self, p):
        a = 1

    # debug function to draw all sampled points on canvas
    def draw_points(self, canvas):
        # draw points
		for i in self.samples:
			# cv2 usese (column, row) position
			cv2.circle(canvas, (i.x,i.y), 3, (0,0,0))
