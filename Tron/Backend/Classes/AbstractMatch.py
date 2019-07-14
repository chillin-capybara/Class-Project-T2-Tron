from abc import ABC, abstractmethod
from .HumanPlayer import HumanPlayer
from typing import List
from .RectangleArena import RectangleArena, DieError
from ..Core.Event import Event
import logging

class AbstractMatch(ABC):
	"""
	Abstract match class for defining all the necessarry properties of a match
	NOTE
		This class inherits from the ABC Metaclass
	"""

	_host: str = "" # Host of the match
	_port: int = 0  # Port of the match
	_name: str = "" # Name of the current match
	_game: str = 'Tron'

	_players: List[HumanPlayer] = None # list of player in the match

	_arena: RectangleArena = None # Arena of the match

	# Match features
	_feat_lifes: int   = 0
	_feat_players: int = 0
	_feat_slots: int = 0

	EInit: Event = None   # Event which is called, when the match is initialzed
	EClose: Event = None  # Event which is called, when the match is closed

	def __init__(self, host: str, name: str, features:List[str]):
		"""
		Initialize a match object with the hostname and its features

		Features of the match are fetched automatically.
		Args:
			host (str): Host IP adress of the match server.
			name (str): Name of the match
			features (List[str]): List of match features
		Raises:
			TypeError, ValueError, KeyError
		"""
		self._host = host
		self._name = name

		# Try to fetch the features
		self._feat_players = self.get_feature_value_int('Players', features)
		self._feat_lifes = self.get_feature_value_int('Lifes', features)
		
		try:
			# Try to set the feature slots
			self._feat_slots = self.get_feature_value_int('Slots', features)
		except:
			pass

		self._generate_default_struture()

		# Initialize events
		self.EInit  = Event()
		self.EClose = Event()

		# Call the init event
		self.EInit(self)
	
	def _generate_default_struture(self):
		self._players = [] # Create an empty list
		self._players.clear()
		# Initialize the list of players with default player objects
		for i in range(0, self.feat_players + 1): # Player zero is reserved for empty space
			player = HumanPlayer()
			player.set_lifes(self.feat_lifes)  # Set the default value of the player life
			self._players.append(player)

		# TODO Initialize the arena based on lobby property
		self._arena = RectangleArena("Testname", (40,40), 0, 0)

	@property
	def arena(self) -> RectangleArena:
		"""
		Arena of the current match
		"""
		return self._arena

	@property
	def host(self) -> str:
		"""
		Host of the match running on. In server mode host = ""
		"""
		return self._host

	@property
	def port(self) -> int:
		"""
		Port of the match is running on. Alays 0 in client mode
		"""
		return self._port
	
	@property
	def game(self) -> str:
		"""
		Name of the game the match belongs to (Tron/Pong)
		"""
		return self._game

	@property
	def name(self) -> str:
		"""
		Name of the match
		"""
		return self._name

	@property
	def feat_players(self) -> int:
		"""
		Number of player slots available in the match
		"""
		return self._feat_players

	@property
	def feat_lifes(self) -> int:
		"""
		Number of lifes available for a player in the match
		"""
		return self._feat_lifes

	@property
	def feat_slots(self) -> int:
		"""
		Number of available slots on the server
		"""
		return self._feat_slots
	
	@property
	def features(self) -> str:
		"""
		Features of the match as a string list
		"""
		return self.get_features()
	
	@property
	def players(self) -> List[HumanPlayer]:
		"""
		List of players in the match. Player ZERO is ignored
		"""
		return self._players[1:]

	def get_feature_string(self) -> str:
		"""
		Get the features of the match as a string.

		Returns:
			str: Features
		"""
		if self.feat_slots > 0:
			string = "BASIC || Players: %d || Lifes: %d || Slots: %d" % (self.feat_players, self.feat_lifes, self.feat_slots)
		else:
			string = "BASIC || Players: %d || Lifes: %d" % (self.feat_players, self.feat_lifes)
		return string
	
	def get_features(self):
		"""
		Get the a string list of match features
		Returns:
			str: Features of the created match
		"""
		flist = ['BASIC']
		flist.append('Players')
		flist.append(self.feat_players)
		flist.append('lifes')
		flist.append(self.feat_lifes)

		if self.feat_slots > 0: # If the slots feature is recodnized
			flist.append("Slots")
			flist.append(self.feat_slots)
		return flist

	def get_feature_value_int(self, name: str, features: List[str]) -> int:
		"""
		Get an integer parameter from the features list
		The feature name is case ignorant, so: Players is the same as players

		Args:
			name (str): Name of the feature to get
			features (List[str]): List of the features
		Raises:
			Keyerror: Feature not found
		"""
		take_next = False
		for feature in features:
			if feature == name:
				# Case sensitive take
				take_next = True
			elif type(feature) is str and feature.lower() == name.lower():
				# Case insensitive take
				take_next = True
			elif take_next:
				return int(feature)

		raise KeyError
