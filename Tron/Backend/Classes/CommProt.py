class CommProt:
	"""
	Client-Server communikation protocol interface
	"""
	# Message types
	CLIENT_READY     = 0
	CLIENT_READY_ACK = 1
	CLIENT_ERROR     = 2
	SERVER_ERROR     = 3
	COUNTDOWN        = 4
	CLIENT_INGAME    = 5
	INGAME           = 6
	PAUSE_REQUEST    = 7
	CONTINUE_GAME    = 8
	EXIT_GAME        = 9
	REVENGE          = 10
	REVENGE_ACK      = 11


	def client_ready(self, player):
		"""
		Get a byte coded client ready message

		Args:
			player: Player	Player Object of the Client

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def client_ready_ack(self, player_id: int) -> bytes:
		"""
		Get a byte coded ack message for a client ready request

		Args:
			player_id (int): Index of the player on the server
		Return:
			bytes
		"""
		raise NotImplementedError

	def server_ready(self, game):
		"""
		Get a byte coded server ready message

		Args:
			game: Game	Game object of the current game
							running on the server
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	
	def server_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg: str	Error description (message)
		
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def client_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg: str	Error description (message)
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def client_start(self):
		"""
		Get a byte coded client start message

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def countdown(self, seconds):
		"""
		Get a byte coded countdown message (server-side)

		Returns:
			bytes
		Raises:
			TypeError: seconds is not an integer
			ValueError: seconds is smaller than 1
		"""
		raise NotImplementedError
	
	def ingame(self, game):
		"""
		Get a byte coded in-game message for continous synchronization
			between client and server
		Args:
			game: Game	Game object of the current game running on the
							server
		Return:
			bytes
		"""
		raise NotImplementedError
	
	def client_ingame(self, player):
		"""
		TODO
		"""
		raise NotImplementedError

	def pause(self):
		"""
		Get a byte coded pause request

		Returns:
			bytes
		"""
		raise NotImplementedError

	def continue_game(self, seconds):
		"""
		Get a byte coded continue request

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def ack_pause(self):
		"""
		Get a byte response for acknowledging a pause

		Returns:
			bytes
		"""
		raise NotImplementedError

	def ack_continue(self):
		"""
		Get a byte response for acknowledging a continue_game action

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def exit_game(self):
		"""
		Get a byte request for exiting a running game
		
		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def end_game(self):
		"""
		Get a byte request for ending a running game

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def revenge(self):
		"""
		Get a byte request for requesting a revenge

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def revenge_ack(self):
		"""
		Get a byte response for accepting a revenge

		Returns:
			bytes
		"""
		raise NotImplementedError
	
	def string_to_bytes(self, string):
		"""
		Convert a string to bytes considering the choosen encoding

		Args:
			string (str): String to convert
		
		Retruns:
			bytes: Converted string
		
		Raises:
			TypeError: string is not a str
		"""
		raise NotImplementedError

	def dict_to_jsonbytes(self, dict):
		"""
		TODO: DOCSTIRNG
		"""
		raise NotImplementedError

