from .TCPClientThreads import SenderClientThread, ReceiverClientThread, makros
from ..Core.Exceptions import ClientError
from .Factory import Factory
from .Client import Client
import socket
import logging

"""
Realisation of TCP Client Interface for TCP Client
"""
class TCPCLient(Client):

	__host         = ""                 # Server Host IP
	__port         = 0                  # Server Port
	__sock         = None 				# Cleintsocket
	__bufferSize   = 4096
	__Comm         = None
	__Player       = None
	__players      = None


	__RecieverThread = None

	def __init__(self):
		"""
		Initialize a new TCP Client
		Details:
			Initialize collections and Event handlers
		"""
		self.__Player = []

		self.__Comm: CommProt = Factory.CommProt()
		#self.__RecieverThread = ReceiverClientThread()

		# Attach client_ready ack handler to event
		self.__Comm.EClientReadyAck += self.handle_ready_ack
		self.__Comm.EIngame += self.handle_ingame #+ self.handle_ingame_update
		self.__Comm.EServerError += self.handle_server_error


		#self.__RecieverThread.EIngameUpdate += handle_ingame_update
		# self.__RecieverThread.EServerNotification += handle_serever_notification
		self.__Comm.EServerNotification += self.handle_serever_notification



	def attachPlayersUpdated(self, callback):
		"""
		TODO: DOC
		"""
		raise NotImplementedError

	def Connect(self, server, port):
		"""
		Connect to the server using the port

		Args:
			server (str): IP address of the server
			port (int):   Port of the server

		Raises:
			TypeError: The type of the input parameters is not valid
			ValueError: The value of the input parameters is invalid,
				(negative port, etc..)
		"""

		if not type(server) == str:
			raise TypeError

		if not type(port) == int:
			raise TypeError

		if port not in range(0,2**16-1):
			raise ValueError

		try:
			# Create IPv4 TCP socket:
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.__sock.connect ((server, port))

			# Start the client threads
			self.__create_threads(self.__sock)

		except Exception as e:
			# raise ClientError
			raise ClientError(str(e))
		# communicate ACK
		# communicate


	def Disconnect(self):
		"""
		Disconnect from a connected game server.

		Raises:
			ClientError: Not connected to any server
		"""
		try:
			self.__sock.close()
		except self.__sock.timeout:
			raise ClientError()

	def Scan(self, port):
		"""
		Scan for available servers on the given port number.

		Args:
			port (int): Port number

		Raises:
			TypeError: The port is not an int
			ValueError: The port number is invalid

		Returns:
			iter: Iterable collection of the available servers
		"""
		raise NotImplementedError

	def __create_threads(self, sock: socket.socket):
		"""
		Create send and receive threads for connection to the server

		Args:
			sock (socket): Accepted connection socket
			player_id (int): Index of the player on the client
		Raises:
			TypeError: sock is not a socket
			ServerError: ???
		"""
		senderThread = SenderClientThread(sock, self.__Comm)
		receiverThread = ReceiverClientThread(sock, self.__Comm)

		# Start the Threads
		senderThread.start()
		receiverThread.start()

	def handle_ready_ack(self, sender, player_id):
		"""
		TODO: DOCKSTRING
		"""
		self.ECClientReadyAck(self, player_id)
		logging.info("I am accepted with ID: %d" % player_id)

	def handle_ingame(self, sender, players):
		"""
		Handle in-game player updates
		Args:
			sender (CommProt): Caller of the event
			players (list): List of player object with current position.
		"""
		self.__players = players
		#logging.debug("Player data refreshed")

	def handle_server_error(self, sender, msg):
		"""
		Handle error messages from the server
		Args:
			sender (CommProt): Caller of the event
			msg (str): Error message sent by the server
		"""
		# TODO: Artem -> behandlung von error messages
		self.ECClientError(self, msg)
		self.__sock.close()
		logging.error("Server ERROR: %s" % msg)
		logging.info("Connection closed because of Server ERROR")

	def handle_ingame_update(self, sender, players):
		"""
		Handle in-game player updates
		Args:
			sender (CommProt): Caller of the event
			players (list): List of player object with current position.
		"""
		pass

	def handle_serever_notification (self, sender, msg):
		"""
		Handle server notification
		Args:
			sender

		"""
		logging.info(msg)
