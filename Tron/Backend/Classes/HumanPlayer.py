from .Player import Player
from .Track import Track, LightTrack
from ..Core.Vect2D import Vect2D
from typing import List
from ..Core.matrix import *

# todo: Implement the Human player according to the UML
#TODO: Makros definition
MAX_X_GAME_FIELD = 240
MAX_Y_GAME_FIELD = 240
MAX_X_VELOCITY = 10**4
MAX_Y_VELOCITY = 10**4
MAX_COLOR_NUMBER = 100

class HumanPlayer(Player):
	"""
	implementation of Human Player Class
	"""

	__Name = ""  # Name of the player
	__Color = None  # Color of the player
	__Position = None
	__Velocity = None
	__Lifes = 0 # Number of lifes, the player has
	# __Track = #TODO

	__IpAdress = None
	__IsConnected = False
	__IsInPause = False

	__track : List[Vect2D] = None
	__last_velocity : Vect2D = None

# input check Velocity.x
	@property
	def velocityX(self):
		"""
		property for Velocity type check
		"""
		return self.__Velocity.x

	@velocityX.setter
	def velocityX(self, new_value):
		if type(new_value) != int:
			raise TypeError
		else:
			if abs (new_value) > MAX_X_VELOCITY:
				raise ValueError
			else:
				self.__Velocity.x = new_value

# input check Velocity.y
	@property
	def velocityY(self):
		"""
		property for Velocity type check
		"""
		return self.__Velocity.y

	@velocityX.setter
	def velocityY(self, new_value):
		if type(new_value) != int:
			raise TypeError
		else:
			if abs (new_value) > MAX_Y_VELOCITY:
				raise ValueError
			else:
				self.__Velocity.y = new_value


	def __init__(self):
		self.__track = []
		self.__Position = Vect2D(0,0)
		self.__Velocity = Vect2D(0,0)
		self.__last_velocity = Vect2D(0,0)
		self.__IpAdress = "0.0.0.0"

		# Set the color to black as default
		self.__Color = (0,0,0)


	def getTrack(self) -> List[Vect2D]:
		"""
		Get the track points of the current player via a list of Vect2D
		
		Returns:
			List[Vect2D]: Track of the current player
		"""
		return self.__track
	
	@property
	def track(self) -> List[Vect2D]:
		"""
		Track points of the current player via a list of Vect2D
		"""
		return self.__track
	
	@property
	def lifes(self) -> int:
		"""
		Lifes of the player has
		"""
		return self.__Lifes
	
	@lifes.setter
	def lifes(self, value:int):
		"""
		Setter for player's life
		"""
		self.set_lifes(value)
	
	def set_lifes(self, value:int):
		"""
		Set the lifes of the current player based on the match properties
		
		Args:
			value (int): Life of the player
		Raises:
			TypeError: Invalid value type
			ValueError: Negative life
		"""
		if type(value) is int:
			if value >= 0:
				self.__Lifes = value
			else:
				raise ValueError
		else:
			raise TypeError
	
	def die(self):
		"""
		Negate 1 from the lifes of the player, until it's zero
		"""
		if self.is_alive:
			# Only negate when the player is still alive
			self.__Lifes -= 1
	
	def is_alive(self):
		"""
		Check if the player is alive or not
		
		Returns:
			int: True = Alive, False = Dead
		"""
		return (self.__Lifes > 0)

	def getLine(self):
		return self.__track.getLine()

	def getName(self) -> str:
		"""
		get the Name from the Sever

		Returns:
		str: Name of the player
		"""

		return self.__Name


	def getColor(self) -> int:
		"""
		get the player's Color

		Returns:
			(r,g,b): player's color

		"""
		return self.__Color


	def getPosition(self) -> Vect2D:
		"""
		Get the current position of the Player

		Returns:
		Player coordinates as Vect2D
		"""
		return self.__Position
	def getVelocity(self) -> Vect2D:
		"""
		TODO: Artem -> DOKU
		"""
		return self.__Velocity

	def isInPause(self) -> bool:
		"""
		Get if the Player is alive

		Returns:
		True or False
		"""
		return self.__IsInPause


	def getIPAdress(self) -> str:
		"""
		Get the IP address of the player

		Returns:
		IP Adress as a string #TODO: IP Adress format
		"""
		return self.__IpAdress


	def isConnected(self) -> bool:
		"""
		Check if the Player is connected to the game

		Returns:
		True or False
		"""
		return self.__IsConnected


	def setName(self, name: str):
		"""
		Set the name of the player

		Args:
		name (str): Name of the Player

		Raises:
		TypeError: The entered value is not a string
		ValueError: The name is either empty or too long
		"""

		if type(name) == str:
			self.__Name = name
		else:
			raise TypeError


	def setColor(self, color: tuple):
		"""
		Set the color of the player

		Args:
			color (r,g,b): New color code based on the game specification

		Raises:
		TypeError: The entered value is not an int
		ValueError: The entered color doesn't exists
		"""
		if type(color) is not tuple:
			raise TypeError
		self.__Color = color


	def setPosition(self, x: int, y: int):
		"""
		Set the position of the player to the given x,y coordinates

		Args:
		x (int): X-coordinate on the gamefield
		y (int): Y-coordinate on the gamefield

		Raises:
		TypeError: x or y is not an integer
		ValueError: x or y is not a valid value on the gamefield
		"""
		if type(x) == int:
			if x <= MAX_X_GAME_FIELD:
				self.__Position.x = x
			else:
				raise ValueError
		else:
			raise TypeError

		if type(y) == int:
			if y <= MAX_Y_GAME_FIELD:
				self.__Position.y = y
			else:
				raise ValueError
		else:
			raise TypeError


	def setVelocity(self, x, y):
		"""
		set the player's velocity

		Args: 
		velocity: velocity as Vect2D
		"""
		# Store the old velocity
		self.__last_velocity.x = self.__Velocity.x
		self.__last_velocity.y = self.__Velocity.y

		# Set the new velocity
		self.__Velocity.x = x
		self.__Velocity.y = y


	def enterPause(self):
		"""
		Starts a process to enter the user -> and the game in pause state

		Raises:
		CommError: Error while communicating the pause request
		"""
		self.__IsInPause = True
		#TODO Error while communicating the pause request

	def move(self, time):
		"""
		Update the players position based on the velocity and the spent time

		Args:
		time: Spent time
		Raises:
			TODO TYPE CHECKING
		"""
		self.__Position.x += self.__Velocity.x * time
		self.__Position.y += self.__Velocity.y * time
	
	def step(self):
		"""
		Step the player forward in the direction of it's velocity
		"""
		self.__Position.x += self.__Velocity.x
		self.__Position.y += self.__Velocity.y
	
	def update_player_track(self, matrix: list, player_id: int):
		"""
		Update the track of the current player
		
		Args:
			matrix (list): Matrix of the game field
			player_id (int): ID of the current player on the server
		"""
		self.__track = get_player_track(matrix, player_id)
