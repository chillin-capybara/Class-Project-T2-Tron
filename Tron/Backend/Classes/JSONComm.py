from CommProt import CommProt
from Game import Game
from Player import Player
from Tron.Backend.Core.Vect2D import Vect2D
from Tron.Backend.Core.core_functions import get_timestamp
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
	
	def bytes_to_dict(self, input: bytes) -> dict:
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
		if type(input) is not bytes:
			raise TypeError

		try:
			return json.loads(input, encoding="UTF-8")
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
			'message': msg
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
			player_dict = {'x':pos.x, 'y':pos.y, 'vx': vel.x, 'vy':vel.y}
			array.append(player_dict)
		
		return array

	
	def ingame(self, game: Game) -> bytes:
		"""
		Get a byte coded in-game packet from the server

		Args:
			game (Game): Current running game in the server
		Returns:
			bytes
		"""
		players_dict = self.__players_dict(game.getPlayers())

		mydict = {
			'type': 'ingame',
			'players': players_dict,
			'timestamp' : get_timestamp()
			}
		# TODO: (Marcell) Add arena stuff
		return self.dict_to_jsonbytes(mydict)
	
	def client_ready(self, player: Player) -> bytes:
		"""
		Get a byte coded client ready message

		Args:
			player: Player	Player Object of the Client
		Returns:
			bytes
		"""

		if type(player) is not Player:
			raise TypeError
		
		msgdict = {
			'type': 'client_ready',
			'playername' : player.getName(),
			'color': player.getColor(),
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
	
	def process_response(self):
		pass