from .Client import Client
from .Player import Player
from .Factory import Factory
from .TCPCLient import TCPCLient
from .Arena import Arena
from .TCPServer import TCPServer
from ..Core.Event import Event
import logging
import threading

class Game(object):
	"""
	Main class of the GAME backend part, handling all events and players
	"""

	__Players = None # List of players participating in the game

	__Arena = None # Arena object of the current game

	__client: Client = None

	__me: Player = None

	__me_id = 0 # Player ID of the current player

	__server_thread : threading.Thread = None

	__server: TCPServer = None

	# EVENTS TO USE BY UI
	ECountDown = None
	EUpdatePlayers = None

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

		# Initialize the players 
		self.__Players = []

		# Initialize Client
		self.__client = TCPCLient(self)

		# Initialize Events
		self.ECountDown = Event('seconds')
		self.EUpdatePlayers = Event()

		# Add player updater Event
		self.__client.EUpdatePlayers += self.UpdatePlayers
	
	def getPlayerName(self):
		"""
		Get the name of the current player.
		Returns:
			str
		"""
		return self.me.getName()
	
	def setPlayerName(self, playername: str) -> None:
		"""
		Set the name of the current player in the game
		Args:
			playername (str): Name of the current player
		Raises:
			TypeError: Invalid player name
		"""
		self.me.setName(playername)
		logging.debug("Player name set to %s" % playername)
	
	def setColor(self, color: int) -> None:
		"""
		Set the color of the current player
		Args:
			color (int): Color of the current player
		Raises:
			TypeError: Color is not int
			ValueError: Color is negative
		"""
		self.me.setColor(color)
		logging.debug("Player color set to %d" % color)
	
	def getColor(self):
		"""
		Get the color of the current player
		Returns:
			int
		"""
		return self.me.getColor()
	
	def ConnectToServer(self, server: str, port: int):
		"""
		Connect to a running game server
		Args:
			server (str): IP Adress of the server
			port   (int): Port of the server
		Raises:
			TODO: WHAT RAISES???
		"""
		self.__client.Connect(server, port)
		logging.debug("Connectiong to %s on port %d" % (server, port))
	
	def CreateServer(self, host: str = "", port: int = 9876, player_number:int = 10) ->  None:
		"""
		Create a new server for clients to connect to
		Args:
			host (str): IPv4 Adress to run the server on. default=""
			port (int): Port to listen to.
		"""
		# Create a new server object
		self.__server = TCPServer(host, port)

		# Set the number of maximal players
		self.__server.setPlayerNumber(player_number)

		# Create a new thread for the server
		self.__server_thread = threading.Thread(target=self.__server.Start)

		# Start the server
		self.__server_thread.start()
	
	def DestroyServer(self):
		"""
		Abort the thread of the running server.
		"""
		self.__server.Stop()

	def getPlayers(self) -> list:
		"""
		Get the list of players in the game

		Returns:
			list
		"""
		return self.Players

	def UpdatePlayers(self,sender, players):
		"""
		Update the players of the current game, based on the receved data from Client
		Interface

		Args:
			sender : Caller of the event
			players (iter): Objects of players
		
		Raises:
			TODO: some game error
		"""
		self.__Players = players
	def RequestPause(self):
		"""
		Request a pause from this client.
		"""
		
	
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