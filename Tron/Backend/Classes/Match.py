from typing import List
from ..Core.leasable_collections import LeasableObject
import logging

class Match(object):
	"""
	Match object on the server to serve a game
	"""

	# Name of the match
	__name : str = ""

	# Features of the game as a string array
	__features : List[str] = None

	__port_lease : LeasableObject = None
	__port : int = 0

	__count_players : int = 0
	__count_lifes : int = 0

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

	def __init__(self, name: str, features : List[str], port_lease : LeasableObject = None):
		"""
		Create a match with name and features
		
		Args:
			name (str): Name of the match
			features (List[str]): List of the features
			port_lease (LeasableObject): Port lease from the port range (server modes)
			port (int) : Port of the match, when in client mode
		"""
		# initialize the match parameters
		self.__name = name
		
		# Distinguish between server and client
		if port_lease != None: # SERVER MODE
			self.__port_lease = port_lease
			self.__port = self.__port_lease.getObj() # Get the leased port

		self.__count_players = self.get_feature_int("Players", features)
		self.__count_lifes = self.get_feature_int("Lifes", features)

		logging.debug(
			"Match %s initialized in port %d for %d players with %d lifes" %
			 (self.name, self.port, self.count_players, self.count_lifes))
	
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

