
class Player(object):
	"""
	Interface for Player object
	"""

	def getName(self):
		"""
		Get the Name of the Player.

		Returns:
			Name of the player
		"""
		raise NotImplementedError
	
	def getColor(self):
		"""
		Get the Color of the Player.

		Returns:
			int: Color of the Player
		"""
		raise NotImplementedError

	def getPosition(self):
		"""
		Get the current position of the Player

		Returns:
			Player coordinates as Vect2D
		"""
		raise NotImplementedError

	def getVelocity(self):
		"""
		Get the current velocity of the Player

		Returns:
			Velocity as Vect2D
		"""
	
	def getTrack(self):
		"""
		Get the track made by the player cruising on the arena.

		Returns:
			LightTrack as Track object
		"""
		raise NotImplementedError
	
	def isAlive(self):
		"""
		Get if the Player is alive

		Returns:
			True or False
		"""
		raise NotImplementedError
	
	def isConnected(self):
		"""
		Check if the Player is connected to the game

		Returns:
			True or False
		"""
		raise NotImplementedError
	
	def isInPause(self):
		"""
		Check if the player is in pause

		Returns:
			True or False
		"""
		raise NotImplementedError
	
	def getIPAddress(self):
		"""
		Get the IP address of the player

		Returns:
			True or False
		"""
		raise NotImplementedError
	
	def setName(self, name):
		"""
		Set the name of the player

		Args:
			name (str): Name of the Player

		Raises:
			TypeError: The entered value is not a string
			ValueError: The name is either empty or too long
		"""
		raise NotImplementedError
	
	def setColor(self, color):
		"""
		Set the color of the player

		Args:
			color (int): New color code based on the game specification
		
		Raises:
			TypeError: The entered value is not an int
			ValueError: The entered color doesn't exists
		"""
		raise NotImplementedError
	
	def setPosition(self, x, y):
		"""
		Set the position of the player to the given x,y coordinates

		Args:
			x (int): X-coordinate on the gamefield
			y (int): Y-coordinate on the gamefield
		
		Raises:
			TypeError: x or y is not an integer
			ValueError: x or y is not a valid value on the gamefield
		"""
		raise NotImplementedError
	
	def addTrack(self, track):
		"""
		Add a new track element to the pulled "light-track" of the player

		Args:
			track (Track): New track element to be added
		
		Raises:
			TrackError: The given track is invalid

		Note:
			TrackError is defined in Core.Exceptions
		"""
		raise NotImplementedError
	
	def enterPause(self):
		"""
		Starts a process to enter the user -> and the game in pause state

		Raises:
			CommError: Error while communicating the pause request
		"""
		raise NotImplementedError
