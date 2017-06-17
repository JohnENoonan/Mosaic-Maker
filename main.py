"""
	Author: John Noonan
	Purpose: create a mosaic out of any given image
"""
#### Inclusions ####
import numpy as np
import cv2
import random
import sys

import mesh

debug = True

#### Functions ####
def create_delaunay(img, min_distance=10, point_count=10):
	# create dimesnion variables
	height = 400
	width = 400
	# new image name
	image_name = "test.png"
	# create Mesh container to store data and call methods from
	delaunay  = mesh.Mesh(width, height, min_distance, point_count)
	# create canvas
	canvas = np.zeros((height,width, 3), np.uint8)
	canvas[:,:] = (255,255,255) # assign white background
	if debug:
		# draw points
		delaunay.draw_points(canvas)

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


	create_delaunay(img,30)
	#test()
	#draw_mesh(img, min_distance)
	"""cv2.imshow("image window", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()"""
