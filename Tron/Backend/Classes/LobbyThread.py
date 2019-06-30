import threading
import socket
import logging

from typing import List

from ..Core.Hook import Hook
from ..Core.Event import Event
from .BasicComm import BasicComm
from ..Core.globals import *
from ..Core.leasable_collections import *
from .Match import Match
from .HumanPlayer import HumanPlayer

class LobbyThread(threading.Thread):
	"""
	Thread for handling the lobby requests and responses for every client.
	"""

	__hook_get_games : Hook = None
	__hook_get_matches : Hook = None

	__sock : socket.socket = None

	__comm : BasicComm = None

	__ECreateGame : Event = None # Event when a the creation of a new match is requested.

	__hello_name :str = "JoeWorkingman" # Name of the player to be stored after the hello message
	__leased_player_id : LeasableObject = None

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
		self.__comm.EMatchFeatures += self.handle_match_features
		self.__comm.EJoinMatch  += self.handle_join_match

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
			try:
				self.__leased_player_id.free()
				logging.debug("Giving the player id free: %d" % self.__leased_player_id.getObj())
			except:
				pass # Player ID was not reserved
			logging.info("Closing connection to [FILL THIS OUT]")
	
	def handle_lobby_stop(self, sender):
		"""
		Handle the stop of the lobby object
		
		Args:
			sender ([type]): Caller lobby object
		"""
		self.Stop()

	def Stop(self):
		"""
		Stop the Lobbythread, when the server was stopped
		"""
		logging.info("Stopping the lobby is requested by the server.")
		self.__sock.close()

	def handle_hello(self, sender, playername: str, features: list):
		"""
		Handle EHello from the communication protocoll
		
		Args:
			sender (CommProt): Caller of the event
			name (str): Name of the player, who said hello
			features (list): Client features
		"""
		logging.info("%s said hello with the following features: %s" % (playername, str(features)))

		# Store the player's name
		self.__hello_name = playername

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
			
			# Check if the match exists.
			ex_matches = self.__hook_get_matches()
			c_with_name = sum(p.name == name for p in ex_matches)

			if c_with_name == 0:
				self.ECreateGame(self, game=game, name=name, features=features)
			else:
				logging.error("The match name %s is already reserver" % name)
				packet = self.__comm.failed_to_create("The name %s is already reserved for a match!" % name)
				self.send(packet)

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
	
	def handle_match_features(self, sender, name:str):
		"""
		Event handler for queriing the match features
		
		Args:
			name (str): Name of the match
		"""
		matches = self.__hook_get_matches()
		for match in matches:
			match : Match
			if match.name == name:
				# Match found
				logging.info("Sending match features: %s %s %s " % (match.game, match.name, match.features))
				packet = self.__comm.match(match.game, match.name, match.features)
				self.send(packet)
				return
		
		# If match not found
		logging.warning("Match %s not found on the server" % name)
		packet = self.__comm.game_not_exists(name)
		self.send(packet)

	def handle_join_match(self, sender, name: str, player: HumanPlayer):
		"""
		Handle when a client wants to join a match
		
		Args:
			sender ([type]): Caller of the event
			name (str): Name of the match to join
			player (HumanPlayer): Player
		"""
		logging.info("%s wants to join the match %s" % (self.__hello_name, name))

		# We have a color and a playername
		player.setName(self.__hello_name)

		# Check if the match exists
		ex_matches = self.__hook_get_matches()
		for match in ex_matches:
			match: Match
			if match.name == name:
				# Found the match
				self.__leased_player_id = match.lease_player_id()
				pid: int = self.__leased_player_id.getObj() # Get the id of the player

				# Tell the client the player id and the success of the join
				packet = self.__comm.match_joined(pid)
				self.send(packet)

				match.EStart += self.handle_match_started
				# Check for the Event to start
				match.check_for_start()
				return
		
		# Failed to join
		packet = self.__comm.failed_to_join("The match %s does not exists in the lobby!" % name)
		self.send(packet)

	def handle_match_started(self, sender, port, player_ids, players):
		"""
		Handle when the server starts the match
		Send out the notifications to all clients
		
		Args:
			sender (match): Caller of the event
			port (int) : Port of the match
			player_ids (list) : list of the available player ids
			players (list) : List of the player objects in the match
		"""
		logging.info("Notifying %s that the game %s has started" % (self.__hello_name, sender.name))
		# Generate match started package for every player in their thread
		packet = self.__comm.match_started(port, player_ids, players)
		self.send(packet)


