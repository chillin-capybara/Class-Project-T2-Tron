
class Game(object):
	"""
	Main class of the GAME backend part, handling all events and players
	"""

	me = None    # Current player from the gamer's perspective

	Players = [] # List of players participating in the game

	Arena = None # Arena object of the current game

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