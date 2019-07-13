from .Broadcaster import Broadcaster
from .Lobby import Lobby

from ..Core.leasable_collections import *
from ..Core.globals import *
from ..Core.Event import Event
from typing import List
import logging
import time
import threading

class GameServer(object):
	"""
	Game server class of the Python game project
	"""	

	__broadcaster: Broadcaster = None
	__lobbies : List[Lobby] = None
	__available_ports : LeasableList = None # Collection for available ports

	__isRunning = False

	EStop : Event = None # Stop Event for the server

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

		self.EStop = Event()
	
	@property
	def available_ports(self) -> LeasableList:
		return self.__available_ports

	def hook_lease_port(self) -> LeasableObject:
		"""
		Lease a port from the collections of ports on the server.

		Returns:
			LeasableObject: New port
		"""
		return self.__available_ports.lease()

	def create_lobby(self):
		"""
		Create a new lobby and add it to the collection of lobbies on the server
		"""	
		leased_port = self.__available_ports.lease()
		host : str = "" # On the server, lobbys have empty host
		port: int = leased_port.getObj()
		self.__lobbies.append(Lobby(host, port, hook_lease_port=self.hook_lease_port, parent=self))
	
	def get_lobbies(self) -> List[Lobby]:
		"""
		Get the list of lobbies available on the server.
		
		Returns:
			List[Lobby]: List of active lobbies
		"""
		return self.__lobbies
	
	def Start(self, loop = False):
		"""
		Start the game server with all the lobbies and discovery protocols
		"""
		logging.info("Starting game server...")

		# Start the discovery
		self.__broadcaster.Start()

		# Add the stop event to close all the threads
		self.EStop += self.__broadcaster.handle_server_stop

		# Start the lobby threads
		for lobby in self.__lobbies:
			# Add the stop event to close all the threads
			self.EStop += lobby.handle_server_stop
			lobby.start_server()

		self.__isRunning = True

		thread = threading.Thread(target=self.__keepalive)
		thread.start()

		try:
			while loop:
				time.sleep(1)
		except KeyboardInterrupt:
			self.Stop() # Close up all the stuff
	
	def __keepalive(self):
		"""
		Keep-alive thread for the server to check status
		"""
		try:
			while True:
				if self.EStop.was_called():
					break
				time.sleep(1)
		except:
			self.EStop(self)
		
		self.__isRunning = False
		self.EStop.reset_called()
		logging.info("The game server was stopped!")


	def Stop(self):
		"""
		Stop the server with all the threads
		"""
		# Only call the stop Event
		self.EStop(self)
	
	def isRunning(self) -> bool:
		"""
		Get if the server is still running
		
		Returns:
			bool: True = RUNNING, False = NOT RUNNING
		"""
		return self.__isRunning


