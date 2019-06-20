import threading
import socket
import logging
from ..Core.Exceptions import ServerError
class SenderThread(threading.Thread):
	"""
	Thread for implementing send functionality for TCP Clients
	Only responsible for Sending in-game data
	"""
	__hook = None
	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server

	def __init__(self, hook, sockfd, comm_proto, player_id):
		"""
		Initializes a new thread for a client with an accepted new tcp connection
		
		Args:
			sockfd (socket): Accepted socket from sock.accept
			comm_proto (CommProt): Instance of communication protocoll
			player_id (int): Index of the player on the server
		Raises:
			TypeError: Invalid Argument types
		TODO: Type checking with Comm Protocoll
		"""

		self.__hook = hook
		
		if type(sockfd) == socket.socket:
			self.__sockfd = sockfd
		else:
			raise TypeError
		
		if type(player_id) == int:
			self.__player_id = player_id
		else:
			raise TypeError
		
		# Initialize the thread handler
		threading.Thread.__init__(self)
	
	def run(self):
		"""
		Operation of the running thread.

		Description:
			Sends update packets from the server whenever needed
		"""
		pass


class ReceiverThread(threading.Thread):
	"""
	Thread for implementing send functionality for TCP Clients.

	Responsible for handling request - response communication and receiving new player data 
	"""
	__hook = None
	__sockfd = None # Socket for client communication
	__comm_proto = None
	__player_id = None # Player index of the player on the server

	def __init__(self, hook, sockfd, comm_proto, player_id):
		"""
		Initializes a new thread for a client with an accepted new tcp connection
		
		Args:
			sockfd (socket): Accepted socket from sock.accept
			comm_proto (CommProt): Instance of communication protocoll
			player_id (int): Index of the player on the server
		Raises:
			TypeError: sockfd is not a socket
		TODO: CHECK COmm PROTO
		"""
		self.__hook = hook

		if type(sockfd) == socket.socket:
			self.__sockfd = sockfd
		else:
			raise TypeError
		
		# Set the communication protocoll
		self.__comm_proto = comm_proto
		self.__comm_proto.EClientError += self.handle_client_error
		self.__comm_proto.EClientReady += self.handle_client_ready
		self.__comm_proto.EClientIngame += self.handle_client_ingame

		if type(player_id) == int:
			self.__player_id = player_id
		else:
			raise TypeError

		# Initialize the thread handler
		threading.Thread.__init__(self)
	
	def run(self):
		"""
		Operation of the running thread.

		Description:
			Receives update packets from the server whenever needed
		"""
		logging.debug("Starting receiver thread %d..." % self.__player_id)
		while True:
			try:
				data = self.__sockfd.recv(1500)
				if data == b'':
					# Disconnect
					self.__sockfd.close()
				else:
					self.__comm_proto.process_response(data)
			except ValueError as v:
				# Invalid message was sent
				logging.warning("Invalid data received." + str(v))
				logging.debug(data)
			except Exception:
				# Connection is broken: Hook that player is leaving
				self.__hook.hook_player_leave(self.__player_id)
				break
		logging.debug("Closing receiver thread %d..." % self.__player_id)
	
	def handle_client_error(self, sender, msg):
		"""
		Handler client error coming from a specific client
		"""
		logging.warning(msg)
	
	def handle_client_ready(self, sender, player):
		"""
		Handle client ready message
		"""

		# Send the reeived data back to update the server
		self.__hook.hook_player_ready(self.__player_id, player)
	
	def handle_client_ingame(self, sender, player):
		"""
		Handle client ingame refresh
		"""
		#Send the updated data with the player index to the main thread
		self.__hook.hook_client_ingame(self.__player_id, player)
			