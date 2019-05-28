import math

class Vect2D(object):
	"""
	Two dimensional Vector object in cartesian coordinates
	"""
	__x = 0
	__y = 0

	@property
	def x(self):
		"""helloooo"""
		return self.__x

	@x.setter
	def x(self, new_value):
		if type(new_value) == int:
			self.__x = new_value
		else:
			raise TypeError
	
	@property
	def y(self):
		return self.__y
	
	@y.setter
	def y(self, new_value):
		if type(new_value) == int:
			self.__y = new_value
		else:
			raise TypeError

	def __init__(self, x, y):
		"""
		Initialize a 2D vector with x, y values
		"""
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
		Get the angle of the vector.
		TODO: TEST IT
		"""
		print("HEllo!")
		return math.atan(self.y / self.x)
#abc