import threading
import time
import socket
import math
from .Factory import Factory
from random import randint
import names

class SenderClientThread(threading.Thread):
	"""
	Thread for implementing send functionality fot TCP Server
	Responsible for sending just the in-game data
	"""
	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server
	__Comm = None

	def __init__(self, sockfd, player_id, comm):
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

		self.__Comm = comm
		
		if type(player_id) == int:
			self.__player_id = player_id
		else:
			raise TypeError
		
		# Initialize the thread handler
		threading.Thread.__init__(self)
    
	def run (self):
		"""
		Operation for the running threads
		Description:
			sends updates of the in-game state to the server
			whenewer it is needed
		"""
		myplayer = Factory.Player(names.get_first_name(), 1)
		self.__sockfd.send(self.__Comm.client_ready(myplayer))
		time.sleep(1)
		while True:
			print("Sending..", flush=True)
			myplayer.setPosition(randint(0,200), randint(0,200))
			self.__sockfd.send(self.__Comm.client_ingame(myplayer))
			#self.__sockfd.send(self.__Comm.client_error("Error CLIENT"))
			time.sleep(0.01)
		pass

class ReceiverClientThread(threading.Thread):
	"""
	Thread for implementing send functionality for TCP Clients.

	Responsible for handling request - response communication and receiving new player data 
	"""

	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server
	__Comm = None

	def __init__(self, sockfd, player_id, comm):
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

		self.__Comm = comm

		# Initialize the thread handler
		threading.Thread.__init__(self)
	
	def run(self):
		"""
		Operation of the running thread.

		Description:
			Receives update packets from the server all the time
		"""
		try:
			while True:
				data = self.__sockfd.recv(1500)
				self.__comm_proto.process_response(data)
		except Exception as e:
			raise ServerError(e)
		pass