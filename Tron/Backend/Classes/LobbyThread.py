import threading
import socket
import logging

from typing import List

from ..Core.Hook import Hook
from ..Core.Event import Event
from .BasicComm import BasicComm
from ..Core.globals import *
from .Match import Match

class LobbyThread(threading.Thread):
	"""
	Thread for handling the lobby requests and responses for every client.
	"""

	__hook_get_games : Hook = None
	__hook_get_matches : Hook = None

	__sock : socket.socket = None

	__comm : BasicComm = None

	__ECreateGame : Event = None # Event when a the creation of a new match is requested.

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
		self.__comm.EListGames += self.handle_list_games
		self.__comm.ECreateMatch += self.handle_create_match
		self.__comm.EListMatches += self.handle_list_matches

		logging.debug("Lobby thread initialized.")
		threading.Thread.__init__(self)

		# Initialize the __ECreateGame
		self.__ECreateGame = Event('game', 'name', 'features')
	
	@property
	def ECreateGame(self):
		"""
		Event to be called when the creation of a new match is requested
		
		Returns:
			Event: Event to add callbacks to
		"""
		return self.__ECreateGame
	@ECreateGame.setter
	def ECreateGame(self, new: Event):
		self.__ECreateGame = new

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
	
	def handle_list_games(self, sender):
		"""
		Handlt the EAvailableGames from the Communication protocol
		
		Args:
			sender (CommProt): Caller of the event
		"""
		logging.info("Sending the list of available games...")
		list_game = self.__hook_get_games()
		packet = self.__comm.available_games(SERVER_GAMES)
		self.__sock.send(packet)
	
	def handle_create_match(self, sender, game:str, name: str, features: List[str]) -> None:
		"""
		Handle the create match commands from the client.
		
		Args:
			sender (CommProt): Caller of the event
			game (str): Name of the game = Tron/Pong
			name (str): Name of the game
			features (List[str]): List of features in the game
		"""
		try:
			logging.info("Creating a new match %s/%s is requested with: %s" % (game, name, str(features)))
			self.ECreateGame(self, game=game, name=name, features=features)

			# If there are no errors: -> Send confirmation
			packet = self.__comm.match_created()
			self.__sock.send(packet)
		except Exception as e:
			# Failed to create the match
			# // TODO add error message sending
			logging.error("Error creating the match!")
	
	def send(self, data: bytes):
		"""
		Send data to the socket of the lobbythread
		
		Args:
			data (bytes): Data to be sent
		"""
		return self.__sock.send(data)

	def handle_list_matches(self, sender, game:str):
		"""
		Handle the list matches request from the client
		
		Args:
			sender (CommProt): Caller of the event
			game (str): Name of the game to list matches of
		"""
		logging.info("Sending list of matches for %s" % game)
		list_matches : List[Match] = self.__hook_get_matches()
		str_list = []

		for m in list_matches:
			str_list.append(m.name)

		# Generate protocoll message, SEND	
		packet = self.__comm.games(game, str_list)
		self.send(packet)