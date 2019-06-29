from ..Core.globals import *

class Lobby(object):
	"""
	Game lobby object for the Tron Game
	NOTE:
		Extendable for Pong, too
	"""

	__port = 0 # Change is not allowed after initialization

	__games : list   = None # List of games Here only Tron
	__matches : list = None # List of matches in the Lobby 

	def __init__(self, port: int):
		"""
		Initialize a lobby on the server, to create games in
		
		Args:
			port (int): Port of the Lobby on the server.
		
		Raises:
			TypeError: Invalid argument types
			ValueError: Invalid port range
		"""

		if type(port) is not int:
			raise TypeError
		
		if port not in LOBBY_PORT_RANGE:
			raise ValueError("The given port is not in the specified range.")
		
		self.__port = port
	
	@property
	def port(self) -> int:
		"""
		Port number of the lobby on the server
		"""
		return self.__port
