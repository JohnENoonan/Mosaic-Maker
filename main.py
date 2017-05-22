"""
	Author: John Noonan
	Purpose: create a mosaic out of any given image
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
# utilizes Poisson-disk sampling
def create_samples(height, width, min_distance, point_count):
	# create grid to store points for easy look up of collisions
	grid = grid2d.Grid2d(width, height, min_distance)
	# initialize containers
	process_queue = queue.Queue() # processing queue
	samples = list() # list of all sampled points
	# grab first random point
	first_point = p.Point(random.randint(0,width-1), random.randint(0,height-1))
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
			if new_point.in_image(width, height) and \
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


def create_delaunay(img, min_distance=10, point_count=10):
	# create dimesnion variables
	height = 400
	width = 400
	# new image name
	image_name = "test.png"
	# generate random points
	samples, grid = create_samples(height, width, 30, point_count)
	# create canvas
	canvas = np.zeros((height,width, 3), np.uint8)
	canvas[:,:] = (255,255,255) # assign white background
	# draw points
	for i in samples:
		# cv2 usese (column, row) position
		cv2.circle(canvas, (i.x,i.y), 3, (0,0,0))
	# sort sampled points
	samples.sort(key=attrgetter('x', 'y'))
	print len(samples)
	# create list of lists of 3 points to create preliminary triangles.
	if len(samples) % 3 != 1:
		points = [samples[x:x+3] for x in xrange(0, len(samples), 3)]
	# if there is a list of just 1 point readjust to have two lists with 2
	else:
		points = [samples[x:x+3] for x in xrange(0, len(samples)-4, 3)]
		points.append([samples[-4], samples[-3]])
		points.append([samples[-2], samples[-1]])
	print len(points)
	tri_list = []
	for i in xrange(len(points)):
		tri_list.append(shape.Triangle(points[i]))
		for j in points[i]:
			print j
		tri_list[i].draw_edges(canvas, (0,0,0))
	cv2.imwrite("test.png",canvas)

# testing function to draw out all points
def draw_mesh(image, min_distance, canvas, point_count=5):
	samples = create_samples(image.shape[0], image.shape[1], min_distance, point_count)
	canvas = np.zeros((400, 400,3), np.uint8)
	canvas[:,:] = (255,255,255)
	for i in samples:
		print str(i)
		cv2.circle(canvas, (i.x,i.y), 0, (0,0,0))

# testing funtion to test triangulation
def test():
	height = 400
	width = 400
	canvas = np.zeros((height,width, 3), np.uint8)
	canvas[:,:] = (255,255,255)
	points = []
	for i in xrange(5):
		points.append(p.Point(random.randint(0,width), random.randint(0, height)))
		print str(points[i])
		#cv2.circle(canvas, (points[i].y,points[i].x), 0, (0,0,0))
	points.sort(key=attrgetter('x', 'y'))
	preTris = [points[x:x+3] for x in xrange(0, len(points), 3)]
	tri_list = []
	for i in xrange(len(preTris)):
		tri_list.append(shape.Triangle(preTris[i]))
		tri_list[i].draw_edges(canvas, (0,0,0))
	cv2.imwrite("test1.png",canvas)


#### main ####
if __name__ == "__main__":
	min_distance = 10
	# load  image
	img = cv2.imread("cv_img.png")
	# store copy
	img_orig = img.copy()
	create_delaunay(img)
	#test()
	#draw_mesh(img, min_distance)
	"""cv2.imshow("image window", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()"""
