from CommProt import CommProt
from Game import Game
from Player import Player
from ..Core.Vect2D import Vect2D
from ..Core.core_functions import get_timestamp
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
	
	def dict_to_jsonbytes(self, dict):
		"""
		Convert a Dictionary to JSON String, then to encoded byte array

		Args:
			dict (dict): Dictionary
		Returns:
			bytes: Encoded dictionary
		"""
		return self.string_to_bytes(json.dumps(dict))


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
		msgdict = {'type': 'server_error', 'message': msg}
		return self.dict_to_jsonbytes(msgdict)
	
	def client_error(self, msg):
		"""
		Get a byte coded client error message

		Args:
			msg (str): Error description (message)
		Returns:
			bytes
		NOTE:
			{"type":"client_error", "message": "this is the message"}
		"""

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
		"""

		msgdict = {
			'type': 'client_ready_ack',
			'player_id': player_id,
			'timestamp': get_timestamp()
		}
		return self.dict_to_jsonbytes(msgdict)