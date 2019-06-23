import threading
import time
import socket
import math
from .Factory import Factory
from ..Core.Exceptions import MessageError
from random import randint
import names
import logging
from ..Core.Event import Event

class SenderClientThread(threading.Thread):
	"""
	Thread for implementing send functionality fot TCP Server
	Responsible for sending just the in-game data
	"""
	__sockfd = None # Socket for client communication
	__player_id = None # Player index of the player on the server
	__Comm = None

	def __init__(self, sockfd, comm):
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
			myplayer.setPosition(randint(0,200), randint(0,200))
			sent_bytes = self.__sockfd.send(self.__Comm.client_ingame(myplayer))

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

	EIngameUpdate = None
	EServerNotification = None

	def __init__(self, sockfd, comm):
		"""
		Initializes a new thread for a client with an accepted new tcp connection
		
		Args:
			sockfd (socket): Accepted socket from sock.accept
			player_id (int): Index of the player on the server
		Raises:
			TypeError: sockfd is not a socket
		"""
		
		self.EIngameUpdate = Event()
		self.EServerNotification = Event()
		
		if type(sockfd) == socket.socket:
			self.__sockfd = sockfd
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
		logging.debug("Receiver thread started...")
		while True:
			try:
				data = self.__sockfd.recv(1500)
				self.__Comm.process_response(data)
			except MessageError:
				# Invalid message was received / Processed
				logging.warning("Invalid message received from server")

		logging.debug("Receiver thread stopped stopped")