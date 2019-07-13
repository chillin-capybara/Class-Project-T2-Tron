from ..Core.globals import *
from ..Core.Hook import Hook
from ..Core.Event import Event
from .BasicComm import BasicComm
from .MatchServer import MatchServer
from .HumanPlayer import HumanPlayer
from .LobbyThread import LobbyThread
from .MatchClient import MatchClient
from ..Core.ThreadCollection import ThreadCollection
from .Match import Match
import socket
import logging
import threading
from typing import List
import queue
import time


# TODO Call UI Events only from the UI Thread

class Lobby(object):
	"""
	Game lobby object for the Tron Game
	NOTE:
		Extendable for Pong, too
	"""
	__host = "" # IP address of the server
	__port = 0 # Change is not allowed after initialization

	__games : list   = None # List of games Here only Tron
	__matches : List[MatchClient] = None # List of matches in the Lobby 

	__sock : socket.socket = None # Socket connection to the lobby
	__comm : BasicComm = None

	__hook_me : Hook = None

	__selected_match : MatchClient = None # Selected match to join

	__hook_lease_port : Hook = None
	__server_thread : threading.Thread = None
	__server_sock : socket.socket = None
	__server_threads : List[threading.Thread] = None

	__sendQ: queue.Queue() = None
	__recvQ: queue.Queue() = None
	__threadcollection : ThreadCollection = None

	__require_close = False

	EError : Event = None
	EMatchJoined : Event = None
	ELobbyStop : Event = None # Event to spread, when the server gets stopped
	EMatchStarted : Event = None

	def __init__(self, host: str, port: int, hook_me = None, hook_lease_port = None, parent=None):
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

		self.__host = host
		self.__port = port

		self.__parent__ = parent

		# Initialize the array of matches
		self.__matches = []

		# Initialize the collection of threads
		self.__threadcollection = ThreadCollection()

		# Initialize send und receiver queues
		self.__sendQ = queue.Queue()
		self.__recvQ = queue.Queue()

		# Initialize own events
		self.EError = Event('msg')
		self.EMatchJoined = Event('matchname')
		self.ELobbyStop = Event()
		self.EMatchStarted = Event() # Detalt event to start the GAME itself

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
		self.__comm.ELifeUpdate += self.handle_life_update

		# Initialize hook : Only for clients
		if hook_me != None:
			self.__hook_me = Hook()
			self.__hook_me.delegate(hook_me)
		else:
			# Only for servers
			self.__hook_lease_port = Hook(hook_lease_port)
	
	@property
	def parent(self):
		return self.__parent__

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
	def match(self) -> MatchClient:
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
				self.__create_thread(thread_sock, addr)
		except Exception as e:
			logging.error(str(e))
	
	def __create_thread(self, sock: socket.socket, conn):
		"""
		Create a thread on the server to handle client requests and responses simultaniously
		Args:
			sock (socket): Socket of the connection to handle
			conn (Addr):   Address struct of the connection
		"""
		# Initialzie all the thread hooks
		thread = LobbyThread(
							sock, conn,
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


	def __client_receiver_thread(self):
		"""
		Receiver thread, that receives message from the server asynchronously
		"""
		logging.info("Starting the receiver thread for the control protocoll...")
		try:
			while not self.__require_close:
				# Receive the data and forward it to the message processor
				packet = self.__sock.recv(CONTROL_PROTOCOL_RECV_SIZE)
				self.__recvQ.put(packet) # Enqueue the packet for processing
		except OSError:
			logging.info("Closing down the client's receiver")
		except Exception as exc:
			logging.error("Error occured while asynchronous receive. Reasor: %s", str(exc))
		
		logging.info("Control receiver thread closed.")
	
	def __client_sender_thread(self):
		"""
		Sender thread to send requests asynchronously
		"""
		try:
			logging.info("Client sender thread started")
			while not self.__require_close:
				if not self.__sendQ.empty():
					self.__sock.send(self.__sendQ.get())
		except OSError:
			logging.info("Stopping the clients lobby sender thread.")
		except Exception as exc:
			logging.error("Error occured while asynchronous send. Reasor: %s", str(exc))

		logging.info("Control sender thread closed.")
	
	def __message_processor(self):
		"""
		Process messages that are received by the client thread.
		NOTE:
			This is the caller thread of every Client operation in the Lobby!
		"""
		try:
			logging.info("Lobby client message processor thread started!")
			while not self.__require_close: # For active thread
				if not self.__recvQ.empty():
					# Block this thread, until there is anything in the queue
					self.__comm.process_response(self.__recvQ.get())
		except Exception as exc:
			logging.error("Error occured while asynchronous send. Reasor: %s", str(exc))

		logging.info("Control message processor thread closed.")
	
	def send(self, packet:bytes):
		"""
		Send a message over the client's socket to the server
		NOTE:
			This enqueues the packet for a send by the sender thread
		
		Args:
			packet (bytes): Message as bytes
		"""
		logging.info("Packet enqueued: %s", str(packet))
		self.__sendQ.put(packet)

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

			# Here to start the receiver thread
			# TODO Make a Stop client threads function
			receiver = threading.Thread(target=self.__client_receiver_thread)
			sender = threading.Thread(target=self.__client_sender_thread)
			processor = threading.Thread(target=self.__message_processor)
			self.__threadcollection += receiver
			self.__threadcollection += sender
			self.__threadcollection += processor


			# Start all the threads
			self.__threadcollection.start_all()

			# Send Hello message
			packet = self.__comm.hello(self.__hook_me(), CLIENT_FEATURES)
			self.send(packet)

		except Exception as e:
			logging.error("Error occured while saying hello: %s" % str(e))
	
	def close(self):
		"""
		Event handler for closing the client with all it's threads
		"""
		logging.info("Closing the Lobby client...")

		# Destroying the socket will close the receiver thread
		self.__sock.close()

		# Set the close flag -> Stop the sender and the processor threads
		self.__require_close = True

		self.__threadcollection.join_all()
		logging.info("Lobby all lobby client threads closed!")

	def list_games(self):
		"""
		Send a request to the server to list the available games
		"""
		try:
			# Create and send the request
			packet = self.__comm.list_games()
			self.send(packet)

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
			self.send(packet)

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
		self.send(packet)

		# Wait until the server lists the matches
		self.__comm.EMatch.wait_clear(0.3)
	
	def join_match(self, index: int):
		"""
		Join the selected match from the list
		
		Args:
			index (int): Index of the match in the list
		"""
		# Send a request to join the game
		logging.info("joining the match %s ..." % self.matches[index].name)
		packet = self.__comm.join_match(self.matches[index].name, self.__hook_me())
		self.send(packet)

		# Set the selected match
		self.__selected_match = self.matches[index]
	
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
			self.__matches.append(MatchClient(self.__host, name, self, self.__hook_me)) # // TODO Get features for every match

			# Send a request to query match features
			packet = self.__comm.match_features(name)
			self.send(packet)
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
		new_match = MatchServer(self.parent.available_ports, name, features)
		new_match.EClose += self.handle_match_close #Add event call back to remove the match
		self.__matches.append(new_match)
		logging.info("Match created!")
	
	def handle_match_close(self, sender: MatchServer):
		"""
		Handle, when a match is closed on the server and remove it from the collection
		
		Args:
			sender (MatchServer): Caller of the event
		"""
		self.__matches.remove(sender)
		logging.info("The match %s was removed from the server.", sender.name)

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

		# Set the player id in the match
		self.__selected_match.set_current_player_id(player_id)

		# Call the Lobby's event -> With the name of the match
		self.EMatchJoined(self, matchname=self.__selected_match.name)
	
	def handle_match_started(self, sender, port:int, players:list):
		"""
		Handle the event, when the match starts
		
		Args:
			sender ([type]): Caller of the event
			port (int): Port of the starting match
			pclist (list): list of player ids and colors
		"""
		logging.info("Match started on port %d with (pid,r,g,b): %s" % (port, str(players)))
		# Connect to the match server via udp and tcp for the control
		# Set the port of the match
		self.__selected_match.set_port(port)

		# Start match client
		self.__selected_match.open()

		# Notifty the UI to show the game
		self.EMatchStarted(self)
	
	def handle_life_update(self, sender, player_id:int, lifes:int):
		"""
		Handle life updates for every player in the current match.
		
		Args:
			sender (CommProt): Caller of the event
			player_id (int): ID of the player in the game
			score (int): Lives of the player left.
		"""
		self.match.life_udpate(player_id, lifes)
