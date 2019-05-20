import math

class Vect2D(object):
	"""
	Two dimensional Vector object in cartesian coordinates
	"""
	x = 0
	y = 0

	def __init__(self, x:int, y:int):
		"""
		Initialize a 2D vector with x, y values
		"""
		if not (type(x) == int and type(y) == int):
			raise TypeError
		self.x = x
		self.y = y

	def length(self):
		"""
		Get the length of the vector

		Returns:
			float
		"""
		length = math.sqrt(self.x**2 + self.y**2)
		return length
	
	def angle(self):
		"""
		Get the angle of the vector
		"""
		raise NotImplementedError
