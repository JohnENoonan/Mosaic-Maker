"""
	Author: John Noonan
	Purpose: Grid2d class used for to speed up point accessing in raduis searches
"""
import numpy as np
import shapes
import cv2

# Grid2d stores cells making up the image for easy lookup where
# each cell can only contain 1 point. look up time is 0(1) when position is known
class Grid2d:
	# create 2d list with all elements set to none given image width and height as ints and min_distance between points
	def __init__(self, img_width, img_height, min_distance):
		# use pythagorean property of sprt(2) to get even squares
		self.cell_size = min_distance/np.sqrt(2)
		# get dimensions of 2d array
		self.width = int(np.ceil(img_width/self.cell_size))
		self.height = int(np.ceil(img_height/self.cell_size))
		# grid is 2d list with all elements set to none
		self.grid = []
		for i in xrange(self.height):
			self.grid.append([])
			self.grid[i] = [None]*self.width

	# push takes Point object as input
	def push(self, point):
		cell = point.convert_point_to_grid(self.cell_size)
		# cell = (y_coord, x_coord)
		self.grid[cell[0]][cell[1]] = point

	# boolean function to determine if there are no collisions between the new_point and
	# any already sampled points. takes the newly sampled point
	# as well as the min distance the points need to be from each other
	def no_collision(self, point, min_distance):
		# get cell that point would occupy
		sampled_cell = point.convert_point_to_grid(self.cell_size)
		# starting points for search. subtract 2 so as to start search
		# 2 cells left and down of sampled
		y = sampled_cell[0]-2
		x = sampled_cell[1]-2
		# iterate through every cell that could contain a collision
		for i in xrange(5):
			# if row not inbounds skip to next row
			if (y + i < 0) or (y + i > (self.height-1)):
				continue
			for j in xrange(5):
				# if column not inbounds skip to next column
				if (x + j < 0) or (x + j > (self.width-1)):
					continue
				# if cell is occupied check distance
				if self.grid[y+i][x+j] is not None:
					# if points are too close return false
					if point.distance(self.grid[y+i][x+j]) < min_distance:
						return False
		return True
