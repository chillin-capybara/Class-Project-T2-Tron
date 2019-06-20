from .HumanPlayer import HumanPlayer
from .Player import Player

class Factory:
	"""
	Static class for factoring Instances for the interfaces dynamically
	"""

	@staticmethod
	def Player(playername: str, color: int) -> Player:
		"""
		Factor a new player instance of HumanPlayer or RandomPlayer
		Args:
			playername (str): Name of the player
			color (int): Color of the player
		Returns:
			Player: Factored Player
		"""
		new = HumanPlayer()
		new.setName(playername)
		new.setColor(color)

		return new

	@staticmethod
	def isPlayer(obj) -> bool:
		"""
		Returns whether an object is any of player type
		"""
		if type(obj) == Player:
			return True
		if type(obj) == HumanPlayer:
			return True
		
		if isinstance(obj, (Player, HumanPlayer)):
			return True
		return False