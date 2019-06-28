from .CommProt import CommProt
from .Player import Player
from .HumanPlayer import HumanPlayer
from ..Core.Exceptions import MessageError
from ..Core.globals import *
import logging

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


class BasicComm(CommProt):
	"""
	Basic communication protocol for the Tron game.
	"""

	POLICY = None

	def __init__(self):
		self.POLICY = {
			'JOIN_MATCH'               : self.__process_client_ready,
			'MATCH_JOINED'             : self.__process_client_ready_ack,
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
			'AVAILABLE_GAME'           : self.__process_available_games,
			'HELLO'                    : self.__process_hello,
			'WELCOME'                  : self.__process_welcome
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
	def client_ready(self, player: Player):
		"""
		Join the match using the client_ready function
		Args:
			player (Player): Current Player
		NOTE
			JOIN_MATCH [player] [color]
		"""
		name = player.getName()
		r,g,b = player.getColor()

		return "JOIN_MATCH %s %d,%d,%d" % (name, r, g, b)

	@c2b
	def client_ready_ack(self, player_id: int):
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
	def available_games(self):
		"""
		Get a list of available games. (Only Tron)
		Return:
			AVAILABLE_GAMES Tron
		"""
		return "AVAILABLE_GAMES Tron"

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

	def __process_client_ready(self, params: str) -> (str, int, int, int):
		"""
		Process JOIN_MATCH requests
		Args:
			params (str): Parameters of the command
		TODO: NOT PLAYERNAME, GAME NAME
		"""
		try:
			spl1 = params.split(" ", 1)
			playername = spl1[0]
			
			spl2 = spl1[1].split(",")
			r = int(spl2[0])
			g = int(spl2[1])
			b = int(spl2[2])

			player = HumanPlayer()
			player.setName(playername)
			player.setColor((r,g,b))

			# Trigger Event
			self.EClientReady(self, player=player)
			return self.CLIENT_READY, player
		except Exception as e:
			raise e
			raise MessageError("Error processing JOIN_MATCH")

	def __process_client_ready_ack(self, params: str) -> (int, int):
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
			self.EClientReadyAck(self, player_id=player_id)

			# Return the data
			return self.CLIENT_READY_ACK, player_id
		except:
			raise MessageError("Invalid MATCH_JOINED received.")

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
			self.EAvailableGames(games=games)
			return self.AVAILABLE_GAMES, games
		except:
			raise MessageError("Invalid message parameters.")
	
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