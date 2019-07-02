from ..Core.Event import Event

class CommProt:
	"""
	Client-Server communikation protocol interface
	"""
	# Message types
	CLIENT_READY           = 0
	CLIENT_READY_ACK       = 1
	CLIENT_ERROR           = 2
	SERVER_ERROR           = 3
	COUNTDOWN              = 4
	CLIENT_INGAME          = 5
	INGAME                 = 6
	PAUSE_REQUEST          = 7
	CONTINUE_GAME          = 8
	EXIT_GAME              = 9
	REVENGE                = 10
	REVENGE_ACK            = 11
	SERVER_NOTIFICAITON    = 12
	CLIENT_CHAT            = 13
	LEAVING_GAME           = 14
	GAME_ENDED             = 15
	DISCOVER_LOBBY         = 16
	LOBBY                  = 17
	LIST_GAMES             = 18
	AVAILABLE_GAMES        = 19
	HELLO                  = 20
	WELCOME                = 21
	CREATE_MATCH           = 22
	MATCH_CREATED          = 23
	LIST_MATCHES           = 24
	GAMES                  = 25
	MATCH_FEATURES         = 26
	MATCH                  = 27
	MATCH_STARTED          = 28
	UPDATE_FIELD           = 29
	NEW_DIRECTION          = 30


	# Create events for processing responsees
	EClientError           : Event    = None # (sender=, msg=)
	EServerError           : Event    = None # (sender=, msg=)
	EJoinMatch             : Event    = None # (sender=, name=, player=)
	EMatchJoined           : Event    = None # (sender=, player_id=)
	EServerReady           : Event    = None # (sender=)
	ECountdown             : Event    = None
	EIngame                : Event    = None
	EClientIngame          : Event    = None # (sender=, player=)
	EPause                 : Event    = None # (sender=)
	ERevenge               : Event    = None # (sender=)
	ERevengeAck            : Event    = None # (sender=)
	EExitGame              : Event    = None # (sender=)
	EServerNotification    : Event    = None
	EClientChat            : Event    = None
	EGameEnded             : Event    = None # (sender=, msg=)
	EDiscoverLobby         : Event    = None
	ELobby                 : Event    = None # (sender=, port=)
	EListGames             : Event    = None
	EAvailableGames        : Event    = None
	EHello                 : Event    = None
	EWelcome               : Event    = None
	ECreateMatch           : Event    = None
	EMatchCreated          : Event    = None
	EListMatches           : Event    = None
	EGames                 : Event    = None
	EMatchFeatures         : Event    = None
	EMatch                 : Event    = None
	EMatchStarted          : Event    = None
	EUpdateField           : Event    = None
	ENewDirection          : Event    = None


	def __init__(self):
		"""
		Initialize the Events for the Communication Protocol Interface
		NOTE
			Calls Event Creators and lets event handlers subscribe to the specific events
		"""
		self.EClientError           = Event('msg') # (sender=, msg=)
		self.EServerError           = Event('msg') # (sender=, msg=)
		self.EJoinMatch             = Event('name', 'player') # (sender=, name=, player=)
		self.EMatchJoined           = Event('player_id') # (sender=, player_id=)
		self.EServerReady           = Event() # (sender=)
		self.ECountdown             = Event('seconds')
		self.EIngame                = Event('players')
		self.EClientIngame          = Event('player') # (sender=, player=)
		self.EPause                 = Event() # (sender=)
		self.ERevenge               = Event() # (sender=)
		self.ERevengeAck            = Event() # (sender=)
		self.EExitGame              = Event() # (sender=)
		self.EServerNotification    = Event('msg') # (sender=, msg=
		self.EClientChat            = Event('player_id', 'msg') # (sender=, player_id=, msg=)
		self.EGameEnded             = Event('msg') # (sender=, msg=)
		self.EDiscoverLobby         = Event() # (sender=)
		self.ELobby                 = Event('port')
		self.EListGames             = Event()
		self.EAvailableGames        = Event('games') # (sender=, games=)
		self.EHello                 = Event('playername', 'features')
		self.EWelcome               = Event('features')
		self.ECreateMatch           = Event('game', 'name', 'features')
		self.EMatchCreated          = Event()
		self.EListMatches           = Event('game')
		self.EGames                 = Event('game', 'matches')
		self.EMatchFeatures         = Event('name')
		self.EMatch                 = Event('game', 'name', 'features')
		self.EMatchStarted          = Event('port', 'players') # the list is formatted as (id, r, g, b)
		self.EUpdateField           = Event('key', 'matrix')
		self.ENewDirection          = Event('player_id', 'direction')

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
	
	def server_notification(self, msg: str):
		"""
		Get a byte coded message for sendin notifications from the server
		Args:
			msg (str): Message to send
		Returns:
			byte
		"""
		raise NotImplementedError
	
	def client_chat(self, player_id: int, msg: str) -> bytes:
		"""
		TODO: DOKU
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

