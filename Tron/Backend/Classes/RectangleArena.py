from Arena import Arena
from ..Core.Vect2D import Vect2D
import logging
#from dill.source import getname

MAX_ARENA_SIZE = 1000
MIN_ARENA_SIZE = 4
MAX_ARENA_NAME_LENGTH = 20
MIN_ARENA_NAME_LENGTH = 2

class DieError(Exception):
	"""
	Exception for signaling when a player dies
	"""
	pass

class RectangleArena(Arena):
	"""
	Realisation of Arena Interface for Arena
	"""
	__name = ""
	__sizeX = MIN_ARENA_SIZE
	__sizeY = MAX_ARENA_SIZE
	__skin = 0
	__mode = 0 

	__matrix : List = None # Matrix representation of the arena

	
	#Size setter implementation
	@property
	def sizeX(self):
		"""
		property for sizeX input check
		"""
		return self.__sizeX

	@sizeX.setter
	def sizeX(self, new_value):
		if type(new_value) == int:
			if (new_value < MIN_ARENA_SIZE) | (new_value > MAX_ARENA_SIZE) : # check, if the value is ok
				raise ValueError	
			else:
				self.__sizeX = new_value
		else:
			raise TypeError
	
	@property
	def sizeY(self):
		"""
		property for sizeY input check
		"""
		return self.__sizeY

	@sizeY.setter
	def sizeY(self, new_value):
		if type(new_value) == int:
			if (new_value < MIN_ARENA_SIZE) | (new_value > MAX_ARENA_SIZE) : # check, if the value is ok
				raise ValueError	
			else:
				self.__sizeY = new_value
		else:
			raise TypeError
	#Name setter implementation
	@property
	def name(self):
		"""
		property for name input check
		"""
		return self.__name 

	# @sizeX.setter
	# def name(self, new_value):
	# 	if type(new_value) == str:
	# 		if (len(new_value) < MIN_ARENA_NAME_LENGTH) | (len(new_value) > MAX_ARENA_NAME_LENGTH) : # check, if the word's length is ok
	# 			raise ValueError
	# 		else:
	# 			self.__name = new_value
	# 	else:
	# 		raise TypeError

	@property
	def matrix(self) -> list:
		"""
		Matrix representation of the arena
		"""
		return self.__matrix
	

	def __init__(self, name: str, size, skin: int, mode: int):
		"""
		Initialize Object from Arena Class
			Args: 
				name(str): Name of the Arena
				size((x,y) Tuple): Size of the Arena
				skin(int): Skin of the Arena 
				mode(int): Mode of the Arena
		"""

		self.__name = name

		# size
		self.sizeX = size[0]
		self.sizeY = size[1]

		if type (skin) != int:
			raise TypeError
		else:
			self.skin = skin

		if type (mode) != int:
			raise TypeError
		else:
			self.mode = mode

		
		# Create an arena matrix filled with zeros
		zrow = []
		for i in range(0, self.sizeY):
			zrow.append(0)

		self.__matrix = []
		for j in range(0, self.sizeX):
			self.__matrix.append(zrow.copy()) # Make a x * y zero matrix for the game
	
	def player_stepped(self, player_id:int, pos: Vect2D):
		"""
		Step a player onto a field. If it was not successfull, the raise an error
		
		Args:
			player_id (int): ID Of the player
			pos (Vect2D): Position on the field
		"""
		# If anything bad happens, you die
		if pos.x < 0 or pos.y < 0:
			raise DieError
		
		if pos.x > self.sizeX or pos.y > self.sizeY:
			raise DieError
		
		if self.__matrix[pos.x][pos.y] == 0:
			# Field is still free, you can step on it
			self.__matrix[pos.x][pos.y] = player_id
		else:
			raise DieError


	def getName(self) -> str:
		"""
		Get the name of the arena object
		Returns:
			str: Arena name
		"""
		
		return self.__name 
	
	def __str__(self) -> str:
		"""
		Convert arena to string = Get the name of the arena
		Returns:
			str: Arena name
		"""
		return self.getName()

	def getSize(self):
		"""
		Get the size of the Arena

		Returns
			Size as (x,y) Tuple
		"""
		return self.size

	
	def getSkin(self):
		"""
		Get the selected Skin of the Arena

		Returns:
			Skin number as int
		"""
		return self.skin
	
	def getMode(self):
		"""
		Get the selected mode of the Arena

		Returns:
			Mode as int
		"""
		return self.mode
	
	def getObjects(self):
		"""
		Get the containing special objects of the Arena

		Returns:
			Array of ArenaObj
		"""
		raise NotImplementedError