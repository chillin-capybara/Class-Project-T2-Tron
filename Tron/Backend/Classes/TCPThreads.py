import threading
import socket

class SenderThread(threading.Thread):
	"""
	Thread for implementing send functionality for TCP Clients
	Only responsible for Sending in-game data
	"""

	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server

	def __init__(self, sockfd, player_id):
		"""
		Initializes a new thread for a client with an accepted new tcp connection
		
		Args:
			sockfd (socket): Accepted socket from sock.accept
			player_id (int): Index of the player on the server
		Raises:
			TypeError: Invalid Argument types
		"""
		
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

	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server

	def __init__(self, sockfd, player_id):
		"""
		Initializes a new thread for a client with an accepted new tcp connection
		
		Args:
			sockfd (socket): Accepted socket from sock.accept
			player_id (int): Index of the player on the server
		Raises:
			TypeError: sockfd is not a socket
		"""
		
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
			Receives update packets from the server whenever needed
		"""
		pass