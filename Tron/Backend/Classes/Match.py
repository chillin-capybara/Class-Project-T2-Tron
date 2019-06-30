from typing import List
from ..Core.leasable_collections import *
from ..Core.Event import Event
from .HumanPlayer import HumanPlayer
import logging

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

	EStart : Event = None # Start event of the match

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

		for i in range(1,self.count_players+1):
			self.__players.append(HumanPlayer())
		
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
			self.EStart(self, port=port, player_ids=player_ids, players=players)