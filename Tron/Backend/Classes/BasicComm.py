from .CommProt import CommProt
from .Player import Player
from .HumanPlayer import HumanPlayer
from ..Core.Exceptions import MessageError
from ..Core.globals import *
from typing import Tuple
import logging

# Import the matrix splitting functionalities
from ..Core.matrix import matrix_split, matrix_to_string, string_to_matrix
from ..Core.matrix_splitter import MatrixSplitter

def c2b(func):
	"""
	Decorate a function to return byte data, converted to byte instead of string
	Args:
		func (callable): Funciton to decorate
	Returns:
		callable
	"""
	def wrapper(*args, **kwargs):
		res = func(*args, **kwargs)
		return (bytes(res, "UTF-8") + b'\x00') # Terminate with 0 byte
	return wrapper

def list_to_strlist(input_list: list) -> str:
	"""
	Converts a list object into a comma separated string list
	
	Args:
		input_list (list): List object to convert
	
	Returns:
		str: Comma separated string
	"""
	return str(input_list).strip('[]\'').replace("'", "").replace(" ", "")
	
def player_tostr(player_id: int, player: Player) -> str:
	"""
	Converts the player to a string, by it's ID and color
	
	Args:
		player (Player): Player object to convert
	
	Returns:
		str: player_id,r,g,b
	"""
	r: int = player.getColor()[0]
	g: int = player.getColor()[1]
	b: int = player.getColor()[2]

	return "%s,%d,%d,%d" % (player_id, r, g, b)

def str_toplayer(str_list: list) -> (int, Player):
	"""
	Converts a list of string to a player
	
	Args:
		str_list (list): List of strings (player_id, r, g, b)
	Returns:
		int: Player ID
		Player: New Player object of RGB
	"""
	pid = int(str_list[0])
	r = int(str_list[1])
	g = int(str_list[2])
	b = int(str_list[3])
	player = HumanPlayer()
	player.setColor((r,g,b))

	return pid, player


