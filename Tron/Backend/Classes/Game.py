from .Client import Client
from .Player import Player
from .Factory import Factory
from .Arena import Arena

class Game(object):
	"""
	Main class of the GAME backend part, handling all events and players
	"""

	Players = [] # List of players participating in the game

	__Arena = None # Arena object of the current game

	__client = None

	__me: Player = None

	__me_id = 0 # Player ID of the current player 

	@property
	def me(self) -> Player:
		"""
		Object of the current player on the computer.
		Returns:
			Player: object of the current player
		"""
		return self.__me
	
	@property
	def Arena(self) -> Arena:
		"""
		Return the current arena of the game
		Returns:
			Arena: object of the current arena
		"""
		return self.__Arena

	def __init__(self):
		# Create a local player for the current game
		self.__me = Factory.Player("", 0)

		# Attach the Player update event to the tcp receive event
		self.__client.attachPlayersUpdated(self.UpdatePlayers)

	def getPlayers(self) -> list:
		"""
		Get the list of players in the game

		Returns:
			list
		"""
		return self.Players

	def UpdatePlayers(self, players):
		"""
		Update the players of the current game, based on the receved data from Client
		Interface

		Args:
			players (iter): Objects of players
		
		Raises:
			TODO: some game error
		"""
		pass
	
	def PauseEntered(self):
		"""
		Event handler for entering pause, requested by the server

		Raises:
			TODO: some game error
		"""
		pass
	
	def Countdown(self):
		"""
		Event handler for starting the game countdown, requested by the server

		Raises:
			TODO: some game error
		"""
		pass