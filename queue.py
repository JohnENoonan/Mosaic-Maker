"""
	Author: John Noonan
	Purpose: queue class used for image simplification
"""
import sys
import random
# queue holds points that have been created that can still have more points added
# in its radius
class Queue:
	def __init__(self):
		self.data = [] # list of Points
		self.size = 0
	# add a Point to data
	def push(self, p):
		self.data.append(p)
		self.size += 1
	# returns true if not empty, false if it is
	def not_empty(self):
		return self.size > 0
	# removes random element and returns it
	def pop_(self):
		if self.not_empty():
			i = random.randint(0, (self.size)-1)
			self.size -= 1
			return self.data.pop(i)
		else:
			sys.stderr.write("Error: Attempted pop on empty Queue")
