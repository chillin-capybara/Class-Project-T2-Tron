
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
			Color of the Player as int
		"""
		raise NotImplementedError

	def getPosition(self):
		"""
		Get the current position of the Player

		Returns:
			Player coordinates as (x,y) Vector
		"""
		raise NotImplementedError

	def getVelocity(self):
		"""
		Get the current velocity of the Player

		Returns:
			Velocity as (x,y) Vector
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