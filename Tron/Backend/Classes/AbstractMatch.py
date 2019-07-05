from abc import ABC, abstractmethod
from .HumanPlayer import HumanPlayer
from typing import List

class AbstractMatch(ABC):
	"""
	Abstract match class for defining all the necessarry properties of a match
	NOTE
		This class inherits from the ABC Metaclass
	"""

	_host: str = "" # Host of the match
	_port: int = 0  # Port of the match
	_name: str = "" # Name of the current match

	_players: List[HumanPlayer] = None # list of player in the match

	# Match features
	_feat_lifes: int   = 0
	_feat_players: int = 0

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
		# Try to fetch the features
		self._feat_players = self.get_feature_value_int('Players', features)
		self._feat_lifes = self.get_feature_value_int('Lifes', features)

		# Initialize the list of players with player objects
		for player in self._players:
			pass
			
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

	def get_feature_string(self) -> str:
		"""
		Get the features of the match as a string.

		Returns:
			str: Features
		"""
		string = "BASIC || Players: %d || Lifes: %d" % (self.feat_players, self.feat_lifes)
		return string

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
			if feature == name or feature.lower() == name.lower():
				take_next = True
			elif take_next:
				return int(feature)

		raise KeyError