class BasicComm(CommProt):
	"""
	Basic communication protocol for the Tron game.
	"""

	POLICY = None

	def __init__(self):
		self.POLICY = {
			'JOIN_MATCH'               : self.__process_join_match,
			'MATCH_JOINED'             : self.__process_match_joined,
			'ERR_CMD_NOT_UNDERSTOOD'   : self.__process_error_incorrect_cmd,
			'ERR_FAILED_TO_CREATE'     : self.__process_failed_to_create,
			'ERR_FAILED_TO_JOIN'       : self.__process_failed_to_join,
			'ERR_GAME_NOT_EXIST'       : self.__process_game_not_exists,
			'DISCONNECTING_YOU'        : self.__process_disconnecting_client,
			'LEAVING_MATCH'            : self.__process_leaving_match,
			'GAME_ENDED'               : self.__process_game_ended,
			'DISCOVER_LOBBY'           : self.__process_discover_lobby,
			'LOBBY'                    : self.__process_lobby,
			'LIST_GAMES'               : self.__process_list_games,
			'AVAILABLE_GAMES'           : self.__process_available_games,
			'HELLO'                    : self.__process_hello,
			'WELCOME'                  : self.__process_welcome,
			'CREATE_MATCH'             : self.__process_create_match,
			'MATCH_CREATED'            : self.__process_match_created,
			'LIST_MATCHES'             : self.__process_list_matches,
			'GAMES'                    : self.__process_games,
			'MATCH'                    : self.__process_match,
			'MATCH_STARTED'            : self.__process_match_started,
			'MATCH_FEATURES'           : self.__process_match_features,
			'UPDATE_FIELD'             : self.__process_update_field,
			'NEW_DIRECTION'            : self.__process_new_direction
			}
		
		# Initialize the events, and the abstract class
		super().__init__()

	def decode_message(self, msg: bytes) -> (str, str):
		"""
		Decode a received message and get the command and the parameters
		Args:
			msg (bytes): Received message
		Returns:
			str: Command
			str: Parameters
		"""
		try:
			decoded = msg.decode("UTF-8")
			splitted = decoded.split(' ', 1) # Split it into 2 parts
			if(len(splitted) == 1):
				return splitted[0][:-1], None
			else:
				return splitted[0], splitted[1][:-1] # Strip the last 'x00'
		except Exception as e:
			raise e
			raise MessageError(str(e)) # Failed to convert into message and params

	@c2b
	def join_match(self, match:str, player: Player):
		"""
		Join the match using the client_ready function
		Args:
			match (str) : Name of the match to join
			player (Player): Current Player
		NOTE
			JOIN_MATCH [match] [color]
		"""
		r,g,b = player.getColor()

		return "JOIN_MATCH %s %d,%d,%d" % (match, r, g, b)

	@c2b
	def match_joined(self, player_id: int):
		"""
		Acknowledge by server that the player is accepted on the match
		Args:
			player_id (int): player identifier on the server
		Returns:
			str: Acknowledgement message
		"""
		if type(player_id) is not int:
			raise TypeError

		return "MATCH_JOINED %d" % player_id
	
	@c2b
	def error_incorrect_cmd(self):
		"""
		Get a server error message, when a client's command is not understood
		Return:
			str
		"""
		return "ERR_CMD_NOT_UNDERSTOOD"
	
	@c2b
	def failed_to_create(self, reason: str) -> str:
		"""
		Get a failed to create message containing a reason.
		Args:
			reason (str): Reason of the errror
		Returns:
			str
		"""
		if type(reason) is not str:
			raise TypeError

		if reason is not "":
			return "ERR_FAILED_TO_CREATE %s" % reason
		else:
			raise ValueError
	
	@c2b
	def failed_to_join(self, reason: str) -> str:
		"""
		Get a failed to join message containing the reason.
		Args:
			reason (str): Resaon of the error
		Returns:
			str
		Raises:
			TypeError: Invalid argument types
			ValueError: reason is empty
		"""
		if type(reason) is not str:
			raise TypeError

		if reason is not "":
			return "ERR_FAILED_TO_JOIN %s" % reason
		else:
			raise ValueError
	
	@c2b
	def game_not_exists(self, name: str) -> str:
		"""
		Get a game not exists message from the server with the name of the game
		Args:
			name (str): Name of the game
		Returns:
			str
		Raises:
			TypeError:  Invalid argument types
			ValueError: Invalid name
		"""
		if type(name) is not str:
			raise TypeError
		
		if name is "":
			raise ValueError
		
		return "ERR_GAME_NOT_EXIST %s" % name
	
	@c2b
	def disconnect_client(self, reason: str) -> str:
		"""
		Get a disconnect client message with the reason of disconnect
		Args:
			reason (str): Reason of the disconnect
		Returns:
			str
		Raises:
			TypeError:  Invalid argument types
			ValueError: Invalid reason
		"""
		if type(reason) is not str:
			raise TypeError

		if reason is not "":
			return "DISCONNECTING_YOU %s" % reason
		else:
			raise ValueError
	
	@c2b
	def leaving_match(self, reason: str) -> str:
		"""
		Get a leaving match message with reason to be sent from the client.
		Args:
			reason (str): Reason of the leave
		Return:
			str
		Raises:
			TypeError:  Invalid argument types
			ValueError: Invalid reason
		"""
		if type(reason) is not str:
			raise TypeError

		if reason is not "":
			return "LEAVING_MATCH %s" % reason
		else:
			raise ValueError
	@c2b
	def game_ended(self, reason: str):
		"""
		Get a game ended message with reason
		Args:
			reason (str): Reason of the game end
		Return:
			str
		Raises:
			TypeError:  Invalid Argument types
			ValueError: Invalid reason
		"""
		if type(reason) is not str:
			raise TypeError

		if reason is not "":
			return "GAME_ENDED %s" % reason
		else:
			raise ValueError
	@c2b
	def discover_lobby(self) -> str:
		"""
		Get a discover lobby broadcast command from the client.
		Return:
			str: DISCOVER_LOBBY
		"""
		return "DISCOVER_LOBBY"

	@c2b
	def lobby(self, port: int) -> str:
		"""
		Get a lobby discovery answer message with the port of the lobby.
		Args:
			port (int): Port of the lobby (only accepts valid ports of the protocol)
		Returns:
			str: LOBBY [port]
		Raises:
			TypeError:  Invalid argument type
			ValueError: Invalid port number
		"""
		if type(port) is not int:
			raise TypeError
		
		if port in LOBBY_PORT_RANGE:
			return "LOBBY %d" % port
		else:
			raise ValueError
	
	@c2b
	def list_games(self):
		"""
		Get a list games command message
		Returns:
			str: LIST_GAMES
		"""
		return "LIST_GAMES"
	
	@c2b
	def available_games(self, games: list):
		"""
		Get a list of available games. (Only Tron)
		Return:
			AVAILABLE_GAMES Tron, ...
		"""
		return "AVAILABLE_GAMES %s" % list_to_strlist(games)

	@c2b
	def hello(self, player: Player, features: list) -> str:
		"""
		Get a hello message to the server
		Args:
			player (Player): Current player on the client
			features (list): List of features
		Returns:
			str: HELLO [name] [features]
		"""
		str_list = str(features).strip('[]\'').replace("'", "").replace(" ", "") # Remove the format characters
		return "HELLO %s %s" %(player.getName(), str_list)

	@c2b
	def welcome(self, features: list) -> str:
		"""
		Get a welcome message from the server
		Args:
			features (list): List of server features
		Returns:
			str: WELCOME [features]
		"""
		str_list = str(features).strip('[]\'').replace("'", "").replace(" ", "") # Remove the format characters
		return "WELCOME %s" % str_list
	
	@c2b
	def create_match(self, game: str, name: str, features: list) -> str:
		"""Get a create match request message
		
		Arguments:
			game {str} -- Game type: Tron/Pong
			name {str} -- Name of the match to create
			features {list} -- Available features
		
		Returns:
			str -- Request message
		"""
		feature_list = list_to_strlist(features)
		return "CREATE_MATCH %s %s %s" % (game, name, feature_list)
	
	@c2b
	def match_created(self)-> str:
		"""
		Get a match created acknowledge message
		
		Returns:
			str: ACK message
		"""
		return "MATCH_CREATED"
	
	@c2b
	def list_matches(self, game: str)->str:
		"""
		List the available matches on the server.
		
		Args:
			game (str): Game type = Tron
		
		Returns:
			str: LIST_MATCHES Tron
		"""
		if type(game) is not str:
			raise TypeError
		
		if game == "":
			raise ValueError

		return "LIST_MATCHES %s" % game
	
	@c2b
	def games(self, game: str, list_games: list) -> str:
		"""
		Get a list of matches running on the server for the current game.
		
		Args:
			game (str): Game type = Tron
			list_games (list): List of available matches
		
		Returns:
			str: GAMES [game] [matches]
		"""
		str_list = list_to_strlist(list_games)
		return "GAMES %s %s" % (game, str_list)
	
	@c2b
	def match_features(self, name: str):
		"""
		Request for getting a list of match features on the server.
		
		Args:
			name (str): Name of the match, to list features
		"""
		if type(name) is not str:
			raise TypeError
		
		if name == "":
			raise ValueError

		return "MATCH_FEATURES %s" % name
	
	@c2b
	def match(self, game: str, name: str, features: list)-> str:
		"""
		Response for listing the features of a match running on the server.
		
		Args:
			game (str): Game type = Tron
			name (str): Name of the match
			features (list): List of features
		
		Returns:
			str: MATCH [game] [name] [features]
		"""
		str_list = list_to_strlist(features)
		return "MATCH %s %s %s" % (game, name, str_list)
	
	@c2b
	def match_started(self, port: int, player_ids: list, players: list) -> str:
		"""
		Get a match started response from the server
		
		Args:
			port (int): Port number of the match
			players (list): List of player objects on the match
		
		Returns:
			str: MATCH_STARTED [port] [playerid,r,g,b]
		"""
		full_list = []
		for i in range(0, len(player_ids)):
			strlist = player_tostr(player_ids[i], players[i])
			full_list.append(strlist)
		
		str_list = list_to_strlist(full_list)
		return "MATCH_STARTED %d %s" % (port, str_list)
	
	@c2b
	def update_field(self, key: str, matrix: list) -> str:
		"""
		Generate an UPDATE_FILED message
		
		Args:
			key (str): (i,j) index of the part matrix
			matrix (list): Partial (matrix) to send
		
		Returns:
			str: Message
		"""
		matrix_str = matrix_to_string(matrix)
		message = "UPDATE_FIELD %d,%d %s" % (key[0],key[1],matrix_str)
		return message
	
	@c2b
	def new_direction(self, player_id: int, direcion: tuple) -> str:
		"""
		Get a change direction message from the client
		
		Args:
			player_id (int): ID of the player who sends the packet
			direction (tuple): New direction as x,y
		
		Returns:
			str: Message strin
		"""
		return "NEW_DIRECTION %d %d,%d" % (player_id, direcion[0], direcion[1])

	def process_response(self, response: bytes):
		"""
		Process response messages received.
		Args:
			response (bytes): Received message as bytes
		"""
		try:
			cmd, params = self.decode_message(response)
			# Call the callback from policy
			if callable(self.POLICY[cmd]):
				return self.POLICY[cmd](params)
			else:
				raise MessageError("Policy cannot be called")
		except Exception as e:
			raise e

	def __process_join_match(self, params: str) -> (str, int, int, int):
		"""
		Process JOIN_MATCH requests
		Args:
			params (str): Parameters of the command
		"""
		try:
			spl1 = params.split(" ", 1)
			matchname = spl1[0]
			
			spl2 = spl1[1].split(",")
			r = int(spl2[0])
			g = int(spl2[1])
			b = int(spl2[2])

			player = HumanPlayer()
			player.setColor((r,g,b))

			# Trigger Event
			self.EJoinMatch(self, name=matchname, player=player)
			return self.CLIENT_READY, matchname, player
		except Exception as e:
			raise e
			raise MessageError("Error processing JOIN_MATCH")

	def __process_match_joined(self, params: str) -> (int, int):
		"""
		Process a MATCH_JOINED message and return the sent ID
		Args:
			params (str): Parameters of the command
		Returns:
			int: self.CLIENT_READY_ACK
			int: Received player_id
		"""
		try:
			player_id = int(params)

			# Trigger the event for processing
			self.EMatchJoined(self, player_id=player_id)

			# Return the data
			return self.CLIENT_READY_ACK, player_id
		except Exception as e:
			raise MessageError("Invalid MATCH_JOINED received. Reason: %s" % str(e))

	def __process_error_incorrect_cmd(self, params: None):
		"""
		Process an ERR_CMD_NOT_UNDERSTOOD command
		Args:
			params (None): ignored parameter
		Event:
			EServerError(self, msg="Command not understood!")
		Returns
			int: SERVER_ERROR
		"""
		self.EServerError(self, msg="Command not understood!")
		return self.SERVER_ERROR, "ERR_CMD_NOT_UNDERSTOOD"
	
	def __process_failed_to_create(self, params: str) -> (int, str):
		"""
		Process an ERR_FAILED_TO_CREATE message with reason
		Args:
			params (str): Reason of the error
		Returns:
			int: CommProt.SERVER_ERROR
			str: Error message
		Event calls:
			EServerError(self, msg)
		"""
		if type(params) is not str:
			raise TypeError
		
		message = "Failed to create match. Reason: %s" % params

		# Call the event
		self.EServerError(self, msg=message)

		# Return the values
		return self.SERVER_ERROR, message
	
	def __process_failed_to_join(self, params: str) -> (int, str):
		"""
		Process an ERR_FAILED_TO_JOIN message with reason
		Args:
			params (str): Reason of the error
		Returns:
			int: CommProt.SERVER_ERROR
			str: Error message
		Event calls:
			EServerError(self, msg)
		"""
		if type(params) is not str:
			raise TypeError
		
		message = "Failed to join the game. Reason: %s" % params

		# Call the event
		self.EServerError(self, msg=message)

		# Return the values
		return self.SERVER_ERROR, message
	
	def __process_game_not_exists(self, params: str) -> (int, str):
		"""
		Process a ERR_GAME_NOT_EXIST message with reason
		Args:
			params (str): Name of the game
		Returns:
			int: CommProt.SERVER_ERROR
			str: Error message
		Event calls:
			EServerError(self, msg)
		"""
		
		message = "The game you want to join does not exist: %s" % params

		# Call the event
		self.EServerError(self, msg=message)

		# Return the values
		return self.SERVER_ERROR, message
	
	def __process_disconnecting_client(self, params: str) -> (int, str):
		"""
		Process a DISCONNECTING_YOU message with reason
		Args:
			params (str): Reason
		Returns:
			int: CommProt.SERVER_ERROR
			str: Error message
		Event calls:
			EServerError(self, msg)
		"""

		message = "You were disconnected by the server. Reason: %s" % params

		# Call the event
		self.EServerError(self, msg=message)

		# Return the values
		return self.SERVER_ERROR, message

	def __process_leaving_match(self, params: str) -> (int, str):
		"""
		Process a LEAVING_MATCH message with reasong
		Args:
			params (str): Reason of leave
		Returns:
			int: CommProt.EXIT_GAME
			str: Error message
		Event calls:
			EExitGame(self, msg)
		"""
		message = "Client is leaving the match. Reason: %s" % params

		# Call the event
		self.EExitGame(self, msg=message)

		# Return the values
		return self.EXIT_GAME, message
	
	def __process_game_ended(self, params: str) -> (int, str):
		"""
		Process a GAME_ENDED message with reason
		Args:
			params (str): Reason of end
		Returns:
			int: CommProt.GAME_ENDED
			str: Game ended message
		"""
		message = "Game ended! Reason: %s" % params

		# Call the event
		self.EGameEnded(self, msg=message)

		# Return the values
		return self.GAME_ENDED, message
	
	def __process_discover_lobby(self, params: None) -> (int, str):
		"""
		Process a DISCOVER_LOBBY request.
		Args:
			params (None): Ignored parameter -> for syntax
		Returns:
			int: CommProt.DISCOVER_LOBBY
			str: DISCOVER_LOBBY
		"""
		self.EDiscoverLobby(self)
		return self.DISCOVER_LOBBY, "DISCOVER_LOBBY"
	
	def __process_lobby(self, params: str) -> (int, int):
		"""
		Process a LOBBY message and return the port number
		Args:
			params (str): Port number
		Returns:
			int: CommProt.LOBBY
			int: Port of the lobby
		Raises:
			TypeError: Invalid port type
			ValueError Invalid port range
		"""
		try:
			port = int(params)
		except:
			raise TypeError("Port cannot be converted to integer")
		
		if port not in LOBBY_PORT_RANGE:
			raise ValueError("The port number is not in the configured range.")

		self.ELobby(self, port=port)
		return self.LOBBY, port
	
	def __process_list_games(self, params: None) -> (int, str):
		"""
		Process the message of list available games command.
		Args:
			params (str): Ignored argument
		Returns:
			int: CommProt.LIST_GAMES
			str: "LIST_GAMES"
		"""
		# Call the event
		self.EListGames(self)
		return self.LIST_GAMES, "LIST_GAMES"
	
	def __process_available_games(self, params: str) -> (int, list):
		"""
		Process the list of available games on a server
		Args:
			params (str): Comma separated list of games
		Returns:
			int:       CommProt.AVAILABLE_GAMES
			list[str]: available games
		"""
		try:
			games = params.split(',')
			self.EAvailableGames(self, games=games)
			return self.AVAILABLE_GAMES, games
		except Exception as e:
			raise MessageError("Invalid message parameters: %s" % str(e))
	
	def __process_hello(self, params: str) -> (int, str, list):
		"""
		Process a hello message received from the client.
		Args:
			params (str): playername, features
		Returns:
			int:  CommProt.HELLO
			str:  Name of the player
			list: List of client features
		"""
		try:
			spl = params.split(' ', 1)
			playername = spl[0]
			features: str = spl[1]
			list_features = features.split(',')

			# Call the event
			self.EHello(self, playername=playername, features=list_features)

			# Return the value
			return self.HELLO, playername, list_features
		except Exception as e:
			raise MessageError("Invalid message format: %s" % str(e))
	
	def __process_welcome(self, params: str) -> (int, list):
		"""
		Process a welcome message from the server.
		Args:
			params (str): Comma separated list of features
		Returns:
			int:  CommProt.WELCOME
			list: list of server features
		Raises:
			MessageError: Invalid message parameters
		"""
		try:
			list_features = params.split(',')

			# Call the events
			self.EWelcome(self, features=list_features)
			
			# Return the results
			return self.WELCOME, list_features
		except:
			MessageError("Invalid message syntax")
	
	def __process_create_match(self, params: str) -> Tuple[int, str, str, list]:
		"""
		Process a create match request
		
		Args:
			params (str): Parameters of the command
		
		Returns:
			Tuple[int, str, str, list]: (CommProt.CREATE_MATCH, game, name, features)
		"""
		try:
			spl = params.split(' ', 2)
			game = spl[0]
			name = spl[1]
			features = spl[2].split(',')

			# Make the event call
			self.ECreateMatch(self, game=game, name=name, features=features)

			# Return the value
			return self.CREATE_MATCH, game, name, features
		except Exception as e:
			raise MessageError("Invalid message syntax for create_match: %s" % str(e))
	
	def __process_match_created(self, params: None) -> Tuple[int, str]:
		"""
		Process a match created acknowledgement
		
		Args:
			params (None): Ignored args
		
		Returns:
			Tuple[int, str]: CommProt.MATCH_CREATED, "MATCH_CREATED"
		"""
		# Event call
		self.EMatchCreated(self)
		
		return self.MATCH_CREATED, "MATCH_CREATED"
	
	def __process_list_matches(self, params: str) -> Tuple[int, str]:
		"""
		Process a list matches command
		
		Args:
			params (str): Game Type : Tron
		
		Returns:
			Tuple[int, str]: CommProt.LIST_MATCHES, game_type
		"""
		self.EListMatches(self, game=params)

		return self.LIST_MATCHES, params
	
	def __process_games(self, params: str) -> Tuple[int, str, list]:
		"""
		Process a GAMES response
		
		Args:
			params (str): [game] [matches]
		
		Returns:
			Tuple[int, str, list]: (CommProt.GAMES, game, list)
		"""
		try:
			game, str_matches = params.split(' ', 1)
			matches = str_matches.split(',')

			if matches == ['']: # Replace the array with empty string to an empty array
				matches = []

			self.EGames.reset_called()
			self.EGames(self, game=game, matches=matches)

			return self.GAMES, game, matches
		except Exception as e:
			if not self.EGames.was_called():
				self.EGames(self, game=game, matches=matches) # Call the event with empty list of games
			else:
				raise MessageError("Syntax error in GAMES [...]: %s" % str(e))

	def __process_match_features(self, params: str) -> Tuple[int, list]:
		"""
		Process a match_features response from the server
		
		Args:
			params (str): List of match features
		
		Returns:
			Tuple[int, list]: CommProt.MATCH_FEATURES, features
		"""
		try:
			name = params
			
			self.EMatchFeatures(self, name=name)
			return self.MATCH_FEATURES, name
		except:
			raise MessageError("Invalid message syntax at MATCH_FEATURES")
	
	def __process_match(self, params: str) -> Tuple[int, str, str, list]:
		"""
		Process the match response from the server
		
		Args:
			params (str): Response parameters
		
		Returns:
			Tuple[int, str, str, list]: CommProt.MATCH, game, name, features
		"""
		try:
			game, name, str_features = params.split(' ', 2)
			features = str_features.split(',')

			self.EMatch(self, game=game, name=name, features=features)
			return self.MATCH, game, name, features
		except:
			raise MessageError("Invalid syntax for: MATCH ...")
	
	def __process_match_started(self, params: str) -> Tuple[int, int, tuple]:
		"""
		Process a match started message from the server
		
		Args:
			params (str): message parameters
		
		Returns:
			Tuple[int, tuple]: CommProt.MATCH_STARTED, port, tuple
		"""
		try:
			str_port, str_list = params.split(' ', 1)
			mylist = str_list.split(',')
			pre = []
			if len(mylist) % 4 == 0:
				for i in range(0, int(len(mylist) / 4)):
					pre.append((int(mylist[4*i]), int(mylist[4*i+1]), int(mylist[4*i+2]), int(mylist[4*i+3])))

				self.EMatchStarted(self, port=int(str_port), players=pre)
				return self.MATCH_STARTED, int(str_port), pre
			else:
				raise MessageError("Invalid syntax for MATCH_STARTED")
		except:
			MessageError("Invalid Syntax for MATCH_STARTED!")
	
	def __process_update_field(self, params:str) -> Tuple[int, tuple, list]:
		"""
		Process an update field request
		
		Args:
			params (str): Partial index and string representation of the matrix
		
		Returns:
			Tuple[int, tuple, list]: Comm.UPDATE_FIELD, (i,j), matrix
		"""
		keys, str_matrix = params.split(" ", 1)
		i,j = keys.split(",")
		i = int(i)
		j = int(j)

		matrix = string_to_matrix(str_matrix)

		# Call the event
		self.EUpdateField(self, key=(i,j), matrix=matrix)

		return self.UPDATE_FIELD, (i,j), matrix
	
	def __process_new_direction(self, params: str):
		"""
		Process a new direction request from the client on the server
		
		Args:
			params (str): Player id x,y
		"""
		pid, sdir = params.split(" ", 1)
		x,y = sdir.split(',', 1)

		pid = int(pid)
		x = int(x)
		y = int(y)

		# Call the event
		self.ENewDirection(self, player_id = pid, direction=(x,y))

		return self.NEW_DIRECTION, pid, (x,y)