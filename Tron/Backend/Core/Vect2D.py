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
		return math.atan(self.y / self.x)
	
	def __add__(self, other):
		"""
		Add a Vect2D vector to yourself
  
		Args:
			Vect2D to add
  
		Returns: 
			Vect2D
  		"""
		if type(other) == Vect2D:
			self.x += other.x
			self.y += other.y
			return self
		else:
			raise TypeError
	
	def __str__(self):
		return "Vector: ({},{})".format(self.x, self.y)
	
	def __mul__(self, other):
		"""
		Multiply a Vect2D by yourself

		Args: 
  			other (Vect2D): to multiply
  
		Returns: 
  			int: For Vect2D * Vect2D
			Vect2D: For scalar * Vect2D
		NOTE:
			Multiplication with scalar value is not supported
  		"""
		if type(other) == Vect2D:
			result = (self.x * other.x) + (self.y * other.y)
			return result
		## integer multiplication implementation 
		elif type(other) == int:
			result = Vect2D(self.x * other, self.y * other)
			return result
		else:
			raise TypeError
	
	def __eq__(self, other):
		"""
		Check if 2 Vect2D objects are identical
		"""
		
		# Check the equality
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False

	def clone(self):
		"""
		needed to implement clone fucntion to create reference to new RAM space
		"""
		return Vect2D(x = self.x, y = self.y)
	






#abc
# OPERATOR OVERLOADING:
# v, u Vect2D
# w = v + u
# w = v * c
# w = Vect2D(2,2) - 2 * v
# v.add(u)
# v = v + u
# v += u
# v -= u 

# v = Vect2D(1,2)
# u = Vect2D(2,3)
# w = v + u
# print(w)
