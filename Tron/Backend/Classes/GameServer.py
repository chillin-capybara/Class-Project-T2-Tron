from .Broadcaster import Broadcaster
from .Lobby import Lobby

from ..Core.leasable_collections import *
from ..Core.globals import *
from typing import List
import logging

class GameServer(object):
	"""
	Game server class of the Python game project
	"""	

	__broadcaster: Broadcaster = None
	__lobbies : List[Lobby] = None
	__available_ports : LeasableList = None # Collection for available ports

	def __init__(self, num_lobbies: int):
		"""
		Initialize a Game Server with a given amount of lobbies
		
		Args:
			num_lobbies (int): Number of lobbies

		Raises:
			TypeError: Invalid argument types
		"""

		# Initialize the collection of available ports
		self.__available_ports = LeasableList(list(LOBBY_PORT_RANGE))

		# Initialize the list of the lobbies
		self.__lobbies = []

		# Create the given amout of lobbies
		if type(num_lobbies) is not int:
			raise TypeError
		
		for i in range(0, num_lobbies):
			self.create_lobby()
		
		logging.info("%d lobbies created." % num_lobbies)
		
		# Initialize the Broadcaster
		self.__broadcaster = Broadcaster(self.get_lobbies)
	
	def create_lobby(self):
		"""
		Create a new lobby and add it to the collection of lobbies on the server
		"""	
		leased_port = self.__available_ports.lease()
		host : str = "" # On the server, lobbys have empty host
		port: int = leased_port.getObj()
		self.__lobbies.append(Lobby(host, port))
	
	def get_lobbies(self) -> List[Lobby]:
		"""
		Get the list of lobbies available on the server.
		
		Returns:
			List[Lobby]: List of active lobbies
		"""
		return self.__lobbies
	
	def Start(self):
		"""
		Start the game server with all the lobbies and discovery protocols
		"""
		logging.info("Starting game server...")

		# Start the discovery
		self.__broadcaster.Start()

		# Start the lobby threads
		for lobby in self.__lobbies:
			lobby.start_server()

		while True:
			pass


