"""
	Author: John Noonan
	Purpose: point class used for image simplification
"""
import random
import numpy as np

# point stores a 2d point in a cartesian grid
# init as Point(x_coord, y_coord)

class Point:
	def __init__(self, x_,y_):
		self.x = x_
		self.y = y_
		self.coord = (self.x, self.y)
	# == operator overload
	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)
	# != operator overload
	def __ne__(self, other):
		return (self.x != other.x) or (self.y != other.y)
	# return distance between two points
	def distance(self, p2):
		return np.sqrt((p2.x - self.x)**2 + (p2.y - self.y)**2)
	# boolean to make sure random generated points are within bounds of image size
	def in_image(self, width, height):
		return (self.x >= 0 and self.x <= width) and (self.y >= 0 and self.y <= height)
	# generates a random point about a given point with radius >= r but <= 2r
	def rand_point(self, min_distance):
		# creates a point in polar and converts to cartesian
		angle = random.uniform(0,2*np.pi)
		radius = min_distance + random.uniform(0,min_distance)
		return Point(int(round(self.x + radius*np.cos(angle))), int(round(self.y + radius*np.sin(angle))))
	# calculate grid position in grid based on point
	def convert_point_to_grid(self, cell_size):
		gridX = int((self.x / cell_size));
		gridY = int((self.y / cell_size));
		return (gridY, gridX)
	def __str__(self):
		return "(%d, %d)" %(self.x, self.y)
