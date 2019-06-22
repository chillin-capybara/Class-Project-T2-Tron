import threading
import socket
import logging
import time
from ..Core.Exceptions import ServerError
from ..Core.Exceptions import MessageError
from .CommProt import CommProt
class SenderThread(threading.Thread):
	"""
	Thread for implementing send functionality for TCP Clients
	Only responsible for Sending in-game data
	"""
	__hook = None
	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server
	__comm_proto = None

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

		self.__comm_proto: CommProt = comm_proto
		
		# Initialize the thread handler
		threading.Thread.__init__(self)
	
	def run(self):
		"""
		Operation of the running thread.

		Description:
			Sends update packets from the server whenever needed
		"""
		logging.debug("Starting sender thread %d..." % self.__player_id)
		try:
			while True:
				# Get the list of the players using the back hook to the server
				msg = self.__comm_proto.ingame(self.__hook.getPlayers(), None)
				self.__sockfd.send(msg)

				msg = self.__comm_proto.server_error("Playername already exists")
				self.__sockfd.send(msg)
				time.sleep(0.01)
		except:
			pass
		finally:
			logging.debug("Stopping sender thread %d..." % self.__player_id)



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
		self.__comm_proto: CommProt = comm_proto
		self.__comm_proto.EClientError += self.handle_client_error
		self.__comm_proto.EClientReady += self.handle_client_ready
		self.__comm_proto.EClientIngame += self.handle_client_ingame
		self.__comm_proto.EExitGame += self.handle_exit_game

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
			except MessageError:
				logging.warning("Invalid message received from player ID=%d" % self.__player_id)
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
		Args:
			sender (CommProt): Caller of the event
			msg (str): Error message from client
		"""
		logging.warning(msg)
	
	def handle_client_ready(self, sender, player):
		"""
		Handle client ready message
		Args:
			sender (CommProt): Caller of the event
			player (Player): Player data of the client for innitialization
		"""

		# Send the reeived data back to update the server
		self.__hook.hook_player_ready(self.__player_id, player)
	
	def handle_client_ingame(self, sender, player):
		"""
		Handle client ingame refresh messages
		Description:
			This function calls a hook on the local game server and updates the data of the
			current player
		Args:
			sender (CommProt): Caller of the event
			player (Player): Data of the current player send
		"""
		#Send the updated data with the player index to the main thread
		self.__hook.hook_client_ingame(self.__player_id, player)
	
	def handle_exit_game(self, sender):
		"""
		Handle an exit game request from the client
		Args:
			sender (CommProt): Caller of the event
		"""
		# Close the connectivity socket
		self.__sockfd.close()

		# Hook the event back to the server
		self.__hook.hook_player_leave(self.__player_id)
			