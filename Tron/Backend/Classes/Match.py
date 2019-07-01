from typing import List
from ..Core.leasable_collections import *
from ..Core.Event import Event
from .BasicComm import BasicComm
from .RectangleArena import DieError, RectangleArena
from .HumanPlayer import HumanPlayer
from ..Core.globals import *
import logging
import socket
import threading
import time
from ..Core.InteropComm import InteropComm
from ..Core.matrix import *

SPLITTER = InteropComm()

class Match(object):
	"""
	Match object on the server to serve a game
	"""

	__game = "Tron"

	# Name of the match
	__name : str = ""

	# Features of the game as a string array
	__features : List[str] = None

	__port_lease : LeasableObject = None
	__port : int = 0

	__count_players : int = 0
	__count_lifes : int = 0

	__player_slots : LeasableList = None # List of player ID's
	__players : List[HumanPlayer] = None # List of players 0: is reserved

	__player_addresses : list = None # List of socket addresses to send data to

	EStart : Event = None # Start event of the match

	__updsock : socket.socket = None # UDP Socket for sending and receiving
	__comm : BasicComm = None
	__arena :RectangleArena = None
	__seq_send : list = None # List of sequence number per connection
	__seq_recv : list = None # List of sequence numbers per connection

	__clientsock :socket.socket = None
	__last_update_seq = 0 # Last update sequence from the server

	@property
	def port(self) -> int:
		"""
		Port of the match running on.
		"""
		return self.__port

	@property
	def count_players(self) -> int:
		"""
		Number of player slots available in the match
		"""
		return self.__count_players
	
	@property
	def count_lifes(self) -> int:
		"""
		Get the numner of lifes for a player in the match.
		"""
		return self.__count_lifes
	
	@property
	def name(self) -> str:
		"""
		Name of the current match
		"""
		return self.__name
	
	@property
	def game(self) -> str:
		"""
		Game type of the match
		"""
		return self.__game

	def __init__(self, game:str, name: str, features : List[str], port_lease : LeasableObject = None):
		"""
		Create a match with name and features
		
		Args:
			name (str): Name of the match
			features (List[str]): List of the features
			port_lease (LeasableObject): Port lease from the port range (server modes)
			port (int) : Port of the match, when in client mode
		"""
		# initialize the match parameters
		self.__game = game
		self.__name = name
		
		# Distinguish between server and client
		if port_lease != None: # SERVER MODE
			self.__port_lease = port_lease
			self.__port = self.__port_lease.getObj() # Get the leased port

		# Set the matches features
		self.set_features(features)

		self.EStart = Event('port', 'player_ids', 'players') # Simple Event to notify the joined playes to that the match is starting

		# Initialize the communication protocoll
		self.__comm = BasicComm()

		# Initialize an empty list of player adresses
		self.__player_addresses = []

		self.__arena = RectangleArena("Test arena", (100,100), 1, 0)

		logging.debug(
			"Match %s initialized in port %d for %d players with %d lifes" %
			 (self.name, self.port, self.count_players, self.count_lifes))
	
	def set_features(self, features: List[str]):
		"""
		Update the features of the match
		
		Args:
			features (List[str]): Features
		"""
		try:
			self.__count_players = self.get_feature_int("Players", features)
			self.__count_lifes = self.get_feature_int("Lifes", features)
		except:
			pass
			#raise KeyError("Players or Lifes feature cannot be fetched")

	@property
	def features(self):
		"""
		Features of the match represented by a string list
		"""
		return self.get_features()

	@property
	def featureString(self) -> str:
		"""
		Features of the match formatted as string
		"""
		return self.get_feature_string()

	def get_features(self) -> List[str]:
		"""
		List the features of the match
		
		Returns:
			List[str]: List of features
		"""
		features = ['BASIC', 'Players', self.count_players, 'Lifes', self.count_lifes]
		return features
	
	def get_feature_string(self) -> str:
		"""
		Get the features of the match as a string.
		
		Returns:
			str: Features
		"""
		string = "BASIC || Players: %d || Lifes: %d" % (self.count_players, self.count_lifes)
		return string
	
	def get_feature_int(self, name: str, features: List[str]) -> int:
		"""
		Get an integer parameter from the features list
		
		Args:
			name (str): Name of the feature to get
			features (List[str]): List of the features
		Raises:
			Keyerror: Feature not found
		"""
		take_next = False
		for feature in features:
			if feature == name:
				take_next = True
			elif take_next == True:
				return int(feature)
		
		raise KeyError
	
	def create(self):
		"""
		Create a match from the pre-initialzied object
		"""
		# Create the list of playerIDs
		pids = list(range(1,self.count_players+1))
		self.__player_slots = LeasableList(pids)

		# Create the player objects, but leave the 0th player empty
		self.__players = []
		self.__players.append(HumanPlayer()) # Leave the index 0 empty

		self.__seq_recv = []
		self.__seq_send = []

		for i in range(1,self.count_players+1):
			self.__players.append(HumanPlayer())
			self.__seq_recv.append(0)
			self.__seq_send.append(0)

	def __client_receiver(self):
		"""
		Receiver thread of the client to receive updates
		"""
		logging.info("Starting the match client thread...")
		# Create client socket
		self.__clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		
		while True:
			data, conn = self.__clientsock.recvfrom(UDP_RECV_BUFFER_SIZE)
			# TODO FETCH DATA


	
	def __receiver_thread(self):
		"""
		Receive the direction updates from players, and the game start request
		"""
		try:
			logging.info("Initializing UPD Game server on port %d" % self.port)
			# Create and bind the socket onto the match's port
			self.__updsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			self.__updsock.bind(("", self.port))

			while True:
				data, conn = self.__updsock.recvfrom(UDP_RECV_BUFFER_SIZE)
				if conn not in self.__player_addresses:
					self.__player_addresses.append(conn)
				
				seq, msg = data.decode("UTF-8").split(" ", 1) # Split the sequence number and the message
				packet = bytes(msg, "UTF-8") # Convert the packet back to bytes
				self.__comm.process_response(packet) # Process the response of the packet
		except Exception as e:
			logging.error("Match handler stopped. Reason: %s" % str(e))
	
	def __sender_thread(self):
		"""
		Send the updates of the matrix to every player that is in the list of addresses
		"""
		logging.info("Starting sender thread to keep the clients updated")
		try:
			while True:
				try:
					cindex = 0
					for conn in self.__player_addresses:
						# Get the matrix to send: Always get a freash matrix
						matrix = self.__arena.matrix

						# Split the matrix -> Send every part as an update request to the client
						splitted = SPLITTER.matrix_split(matrix, MAX_MATRIX_SIZE)
						for key in splitted.keys():
							packet = self.__comm.update_field(key, splitted[key])
							seq = bytes("%d " % self.__seq_send[cindex], "UTF-8")
							packet = seq + packet

							# Constantly send updates to every client
							self.__updsock.sendto(packet, conn)
							self.__seq_send[cindex] += 1 # Increment the sent index
						
						# Increment the index of the connection
						cindex += 1
				except Exception as e:
					logging.warning("Error while sending. %s" % str(e))
		except Exception as e:
			logging.error("Game updater has stopped. Reason: %s" % str(e))
	
	def __field_updater_thread(self):
		"""
		Update the field with stepping the players to the current direction
		"""
		logging.info("Starting stepper thread, to update the player positions...")
		while True:
			try:
				for player in self.__players:
					try:
						player.step()
						self.__arena.player_stepped(player.getPosition())
					except DieError:
						logging.info("Player %s died" % player.getName())
			except Exception as e:
				logging.warning("Error while updating player positions. Reason: %s" % str(e))
			
			time.sleep(0.5) # 2 Updates per second
	
	def serve_match(self):
		"""
		Start the server-side of the match
		"""
		logging.info("Starting hosting the match: %s on port %d" % (self.name, self.port))
		senderThread = threading.Thread(target=self.__sender_thread)
		receiverThread = threading.Thread(target=self.__receiver_thread)
		updaterThread = threading.Thread(target=self.__field_updater_thread)


		# Append the event handlers for the server side
		self.__comm.ENewDirection += self.handle_new_direction

		senderThread.start()
		receiverThread.start()
		updaterThread.start()


		
	def lease_player_id(self) -> LeasableObject:
		"""
		Lease a player ID from the list of player_ids
		
		NOTE
			The Player ID has to be freed, when the connnection is broken
		Returns:
			LeasableObject: Wrapped object of the playerid
		"""
		return self.__player_slots.lease()
	
	def check_for_start(self):
		"""
		Check if the match can be started or not
		"""

		if self.__player_slots.count_free() == 0:
			logging.info("Match %s is full, starting the match..." % self.name)

			# Generate the params string from the players
			player_ids = list(range(1,self.count_players+1))
			players = self.__players[1:] # Ignore player 0

			# All slots reserved
			self.EStart(self, port=self.port, player_ids=player_ids, players=players)
	
	def handle_new_direction(self, player_id, direction):
		"""
		Handle when a player sets a new direction
		
		Args:
			player_id (int): ID of the player in the match
			direction (tuple): New direction
		"""
		logging.info("Player ID=%d has a new direction %s" % (player_id, str(direction)))
		self.__players[player_id].setVelocity(direction[0], direction[1])