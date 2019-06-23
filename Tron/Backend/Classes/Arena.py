
class Arena(object):
	"""
	Arena Interface for defining the mandatory functionalities of an Arena object
	"""

	def getName(self):
		"""
		Get the name of the arena object
		Returns:
			str: Arena name
		"""
		raise NotImplementedError
	
	def __str__(self):
		"""
		Convert arena to string = Get the name of the arena
		Returns:
			str: Arena name
		"""
		raise NotImplementedError

	def getSize(self):
		"""
		Get the size of the Arena

		Returns
			Size as (x,y) Tuple
		"""
		raise NotImplementedError
	
	def getSkin(self):
		"""
		Get the selected Skin of the Arena

		Returns:
			Skin number as int
		"""
		raise NotImplementedError
	
	def getMode(self):
		"""
		Get the selected mode of the Arena

		Returns:
			Mode as int
		"""
		raise NotImplementedError
	
	def getObjects(self):
		"""
		Get the containing special objects of the Arena

		Returns:
			Array of ArenaObj
		"""
		raise NotImplementedError