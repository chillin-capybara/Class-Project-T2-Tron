from .HumanPlayer import HumanPlayer
from .Player import Player as IPlayer


class Factory:
	"""
	Static class for factoring Instances for the interfaces dynamically
	"""

	@staticmethod
	def Player(playername: str, color: tuple) -> IPlayer:
		"""
		Factor a new player instance of HumanPlayer or RandomPlayer
		Args:
			playername (str): Name of the player
			color (int): Color of the player
		Returns:
			Player: Factored Player
		"""
		new = None
		new = HumanPlayer()
		new.setName(playername)
		new.setColor(color)

		return new

	@staticmethod
	def isPlayer(obj) -> bool:
		"""
		Returns whether an object is any of player type
		"""
		try:
			return obj.isPlayer() == True
		except:
			return False

	#@staticmethod
	#def Client():
	#	return TCPCLient()