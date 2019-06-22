from Arena import Arena


class RectangleArena(Arena):
	"""
	Realisation of Arena Interface for Arena
	"""

	def __init__(self, name: str, size, skin: int, mode: int):
		"""
		Initialize Object from Arena Class
			Args: 
				name(str): Name of the Arena
				size((x,y) Tuple): Size of the Arena
				skin(int): Skin of the Arena 
				mode(int): Mode of the Arena
		"""
		if type (name) != str:
			raise TypeError
		else:
			self.name = name

		if (type (size[0]) != int) | ((type (size[1]) != int) ):
			raise TypeError
		else:
			self.size = size

		if type (skin) != int:
			raise TypeError
		else:
			self.skin = skin

		if type (mode) != int:
			raise TypeError
		else:
			self.mode = mode

	def getName(self) -> str:
		"""
		Get the name of the arena object
		Returns:
			str: Arena name
		"""
		return self.name #TODO: were is the difference between __str__?
	
	def __str__(self):
		"""
		Convert arena to string = Get the name of the arena
		Returns:
			str: Arena name
		"""
		return self.name

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