class Server(object):
	"""
	Interface for a game server
	"""

	def __init__(self, host, port):
		"""
		Initialize the game server with the given game and network settings

		Args:
			host (str): IP address of the host. "" for default mode
			port (str): Port to start the listening server on
		
		Raises:
			TypeError: Host is not string or port is not int
			ValueError: Invalid host or port value
			ServerError: Error in the network initialization
		"""
		raise NotImplementedError
	
	def setArena(self, arena):
		"""
		Set the arena of the game server

		Args:
			arena (Arena): Arena object created for the game
		
		Raises:
			TypeError: The object is not an arena.
			ServerError: The arena type doesn't exist on the server, or ...
				the server is still running.
		"""
		raise NotImplementedError
	
	def setPlayerNumber(self, players):
		"""
		Set the number of the players who will play the game
		
		Args:
			players (int): Number of the players the server starts the game with.
		
		Raises:
			TypeError: players is not an integer
			ValueError: Players is not a valid number
			ServerError: The server is still running.
		"""
		raise NotImplementedError
	
	def getArena(self):
		"""
		Get the arena the game server hosts.

		Returns:
			Arena: Currently active arena object
		"""
		raise NotImplementedError

	def getPlayerNumber(self):
		"""
		Get the number of players currently on the server.

		Returns:
			int: Number of players
		"""
		raise NotImplementedError

	def Start(self):
		"""
		Start the server with the given game settings.

		Raises:
			ServerError: Problem with starting up the server
		"""
		raise NotImplementedError
	
	def Stop(self):
		"""
		Closes a running game and stops the server.

		Raises:
			ServerError: Error while closing down
		"""
		raise NotImplementedError
	
	def getPlayers(self):
		"""
		Get the collection of players connected to the server

		Returns:
			iter: List of the players connected to the server
		
		Raises:
			ServerError: Server is not running
		"""
		raise NotImplementedError
	