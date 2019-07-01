from .CommProt import CommProt
from .Player import Player
from .Factory import Factory
from .Arena import Arena
from ..Core.Vect2D import Vect2D
from ..Core.core_functions import get_timestamp
from ..Core.Exceptions import MessageError
import json

class JSONComm(CommProt):
	"""
	Communication protocoll implementation using JSON format
	"""

	def string_to_bytes(self, string):
		"""
		Convert a string to an encoded byte array

		Args:
			string (str): String to convert
		Returns:
			bytes: Encoded string
		"""
		if type(string) == str:
			return bytes(string, "UTF-8")
		else:
			raise TypeError
		
	def bytes_to_string(self, input: bytes) -> str:
		"""
		Converts the input bytes array into a decoded string

		Args:
			input (bytes): Bytes input
		Returns:
			str: decoded string
		Raises:
			TypeError: input is not bytes
		"""
		if type(input) is not bytes:
			raise TypeError
		
		return input.decode("UTF-8")
	
	def dict_to_jsonbytes(self, dict):
		"""
		Convert a Dictionary to JSON String, then to encoded byte array

		Args:
			dict (dict): Dictionary
		Returns:
			bytes: Encoded dictionary
		"""
		return self.string_to_bytes(json.dumps(dict))
	
	def bytes_to_dict(self, data: bytes) -> dict:
		"""
		Converts the input bytes array into a dictionary
		Args:
			input (bytes): Input bytes
		Returns:
			dict: Converted dictionary
		Raises:
			TypeError
			ValueError
		"""
		if type(data) is not bytes:
			raise TypeError

		try:
			decoded = data.decode("UTF-8")
			return json.loads(decoded)
		except json.JSONDecodeError: # Invalid JSON String
			raise MessageError()
		except Exception as e:
			raise ValueError(str(e))


	def server_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg (str):	Error description (message)
		
		Returns:
			bytes
		NOTE:
			{"type":"server_error", "message": "this is the message"}
		"""

		if type(msg) is not str:
			raise TypeError

		msgdict = {'type': 'server_error', 'message': msg}
		return self.dict_to_jsonbytes(msgdict)
	
	def client_error(self, msg: str):
		"""
		Get a byte coded client error message

		Args:
			msg (str): Error description (message)
		Returns:
			bytes
		NOTE:
			{"type":"client_error", "message": "this is the message"}
		"""
		if type(msg) is not str:
			raise TypeError
		
		msgdict = {
			'type': 'client_error',
			'message': msg,
			'timestamp' : get_timestamp()
		}
		return self.dict_to_jsonbytes(msgdict)
	
	def __players_dict(self, players: list) -> list:
		"""
		Convert an array of players to a dictionary for in-game packets

		Args:
			players: list of players in-game
		Returns:
			list of dictonaries containing player position and velocity
		"""

		array: list = [] # List to collect the player dicts

		for player in players:
			player: Player = player # Static typing fix

			# Get the current data of the player
			pos: Vect2D = player.getPosition()
			vel: Vect2D = player.getVelocity()

			# Create a dict
			player_dict = {
				'playername': player.getName(), 
				'color_r': player.getColor()[0],
				'color_g': player.getColor()[1],
				'color_b': player.getColor()[2],
				'x':pos.x,
				'y':pos.y,
				'vx': vel.x,
				'vy':vel.y}
			array.append(player_dict)
		
		return array

	
	def ingame(self, players: list, arena: Arena) -> bytes:
		"""
		Get a byte coded in-game packet from the server

		Args:
			game (Game): Current running game in the server
		Returns:
			bytes
		TODO
			Add Arena object too
		"""
		players_dict = self.__players_dict(players)

		mydict = {
			'type': 'ingame',
			'players': players_dict,
			'timestamp' : get_timestamp()
			}
		# TODO: (Marcell) Add arena stuff
		return self.dict_to_jsonbytes(mydict)
	
	def client_ingame(self, player: Player) -> bytes:
		"""
		Get a byte coded in-game message from a single client
		It shall only contain the client player's data
		Args:
			player (Player): Current player [ME]
		Return:
			bytes: message
		Raises:
			TypeError: Argument types ar not valid
		"""
		
		if not Factory.isPlayer(player):
			raise TypeError
		
		msgdict = {
			'type': 'client_ingame',
			'playername': player.getName(),
			'color_r': player.getColor()[0],
			'color_g': player.getColor()[1],
			'color_b': player.getColor()[2],
			'x': player.getPosition().x,
			'y': player.getPosition().y,
			'vx': player.getVelocity().x,
			'vy': player.getVelocity().y,
			'timestamp': get_timestamp()
		}

		return self.dict_to_jsonbytes(msgdict)
	
	def client_ready(self, player: Player) -> bytes:
		"""
		Get a byte coded client ready message

		Args:
			player: Player	Player Object of the Client
		Returns:
			bytes
		"""

		if not Factory.isPlayer(player):
			raise TypeError
		
		msgdict = {
			'type': 'client_ready',
			'playername' : player.getName(),
			'color_r': player.getColor()[0],
			'color_g': player.getColor()[1],
			'color_b': player.getColor()[2],
			'timestamp': get_timestamp()
		}

		return self.dict_to_jsonbytes(msgdict)
	
	def client_ready_ack(self, player_id: int) -> bytes:
		"""
		Get a byte coded ack message for a client ready request

		Args:
			player_id (int): Index of the player on the server
		Return:
			bytes
		Raises:
			TypeError: player_id is not integer
		"""
		if type(player_id) is not int:
			raise TypeError

		msgdict = {
			'type': 'client_ready_ack',
			'player_id': player_id,
			'timestamp': get_timestamp()
		}
		return self.dict_to_jsonbytes(msgdict)
	
	def countdown(self, seconds: int):
		"""
		Get a byte coded countdown message (server-side)

		Returns:
			bytes
		Raises:
			TypeError: seconds is not an integer
			ValueError: seconds is smaller than 1
		"""
		# Type and range verification
		if type(seconds) is not int:
			raise TypeError
		
		if seconds < 1:
			raise ValueError
		
		# Generate bytes message
		msgdict = {
			'type': 'countdown',
			'seconds': seconds,
			'timestamp': get_timestamp()
		}

		return self.dict_to_jsonbytes(msgdict)
	
	def exit_game(self) -> bytes:
		"""
		Get a byte request for exiting a running game
		
		Returns:
			bytes
		"""
		msgdict = {
			'type': 'exit_game',
			'timestamp': get_timestamp()
		}

		return self.dict_to_jsonbytes(msgdict)
	
	def revenge(self) -> bytes:
		"""
		Get a byte request for requesting a revenge

		Returns:
			bytes
		"""
		msgdict = {
			'type': 'revenge',
			'timestamp': get_timestamp()
			}
		
		return self.dict_to_jsonbytes(msgdict)
	
	def revenge_ack(self) -> bytes:
		"""
		Get a byte message for a revenge ack

		Returns:
			bytes
		"""
		msgdict = {
			'type': 'revenge_ack',
			'timestamp': get_timestamp()
			}
		
		return self.dict_to_jsonbytes(msgdict)
	
	def server_notification(self, msg):
		"""
		Get a byte coded message for sending notifications from the server
		Args:
			msg (str): Message to send
		Returns:
			byte
		"""
		msgdict = {
			'type': 'server_notification',
			'message': msg,
			'timestamp': get_timestamp()
		}

		return self.dict_to_jsonbytes(msgdict)
	
	def client_chat(self, player_id: int, msg: str) -> bytes:
		"""
		Get a byte coded message for sending chat messages between clients
		Args:
			player_id (int): Identifier of the player on the server
			msg (str): Chat message
		Returns:
			byte
		"""
		msgdict = {
			'type': 'client_chat',
			'player_id': player_id,
			'message': msg,
			'timestamp': get_timestamp()
		}

		return self.dict_to_jsonbytes(msgdict)
	
	def process_response(self, response: bytes):
		"""
		Process incoming requests in JSONComm format, return type and result
		Args:
			response (bytes): Incoming response, received packet content
		Raises:
			ValueError: Invalid format
			TypeError: Response is not bytes
		"""

		#if type(response) is not bytes:
		#	raise TypeError

		try:
			# Decode the message
			decoded = self.bytes_to_dict(response)

			# Look for the message type
			if 'type' not in decoded.keys():
				raise ValueError("The received message is invalid")
			
			if decoded['type'] == "client_ready":
				obj = self.__process_client_ready(decoded)
				self.EClientReady(self, player=obj)
				return CommProt.CLIENT_READY, obj
			elif decoded['type'] == 'client_ready_ack':
				obj = self.__process_client_ready_ack(decoded)
				self.EClientReadyAck(self, player_id=obj) # Call the event with the player_id
				return CommProt.CLIENT_READY_ACK, obj
			elif decoded['type'] == 'client_error':
				obj = self.__process_error(decoded) # OBJECT STORE
				self.EClientError(self, msg=obj)    # CALL EVENT
				return CommProt.CLIENT_ERROR, obj   # RETURN VALUE
			elif decoded['type'] == 'server_error':
				obj = self.__process_error(decoded) # OBJECT STORE
				self.EServerError(self, msg=obj)    # CALL EVENT
				return CommProt.SERVER_ERROR, obj   # RETURN VALUE
			elif decoded['type'] == 'server_notification':
				obj = self.__process_server_notification(decoded)
				self.EServerNotification(self, msg=obj)
				return CommProt.SERVER_NOTIFICAITON, obj
			elif decoded['type'] == 'client_chat':
				pid, msg = self.__process_client_chat(decoded)
				self.EClientChat(self, player_id=pid, msg=msg)
				return CommProt.CLIENT_CHAT, pid, msg
			elif decoded['type'] == 'ingame':
				obj, obj2 = self.__process_ingame(decoded)
				self.EIngame(self, players=obj)    # EVENT CALL
				return CommProt.INGAME, obj, obj2
			elif decoded['type'] == 'client_ingame':
				obj = self.__process_client_ingame(decoded)
				self.EClientIngame(self, player=obj) # EVENT CALL
				return CommProt.CLIENT_INGAME, obj
			elif decoded['type'] == 'countdown':
				obj = self.__process_countdown(decoded)
				self.ECountdown(self, seconds=obj)
				return CommProt.COUNTDOWN, obj
			elif decoded['type'] == 'revenge':
				return CommProt.REVENGE, True
			elif decoded['type'] == 'revenge_ack':
				return CommProt.REVENGE_ACK, True
			elif decoded['type'] == 'exit_game':
				return CommProt.EXIT_GAME, True
			else:
				# Invalid message type: Type not exists
				raise ValueError("The message type is invalid!")
		except Exception as e:
			# Pass exception along
			raise e
		
	def __process_client_ready(self, msgdict: dict) -> Player:
		"""
		Converts a dictonary to a new Player object using the Factory
		Args:
			msgdict (dict): Message dictionary
		Raises:
			TypeError: Invalid argument types
			KeyError: Missing dictionary keys
		NOTE
			The type errors should be checked in the calling function.
		"""
		if 'playername' not in msgdict.keys():
			raise KeyError

		r = msgdict['color_r']
		g = msgdict['color_g']
		b = msgdict['color_b']

		# Factor the player by name and color
		newplayer: Player = Factory.Player(msgdict['playername'], (r,g,b))
		return newplayer
	
	def __process_client_ready_ack(self, msgdict: dict) -> int:
		"""
		Get the index of the current player based on a client ready_ack request
		Args:
			msgdict (dict): Message dictionary
		Raises:
			KeyError: Missing key / Wrong format
			TypeError: Invalid player_id type
		Return:	
			int: Index of the current player on the server
		"""
		# Check for id key
		if 'player_id' not in msgdict.keys():
			raise KeyError
		
		# Check item type
		if type(msgdict['player_id']) is not int:
			raise TypeError
		
		return msgdict['player_id']
	
	def __process_countdown(self, msgdict: dict) -> int:
		"""
		Get the countdown time for starting a countdown.
		Args:
			msgdict (dict): Message dictionary
		Raises:
			KeyError: Invalid message structure
			TypeError: Invalid message types
			ValueError: Invalid message value
		Return:
			int: seconds to countdown
		"""
		# Check for seconds
		if 'seconds' not in msgdict.keys():
			raise KeyError()
		
		if type(msgdict['seconds']) is not int:
			raise TypeError()

		seconds = msgdict['seconds']
		# Check if the countdown is positive
		if seconds < 1:
			raise ValueError("Negative countdown")
		
		return seconds
	
	def __process_error(self, msgdict: dict) -> str:
		"""
		Get the error message of a client error or server error
		NOTE
			Client and server error messages only differ in message type
			but not in structure
		Args:
			msgdict (dict): Message dictionary
		Raises:
			KeyError: Message key is not found
			TypeError: Message is not a string
		Returns:	
			str: Sent error message
		"""
		# Check for message key
		if 'message' not in msgdict.keys():
			raise KeyError
		
		# Check the message type
		if type(msgdict['message']) is not str:
			raise TypeError
		
		return msgdict['message']
	
	def __process_server_notification(self, msgdict: dict) -> str:
		"""
		Get the notification message from the server
		Args:
			msgdict (dict): Dict of the sent messages
		Returns:
			str: Received messsage
		"""
		# Check for message key
		if 'message' not in msgdict.keys():
			raise KeyError
		
		# Check the message type
		if type(msgdict['message']) is not str:
			raise TypeError
		
		return msgdict['message']
	
	def __process_client_chat(self, msgdict: dict) -> tuple:
		"""
		Process the client chat messages
		"""
		# Check for message key
		if 'message' not in msgdict.keys():
			raise KeyError
		
		# Check the message type
		if type(msgdict['message']) is not str:
			raise TypeError

		# Check for message key
		if 'player_id' not in msgdict.keys():
			raise KeyError
		
		# Check the message type
		if type(msgdict['player_id']) is not int:
			raise TypeError
		
		return msgdict['player_id'], msgdict['message']

	def __process_ingame(self, msgdict: dict):
		"""
		Process an ingame update of player and the arena
		Args:
			msgdict (dict): Dictionary of the received package
		Returns:
			list[Player]: List of players
			Arena:        Updated arena
		"""
		# Check for the players instance
		if 'players' not in msgdict.keys():
			raise KeyError
		
		if type(msgdict['players']) is not list:
			raise TypeError
		
		# List all players and fetch them to an array
		plarray = []

		for pldata in msgdict['players']:
			# Fetch data from the dict
			r = pldata['color_r']
			g = pldata['color_g']
			b = pldata['color_b']
			player = Factory.Player(pldata['playername'], (r,g,b))
			player.setVelocity(pldata['vx'], pldata['vy'])
			player.setPosition(pldata['x'], pldata['y'])

			# Add player to the results
			plarray.append(player)
		return plarray, None

	
	def __process_client_ingame(self, msgdict: dict) -> Player:
		"""
		Process a client in-game request.
		Args:
			msgdict (dict): Encoded messaage dictionary
		Returns:
			Player: Current player object
		"""
		# Check for message key
		if 'playername' not in msgdict.keys():
			raise KeyError

		# Check for message key
		if 'x' not in msgdict.keys():
			raise KeyError
		
		# Check for message key
		if 'y' not in msgdict.keys():
			raise KeyError
		
		# Check for message key
		if 'vx' not in msgdict.keys():
			raise KeyError
		
		# Check for message key
		if 'vy' not in msgdict.keys():
			raise KeyError
		r = msgdict['color_r']
		g = msgdict['color_g']
		b = msgdict['color_b']
		pl = Factory.Player(msgdict['playername'], (r,g,b))
		pl: Player()
		pl.setPosition(msgdict['x'], msgdict['y'])
		pl.setVelocity(msgdict['vx'], msgdict['vy'])

		return pl