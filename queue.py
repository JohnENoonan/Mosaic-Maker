"""
	Author: John Noonan
	Purpose: queue class used to store points ordered for sampling
"""
import sys
import random
# queue holds points that have been created that can still have more points added
# within its radius. Underlying structure is just alist with additional methods
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
	def rand_pop(self):
		if self.not_empty():
			i = random.randint(0, (self.size)-1)
			self.size -= 1
			return self.data.pop(i)
		else:
			sys.stderr.write("Error: Attempted pop on empty Queue")
			sys.exit(1)
