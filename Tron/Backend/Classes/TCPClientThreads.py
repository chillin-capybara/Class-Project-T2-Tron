import threading
import time
import socket
import math
from .Factory import Factory
from ..Core.Exceptions import MessageError
from random import randint
import logging
from ..Core.Event import Event
from .ClientStateMachine import StateMaschine

class SenderClientThread(threading.Thread):
	"""
	Thread for implementing send functionality fot TCP Server
	Responsible for sending just the in-game data
	"""
	__sockfd: socket.socket = None # Socket for client communication
	__player_id = None # Player index of the player on the server
	__Comm = None
	__hook = None
	

	def __init__(self, sockfd, comm, hook):
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
		self.__hook = hook
		StateMaschine.change(StateMaschine.CLIENT_READY)
		# Initialize the thread handler
		threading.Thread.__init__(self)

	def run (self):
		"""
		Operation for the running threads
		Description:
			sends updates of the in-game state to the server
			whenewer it is needed
		"""
		self.__sockfd.send(self.__Comm.client_ready(self.__hook.me))
		StateMaschine.change(StateMaschine.CLIENT_WAITING)
		time.sleep(1)
		if StateMaschine.state == StateMaschine.CLIENT_INGAME:			
			while True:
				sent_bytes = self.__sockfd.send(self.__Comm.client_ingame(self.__hook.me))

				#self.__sockfd.send(self.__Comm.client_error("Error CLIENT"))
				time.sleep(0.01)
			pass
		else:
			pass #TODO: CLIENT NOT IN GAME implementation


class ReceiverClientThread(threading.Thread):
	"""
	Thread for implementing send functionality for TCP Clients.

	Responsible for handling request - response communication and receiving new player data 
	"""

	__sockfd: socket.socket = None # Socket for client communication
	__player_id = None # Player index of the player on the server
	__Comm = None
	__stateFSM = None
	__hook = None

	EIngameUpdate = None
	EServerNotification = None

	def __init__(self, sockfd, comm, hook):
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
		#self.__stateFSM = makros.INIT_STATE
		self.__hook = hook
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
				#logging.warning("Invalid message received from server")
				pass
		logging.debug("Receiver thread stopped stopped")

	# def clientFSM (self):
	# 	"""
	# 	TODO: DOCSTRING

	# 		Args: newState (int) New State
	# 	"""
	# 	# FSM
	# 	if self.__stateFSM == makros.INIT_STATE:
	# 		pass

	# 	elif self.__stateFSM == makros.CLIENT_READY:
	# 		logging.info ("Ready, waiting for ACK")

	# 	elif self.__stateFSM == makros.CLEINT_READY_ACK:
	# 		logging.info ("Ready ACK recieved")

	# 	elif self.__stateFSM == makros.CLIENT_ERROR:
	# 		self.__sockfd.close()
	# 		logging.info ("Client ERROR")
	# 	pass
