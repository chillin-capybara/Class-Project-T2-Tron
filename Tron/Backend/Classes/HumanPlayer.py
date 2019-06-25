from .Player import Player
from .Track import Track, LightTrack
from ..Core.Vect2D import Vect2D

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
	# __Track = #TODO
	__IsAlive = False
	__IpAdress = None
	__IsConnected = False
	__IsInPause = False

	__track = None

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
		self.__track = LightTrack()
		self.__Position = Vect2D(0,0)
		self.__Velocity = Vect2D(0,0)
		self.__IpAdress = "0.0.0.0"

	def getTrack(self):
		return self.__track

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


	def getTrack(self):
		"""
		Get the track made by the player cruising on the arena.

		Returns:
		LightTrack as Track object
		"""
		raise NotImplementedError


	def isAlive(self) -> bool:
		"""
		Get if the Player is alive

		Returns:
		True or False
		"""
		return self.__IsAlive


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
		self.__Velocity.x = x
		self.__Velocity.y = y


	def addTrack(self, start, end):
		"""
		Add a new track element to the pulled "light-track" of the player

		Args:
		track (track_segment): New track element to be added

		Raises:
		TrackError: The given track is invalid

		Note:
		TrackError is defined in Core.Exceptions
		"""
		self.__track.addElement(start, end)


	def enterPause(self):
		"""
		Starts a process to enter the user -> and the game in pause state

		Raises:
		CommError: Error while communicating the pause request
		"""
		self.__IsInPause = True
		#TODO: Error while communicating the pause request


	def move(self, time: int):
		"""
		Update the players position based on the velocity and the spent time

		Args:
		time: Spent time
		Raises:
		TypeError: time is not an integer
		"""
		if type(time) == int:
			self.__Position += self.__Velocity.x * time, self.__Velocity.y * time
		else:
			raise TypeError

# # test Player implementation
# testPlayer = HumanPlayer()
# testPlayer.__Name = "Max Mustermann"
# testPlayer.__Color = 2
