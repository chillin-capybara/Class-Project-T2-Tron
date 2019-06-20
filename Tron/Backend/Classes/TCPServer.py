from .Server import Server                # Server interface
from .TCPThreads import SenderThread, ReceiverThread
from .CommProt import CommProt
from ..Core.Exceptions import ServerError  #ServerError Exception
from ..Core.core_functions import get_timestamp
from .JSONComm import JSONComm
from .Player import Player
from .Arena import Arena
from .Factory import Factory
import logging
import socket

def print_error(sender: CommProt, msg: str):
	logging.warning(msg)

class TCPServer(Server):
	"""
	Realization of Server Interface for TCP Server
	"""

	__host = ""                 # Server Host IP
	__port = 0                  # Server Port
	__status = 0                # Server status
	__Arena = None              # Hosted Arena
	__playernumber = 0          # Number of players
	__comm_proto = None         # Communication protocol
	__players = None              # Array of players
	__playerThreads = None        # Array of TCP Threads for the players in async communication
	__player_index = 0          # Player index currently to be added
	__sock = None # Serversocket
	__settings_locked = False   # Check if server settings are locked

	def __init__(self, host="", port=23456):
		"""
		Initialize TCP Server on the given host IP and port
		Args:
			host (str): IPv4 address of host (any="")
			port (int): Port number of the server
		Raises:
			TypeError: Not valid types
			ValueError: Port Number is invalid
		"""
		if not type(host) == str:
			raise TypeError
		
		if not type(port) == int:
			raise TypeError
		
		if port not in range(0,2**16-1):
			raise ValueError
		try:
			# Setup the communication protocoll
			self.__comm_proto = JSONComm()

			# Create IPv4 TCP Socket
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.__sock.bind((host, port))

			self.__players = []
			self.__playerThreads = []
		except Exception as e:
			# Raise a ServerError
			raise ServerError(str(e))
	
	def setArena(self, arena):
		"""
		Set the arena of the game server

		Args:
			arena (Arena): Arena object created for the game
		
		Raises:
			TypeError: The object is not an arena.
			ServerError: The arena type doesn't exist on the server, or ...
				the server is still running.
		"""

		if not type(arena) == Arena:
			raise TypeError
		
		if self.__settings_locked:
			raise ServerError("Cannot change the arena, while the server is running")
		
		self.__Arena = arena

		logging.debug("Arena set to " + str(arena))
	
	def getArena(self):
		"""
		Get the arena the game server hosts.

		Returns:
			Arena: Currently active arena object
		"""
		return self.__Arena

	
	def setPlayerNumber(self, players):
		"""
		Set the number of the players who will play the game
		
		Args:
			players (int): Number of the players the server starts the game with.
		
		Raises:
			TypeError: players is not an integer
			ValueError: Players is not a valid number
			ServerError: The server is still running.
		"""
		if not type(players) == int:
			raise TypeError
		
		if not players in range(0,100):
			raise ValueError
		
		if(self.__settings_locked):
			raise ServerError("Cannot update player number, the server is running")
		
		# Set the player number
		self.__playernumber = players

		logging.debug("Number of players set to %d" % players)

		# Reserve the objects for the players
		for i in range(0, players):
			self.__players.append(Factory.Player("", 0))

	
	def getPlayerNumber(self):
		"""
		Get the number of players currently on the server.

		Returns:
			int: Number of players
		"""

		return self.__playernumber
	
	def getPlayers(self):
		"""
		Get the collection of players connected to the server

		Returns:
			iter: List of the players connected to the server
		
		Raises:
			ServerError: Server is not running
		"""
		# TODO: Add ServerError when the server is not running
		return self.__players

	def __create_threads(self, sock: socket.socket, player_id: int):
		"""
		Create send and receive threads for every client connecting to the server

		Args:
			sock (socket): Accepted connection socket
			player_id (int): Index of the player on the server
		Raises:
			TypeError: sock is not a socket
			ServerError: ???
		"""
		# Create a protocoll instance for every thread pair!
		thr_proto = JSONComm()
		senderThread = SenderThread(self, sock, thr_proto, player_id)
		receiverThread = ReceiverThread(self, sock, thr_proto, player_id)

		# Start the Threads
		senderThread.start()
		receiverThread.start()

		# Append the threads for the players
		self.__playerThreads.append((senderThread, receiverThread))

		logging.debug("Networking threads created for client")


	def Start(self):
		
		try:
			# Start listening on socket
			self.__sock.listen()
			logging.info("Server started on port %d, maximal %d players" % (self.__port, self.__playernumber))
			
			while(True):

				conn, address = self.__sock.accept()

				logging.info("New TCP Connection accepted: " + str(address))

				# TODO: Start new thread for client_socket
				self.__create_threads(conn, self.__player_index)
				
				# Create a new empty player into the array
				#self.__players.append(Factory.Player("",0))

				self.__player_index += 1

		except Exception as e:
			raise e

	def hook_player_ready(self, player_id: int, player: Player):
		"""
		Uptade the player object, which belongs to the thread
		"""
		# PRINT ALL THE PLAYER IN THE LIST
		self.__players[player_id] = player
		logging.info("%s joined with ID=%d" % (player.getName(), player_id))
		
	
	def hook_client_ingame(self, player_id, player: Player):
		"""
		Update a specific player object ingame
		"""
		self.__players[player_id] = player
		logging.debug("Client updated with name=%s ID=%d" % (player.getName(), player_id))
		logging.debug("New position: " + str(player.getPosition()))
	
	def hook_player_leave(self, player_id: int):
		"""
		Log and communicates with the clients if somebody leaves
		"""
		logging.info("%s has left the match!", (self.__players[player_id].getName()))
