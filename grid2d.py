"""
	Author: John Noonan
	Purpose: Grid2d class used for image simplification
"""
import numpy as np

# Grid2d stores the grids of the image for easy lookup where
# each cell can only contain 1 point. look up time is 0(1) when position is known
class Grid2d:
	# create 2d list with all elements set to none given image width and height as ints and min_distance between points
	def __init__(self, img_width, img_height, min_distance):
		self.cell_size = min_distance/np.sqrt(2)
		self.width = int(np.ceil(img_width/self.cell_size))
		self.height = int(np.ceil(img_height/self.cell_size))
		# grid is 2d array with all elements set to none
		self.grid = []
		for i in xrange(self.height):
			self.grid.append([])
			self.grid[i] = [None]*self.width
	# push takes the point and a tuple in form (y_coord, x_coord)
	def push(self, point):
		cell = point.convert_point_to_grid(self.cell_size)
		#print str(cell) + ": " + "(" + str(self.width) + ", " + str(self.height) + ")"
		self.grid[cell[0]][cell[1]] = point
	# boolean function to determine if there are no collisions between the new_point and
	# any already sampled points. takes the newly sampled point and the cell it would occupy
	# as well as the min distance the points need to be from each other
	def no_collision(self, point, sampled_cell, min_distance):
		# starting points for search. subtract 2 so as to start search 2 cells left of sampled
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
					# print self.grid[y+i][x+j]
					if point.distance(self.grid[y+i][x+j]) < min_distance:
						return False
		return True
