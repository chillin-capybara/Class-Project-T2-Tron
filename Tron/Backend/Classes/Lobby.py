from ..Core.globals import *
from ..Core.Hook import Hook
from ..Core.Event import Event
from .BasicComm import BasicComm
from .HumanPlayer import HumanPlayer
from .LobbyThread import LobbyThread
from .Match import Match
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
	__matches : List[Match] = None # List of matches in the Lobby 

	__sock : socket.socket = None # Socket connection to the lobby
	__comm : BasicComm = None

	__hook_me : Hook = None

	__selected_match : Match = None # Selected match to join


	__hook_lease_port : Hook = None
	__server_thread : threading.Thread = None
	__server_sock : socket.socket = None
	__server_threads : List[threading.Thread] = None

	EError : Event = None
	EMatchJoined : Event = None
	ELobbyStop : Event = None # Event to spread, when the server gets stopped

	def __init__(self, host: str, port: int, hook_me = None, hook_lease_port = None):
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

		# Initialize the array of matches
		self.__matches = []

		# Initialize own events
		self.EError = Event('msg')
		self.EMatchJoined = Event('matchname')
		self.ELobbyStop = Event()

		# Intialize communication protocol : CLIENT EVENTS!!!!
		self.__comm = BasicComm()
		self.__comm.EWelcome += self.handle_welcome
		self.__comm.EAvailableGames += self.handle_available_games
		self.__comm.EMatchCreated += self.handle_match_created
		self.__comm.EGames += self.handle_list_matches
		self.__comm.EMatch += self.handle_match
		self.__comm.EServerError += self.handle_server_error
		self.__comm.EMatchStarted += self.handle_match_started
		self.__comm.EMatchJoined += self.handle_match_joined

		# Initialize hook : Only for clients
		if hook_me != None:
			self.__hook_me = Hook()
			self.__hook_me.delegate(hook_me)
		else:
			# Only for servers
			self.__hook_lease_port = Hook(hook_lease_port)
	
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
	
	@property
	def matches(self) -> List[Match]:
		"""
		Active matches in the lobby
		"""
		return self.__matches
	
	@property
	def match(self) -> Match:
		"""
		Selected match for waiting to start...
		"""
		return self.__selected_match

	def hook_get_games(self):
		"""
		Get the list of games in the lobby
		
		Returns:
			list: List of the game types ont he server
		"""
		return SERVER_GAMES
	
	def hook_get_matches(self):
		"""
		Return the matches running in the lobby
		// TODO Return a real list...
		"""
		return self.__matches
	
	def start_server(self):
		"""
		Start serving the lobby on the server
		"""
		# Initialize the list of threads
		self.__server_threads = []
		# Create a thread fot the server
		self.__server_thread = threading.Thread(target=self.__server)
		self.__server_thread.start()
	
	def Stop(self):
		"""
		Stop the lobby server with all it's parent threads
		"""
		logging.info("Stopping the lobby server was requested")
		# Trigger a socket close
		self.__server_sock.close()

		self.ELobbyStop(self)

	def handle_server_stop(self, sender):
		"""
		Handle the server stop
		
		Args:
			sender ([type]): GameServer
		"""
		self.Stop()

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
		# Add event handlers for the Lobby thread
		thread.ECreateGame += self.handle_create_game

		# Add Lobby stop event handler
		self.ELobbyStop += thread.handle_lobby_stop

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

	def list_games(self):
		"""
		Send a request to the server to list the available games
		"""
		try:
			# Create and send the request
			packet = self.__comm.list_games()
			self.__sock.send(packet)

			# Process the response
			resp = self.__sock.recv(CONTROL_PROTOCOL_RECV_SIZE)
			logging.debug(resp)
			self.__comm.process_response(resp)
		except Exception as e:
			logging.error(str(e))
	
	def create_match(self, game: str, name: str, settings: dict):
		"""
		Create a match in the lobby with the selected settings
		
		Args:
			game (str): Name of the game : Tron
			name (str): Name of the match
			settings (dict): Match settings
		NOTE:
			Settings take some mandatory fields (value can be changed):
			'Players' : 3,
			'Lifes' : 2
		"""
		try:
			logging.info("Creating match on server %s/%s..." % (game, name))
			features = ['BASIC', 'Players', settings['Players'], 'Lifes', settings['Lifes']]
			
			# Create protocolled message
			packet = self.__comm.create_match(game, name, features)

			# Send the request to the server
			self.__sock.send(packet)

			# Wait and process response
			self.__process_response()
		except Exception as e:
			logging.error("Error creating match: %s" % str(e))
	
	def list_matches(self, game:str):
		"""
		List matches in a lobby to a game
		
		Args:
			game (str): Tron / Pong
		"""
		# Empty the list of matches
		self.__matches.clear()

		logging.info("Listing matches for %s" % game)
		packet = self.__comm.list_matches(game)
		self.__sock.send(packet)

		# Wait and process the response
		self.__process_response()
	
	def join_match(self, index: int):
		"""
		Join the selected match from the list
		
		Args:
			index (int): Index of the match in the list
		"""
		# Send a request to join the game
		logging.info("joining the match %s ..." % self.matches[index].name)
		packet = self.__comm.join_match(self.matches[index].name, self.__hook_me())
		self.__sock.send(packet)

		# Set the selected match
		self.__selected_match = self.matches[index]
		
		# Automatically handle the response from the server
		self.__process_response()

	def __process_response(self):
		"""
		Get and process the response of the server
		"""
		# Process the response
		resp = self.__sock.recv(CONTROL_PROTOCOL_RECV_SIZE)
		logging.debug(resp)
		self.__comm.process_response(resp)
	
	def handle_welcome(self, sender, features: list):
		"""
		Event handler for receiving a welcome message form the server
		
		Args:
			sender   (CommProt): Caller of the event
			featrues (list): List of server features
		"""
		logging.info("The server welcomes you. Supported server features %s" % str(features))

	def handle_available_games(self, sender, games: List[str]):
		"""
		Event handler for handling the list of abailable games in a lobby
		
		Args:
			sender (CommProt): Caller of the evernt
			games (list): List of available games: Tron, Pong...
		"""
		logging.info("The following games are available in the server: %s" % str(games))
	
	def handle_list_matches(self, sender, game: str, matches: list):
		"""
		Event handler for handling the list of matches in a lobby with a specific game
		
		Args:
			sender (CommProt): Caller of the event
			game (str): Name of the game
			matches (list): List of matches available
		"""
		logging.info("The server %s:%d has the following matches for %s : %s" % (self.host, self.port, game, str(matches)))
		for matchname in matches:
			self.__append_match(matchname)

	def __append_match(self, name: str):
		"""
		Append a match to the collection of matches on the client side
		
		Args:
			name (str): Name of the match
		"""
		try:
			logging.debug("Match listed: %s" % name )
			self.__matches.append(Match('Tron', name, ['BASIC'])) # // TODO Get features for every match

			# Send a request to query match features
			packet = self.__comm.match_features(name)
			self.__sock.send(packet)
			self.__process_response()
		except Exception as e:
			logging.error("Error appending match %s. Reason: %s" % (name, str(e)))
	
	def handle_match_features(self, sender, game: str, name: str, features: List[str]):
		"""
		Handle the listing of match features for a specific match on the server
		
		Args:
			sender (CommProt): Caller of the event
			game (str): Name of the game (Tron/Pong...)
			name (str): Name of the match
			features (List[str]): List of features on the match
		"""
		logging.info("The match %s in %s has the features: %s" % (name, game, str(features)))
	
	def handle_match_created(self, sender):
		"""
		Handle a match created event from the server
		
		Args:
			sender (CommProt): Caller of the event
		"""
		logging.info("Match created successfully!")
		# // TODO Inform the UI

	def handle_create_game(self, sender, game:str, name:str, features : List[str]):
		"""
		Handle the creation of a new match, when requested from a LobbyThread
		NOTE:
			THIS IS A SERVER EVENT HANDLER!!!
		
		Args:
			sender (LobbyThread): Caller of the event
			game (str): Name of the game Tron/Pong
			name (str): Name of the match
			features (List[str]): List of the features
		"""
		# Create a new match object and lease a port from the server's collection
		new_match = Match(game, name, features, self.__hook_lease_port())
		new_match.create()
		self.__matches.append(new_match)
		logging.info("Match created!")

	def handle_match(self, sender, game:str, name:str, features: List[str]):
		"""
		Event handler for getting the match features
		
		Args:
			sender ([type]): Caller of the event
			game (str): Name of the game
			name (str): Name of the match
			features (List[str]): Match features
		"""
		try:
			for match in self.__matches:
				if match.game == game and match.name == name:
					match.set_features(features)
					logging.debug("Match %s has the features: %s" % (name, features))
					return
			
			logging.warning("Match %s not found in the lobby." % name)
		except Exception as e:
			logging.error("Error while setting the match features of %s to %s. Reason: %s" % (name, str(features), str(e)))
	
	def handle_server_error(self, sender, msg:str):
		"""
		Handle the error message from the server
		
		Args:
			sender ([type]): Caller of the event
			message (str): Error message
		"""
		# Simply log the error
		logging.error(msg)
		
		# Pass the error along to the client class
		self.EError(self, msg=msg)
	
	def handle_match_joined(self, sender, player_id:int):
		"""
		Handle a match_joined resposne from the server
		
		Args:
			sender (Any): Caller of the event
			player_id (int): Player id of the current player
		"""
		logging.info("The server accepted you to join the game with id=%d" % player_id)

		# Call the Lobby's event -> With the name of the match
		self.EMatchJoined(self, matchname=self.__selected_match.name)
	
	def handle_match_started(self, sender, port:int, pclist:list):
		"""
		Handle the event, when the match starts
		
		Args:
			sender ([type]): Caller of the event
			port (int): Port of the starting match
			pclist (list): list of player ids and colors
		"""
		logging.info("Match started on port %d with (pid,r,g,b): %s" % str(pclist))
		# Connect to the match server via udp and tcp for the control
