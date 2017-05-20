"""
	Author: John Noonan
	Purpose: experiment with Poisson-disk sampling
"""
#### Inclusions ####
import numpy as np
import cv2
import random
import sys
from operator import attrgetter, methodcaller
# import classes
import point as p
import shapes as shape
import grid2d, queue

debug = False

#### Functions ####
# returns a list of points which constitute the random sampling of the image
# takes the height and width of image, radius, and number of points to try before exiting
def create_samples(height, width, min_distance, point_count):
	# create grid to store points for easy look up of collisions
	grid = grid2d.Grid2d(width, height, min_distance)
	# containers
	process_queue = queue.Queue() # processing queue
	samples = list() # list of all sampled points
	# first random point
	first_point = p.Point(random.randint(0,width-1), random.randint(0,height-1))
	# add first point to containers
	process_queue.push(first_point)
	samples.append(first_point)
	grid.push(first_point)
	# iterate through process_queue and add points to sampled
	while process_queue.not_empty():
		point = process_queue.pop_()
		# look for suitable points
		for i in xrange(point_count):
			new_point = point.rand_point(min_distance)
			if new_point.in_image(width, height) and \
			    grid.no_collision(new_point, new_point.convert_point_to_grid(grid.cell_size), \
				min_distance):
				# if a point is found both points can be put in process_queue
				process_queue.push(new_point)
				process_queue.push(point)
				# new point can be added to sampled list
				samples.append(new_point)
				# add new_point to grid
				grid.push(new_point)
				# break for loop as a point has been added
				break
	return samples


def create_delaunay(img, min_distance=10, point_count=10):
	# generate random points
	samples = create_samples(img.shape[0], img.shape[1], min_distance, point_count)
	canvas = np.zeros((400, 400,3), np.uint8)
	canvas[:,:] = (255,255,255)
	samples.sort(key=attrgetter('x', 'y'))
	# create list of lists of 3 points to create preliminary triangles.
	# If not possible make remaining lists size 2
	points = [samples[x:x+3] for x in xrange(0, len(samples), 3)]
	if len(points[len(points)-1]) == 1:
		temp_points = (points[len(points)-2][2], points[len(points)-1][0])
		points[len(points)-2] = points[len(points)-2][0:2]
		points[len(points)-1] = [temp_points[0], temp_points[1]]
	tri_list = []
	print str(points[len(points)-1])
	for i in xrange(len(points)):
		tri_list.append(shape.Triangle(points[i]))
		tri_list[i].draw_edges(img, (0,0,0))
	cv2.imwrite("cv_img.png",canvas)


def draw_mesh(image, min_distance, point_count=5):
	samples = create_samples(400, 400, min_distance, point_count)
	canvas = np.zeros((400, 400,3), np.uint8)
	canvas[:,:] = (255,255,255)
	for i in samples:
		#print i
		cv2.circle(canvas, (i.x,i.y), 0, (0,0,0))
	cv2.imwrite("cv_img.png",canvas)
	s = cv2.Subdiv2d()




# main
if __name__ == "__main__":
	min_distance = 10
	# load  image
	img = cv2.imread("cv_img.png")
	# store copy
	img_orig = img.copy()
	create_delaunay(img)
	#draw_mesh(img, min_distance)
	"""cv2.imshow("fuck bitches", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()"""
