from ..Core.globals import *
from ..Core.Hook import Hook
from .BasicComm import BasicComm
from .HumanPlayer import HumanPlayer
from .LobbyThread import LobbyThread
import socket
import logging
import threading
from typing import List

class Lobby(object):
	"""
	Game lobby object for the Tron Game
	NOTE:
		Extendable for Pong, too
	"""
	__host = "" # IP address of the server
	__port = 0 # Change is not allowed after initialization

	__games : list   = None # List of games Here only Tron
	__matches : list = None # List of matches in the Lobby 

	__sock : socket.socket = None # Socket connection to the lobby
	__comm : BasicComm = None

	__hook_me : Hook = None

	__server_thread : threading.Thread = None
	__server_sock : socket.socket = None
	__server_threads : List[threading.Thread] = None

	def __init__(self, host: str, port: int, hook_me = None):
		"""
		Initialize a lobby on the server, to create games in
		
		Args:
			host(str) : IP adress of the lobby's server
			port (int): Port of the Lobby on the server.
			hook_me (callable): Hook to get the clients player. (CLIENT ONLY)
		
		Raises:
			TypeError: Invalid argument types
			ValueError: Invalid port range
		"""
		if type(host) is not str:
			raise TypeError
		
		if type(port) is not int:
			raise TypeError
		
		if port not in LOBBY_PORT_RANGE:
			raise ValueError("The given port is not in the specified range.")

		self.__host = host
		self.__port = port

		# Intialize communication protocol
		self.__comm = BasicComm()
		self.__comm.EWelcome += self.handle_welcome
		
		# Initialize hook : Only for clients
		if hook_me != None:
			self.__hook_me = Hook()
			self.__hook_me.delegate(hook_me)
	
	@property
	def port(self) -> int:
		"""
		Port number of the lobby on the server
		"""
		return self.__port
	
	@property
	def host(self):
		"""
		Host address of the Lobby's server
		"""
		return self.__host
	
	def hook_get_games(self):
		"""
		Get the list of games in the lobby
		
		Returns:
			list: List of games
			// TODO return the real list...
		"""
		return []
	
	def hook_get_matches(self):
		"""
		Return the matches running in the lobby
		// TODO Return a real list...
		"""
		return []
	
	def start_server(self):
		"""
		Start serving the lobby on the server
		"""
		# Initialize the list of threads
		self.__server_threads = []
		# Create a thread fot the server
		self.__server_thread = threading.Thread(target=self.__server)
		self.__server_thread.start()
	
	def __server(self):
		"""
		Server thread of the lobby on the server
		"""
		try:
			logging.info("Lobby server started %s:%d" % (self.host, self.port))
			# Create server socket
			self.__server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.__server_sock.bind((self.host, self.port))
			self.__server_sock.listen()

			while True:
				# Wait for incoming connections
				thread_sock, addr = self.__server_sock.accept()
				self.__create_thread(thread_sock)
		except Exception as e:
			logging.error(str(e))
	
	def __create_thread(self, sock: socket.socket):
		"""
		Create a thread on the server to handle client requests and responses simultaniously
		Args:
			sock (socket): Socket of the connection to handle
		"""
		# Initialzie all the thread hooks
		thread = LobbyThread(
							sock,
							hook_get_games=self.hook_get_games,
							hook_get_matches=self.hook_get_matches
							)
		# Add the thread to the collections
		self.__server_threads.append(thread)
		# Start the thread
		thread.start()


	def say_hello(self):
		"""
		Connect to a lobby on the server

		NOTE:
			Only supported for client
		"""
		try:
			logging.info("Entering the Lobby %s:%d" % (self.host, self.port))
			
			# create socket and connect
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.__sock.connect((self.host, self.port))

			# Send Hello message
			packet = self.__comm.hello(self.__hook_me(), CLIENT_FEATURES)
			self.__sock.send(packet)

			# Receive the answer
			resp = self.__sock.recv(CONTROL_PROTOCOL_RECV_SIZE)
			self.__comm.process_response(resp)
			logging.info(resp)
		except Exception as e:
			logging.error("Error occured while saying hello: %s" % str(e))
	
	def handle_welcome(self, sender, features: list):
		"""
		Event handler for receiving a welcome message form the server
		
		Args:
			sender   (CommProt): Caller of the event
			featrues (list): List of server features
		"""
		logging.info("The server welcomes you. Supported server features %s" % str(features))


