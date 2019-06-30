from typing import List
from ..Core.leasable_collections import *
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

	__player_slots : LeasableList = None


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

	def get_features(self) -> List[str]:
		"""
		List the features of the match
		
		Returns:
			List[str]: List of features
		"""
		features = ['BASIC', 'Players', self.count_players, 'Lifes', self.count_lifes]
		return features
	
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
		# Create a collection of leaseable player objects for server slots
		list_of_player = []
		for i in range(0, self.count_players):
			list_of_player.append(HumanPlayer())

		self.__player_slots = LeasableList(list_of_player)


