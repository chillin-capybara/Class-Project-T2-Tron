class Client(object):
	"""
	Client Interface for the game server
	"""

	def attachPlayersUpdated(self, callback):
		"""
		TODO: DOC
		"""
		raise NotImplementedError

	def Connect(self, server, port):
		"""
		Connect to the server using the port

		Args:
			server (str): IP address of the server
			port (int):   Port of the server
		
		Raises:
			TypeError: The type of the input parameters is not valid
			ValueError: The value of the input parameters is invalid, 
				(negative port, etc..)
		"""
		raise NotImplementedError
	
	def Disconnect(self):
		"""
		Disconnect from a connected game server.

		Raises:
			ServerError: Not connected to any server
		"""
		raise NotImplementedError
	
	def Scan(self, port):
		"""
		Scan for available servers on the given port number.

		Args:
			port (int): Port number

		Raises:
			TypeError: The port is not an int
			ValueError: The port number is invalid
		
		Returns:
			iter: Iterable collection of the available servers
		"""
		raise NotImplementedError
