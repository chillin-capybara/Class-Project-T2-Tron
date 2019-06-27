from .CommProt import CommProt
from .Player import Player
from .HumanPlayer import HumanPlayer
from ..Core.Exceptions import MessageError
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
			'JOIN_MATCH': self.__process_client_ready,
			'MATCH_JOINED' : self.__process_client_ready_ack,
			'ERR_CMD_NOT_UNDERSTOOD': self.__process_error_incorrect_cmd,
			'ERR_FAILED_TO_CREATE': self.__process_failed_to_create,
			'ERR_FAILED_TO_JOIN': self.__process_failed_to_join,
			'ERR_GAME_NOT_EXIST': self.__process_game_not_exists,
			'DISCONNECTING_YOU': self.__process_disconnecting_client,
			'LEAVING_MATCH': self.__process_leaving_match,
			'GAME_ENDED': self.__process_game_ended
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