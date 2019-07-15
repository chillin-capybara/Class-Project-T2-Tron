from .Broadcaster import Broadcaster
from .Lobby import Lobby
from ..Core.Router import *

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

	ROOT_DIRECTORIES = ['config', 'lobbies', 'firewall']
	ROOT_ROUTER = Router()

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

		# Add the server command routes
		self.ROOT_ROUTER.add_default(self.root_default)
		self.ROOT_ROUTER.add_route('ls', self.root_ls)
		self.ROOT_ROUTER.add_route('cd (\d+)', self.root_cd)
		self.ROOT_ROUTER.add_route('log on', self.root_log_on)
		self.ROOT_ROUTER.add_route('log off', self.root_log_off)
		self.ROOT_ROUTER.add_route('shutdown', self.root_shutdown)
	
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
				ins = input('>>>')
				self.ROOT_ROUTER.run(ins)
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

	def root_ls(self):
		"""
		List all the directories in the server root
		"""
		lid = 0
		for lobby in self.__lobbies:
			print("{:<3d} Lobby {:<3d}    :{:<10d}".format(lid, lid, lobby.port), flush=True)
			lid += 1

	def root_cd(self, path: str):
		"""
		CD command on the server
		
		Args:
			path (str): Directory to switch to
		"""
		lobby_nr = int(path)
		try:
			# Call the base command of the lobby
			self.__lobbies[lobby_nr].base("/lobbies/lobby%d"%lobby_nr)
		except:
			logging.error("The lobby %d is not found on the server." % lobby_nr)
	
	def root_default(self):
		"""
		Default command route to call when a command is not recognized
		"""
		print("Command not recognizeable")
	
	def root_log_off(self):
		"""
		Turns off the logging
		"""
		logger = logging.getLogger()
		logger.propagate = False
		print("Logging turned OFF.", flush=True)
	
	def root_log_on(self):
		"""
		Turns the logging on again
		"""
		logger = logging.getLogger()
		logger.propagate = False
		print("Logging turned ON.", flush=True)

	def root_shutdown(self):
		"""
		Shuts the server down
		"""
		# This will effect the main loop and shut the server down
		raise KeyboardInterrupt

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


