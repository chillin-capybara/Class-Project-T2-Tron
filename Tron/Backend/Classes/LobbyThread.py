import threading
import socket
import logging

from ..Core.Hook import Hook
from .BasicComm import BasicComm
from ..Core.globals import *

class LobbyThread(threading.Thread):
	"""
	Thread for handling the lobby requests and responses for every client.
	"""

	__hook_get_games : Hook = None
	__hook_get_matches : Hook = None

	__sock : socket.socket = None

	__comm : BasicComm = None

	def __init__(self, sock:socket.socket, hook_get_games, hook_get_matches):
		"""
		Create a new lobbythread for a client
		
		Args:
			socket (socket.socket): Connected socket from the client
			hook_get_games (callable): Hook to get the list of the games in the lobby
			hook_get_matches (callable): Hook to get the list of the matches in the lobby
		"""

		self.__hook_get_games = Hook(hook_get_games)
		self.__hook_get_matches = Hook(hook_get_matches) # (game=)

		# Set the socket
		self.__sock = sock

		# Initialize the communication
		self.__comm = BasicComm()

		# Initialize event handlers
		self.__comm.EHello += self.handle_hello

		logging.debug("Lobby thread initialized.")
		threading.Thread.__init__(self)

	def run(self):
		"""
		Loop function of the thread for handling every lobby client connection.
		"""
		try:
			logging.info("Starting lobby thread...")
			while True:
				# Receive data from the client
				data = self.__sock.recv(CONTROL_PROTOCOL_RECV_SIZE)

				if data == "" or not data: # Break the loop, if the connection is broken
					break

				try:
					# Pipeline it into the processor
					self.__comm.process_response(data)
				except Exception as e:
					# Message processing error
					logging.warning(str(e))
		except Exception as e:
			logging.error("Connection to the client stopped: %s" % str(e))
		finally:
			logging.info("Closing connection to [FILL THIS OUT]")
	
	def handle_hello(self, sender, playername: str, features: list):
		"""
		Handle EHello from the communication protocoll
		
		Args:
			sender (CommProt): Caller of the event
			name (str): Name of the player, who said hello
			features (list): Client features
		"""
		logging.info("%s said hello with the following features: %s" % (playername, str(features)))

		# Answer back with welcome message
		packet = self.__comm.welcome(SERVER_FEATURES)
		self.__sock.send(packet)

		logging.info("Answering with server features: %s" % str(SERVER_FEATURES))

