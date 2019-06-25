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
			'MATCH_JOINED' : self.__process_client_ready_ack
			}
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
			return splitted[0], splitted[1][:-1] # Strip the last 'x00'
		except Exception as e:
			raise MessageError(str(e)) # Failed to convert into message and params

	def __color_to_rgb(self, color: int):
		"""
		Convert color to an RGB Value
		Args:
			color (int): Player color
		"""
		r: int = (color * 25) % 255
		g: int = (color * 25) % 255
		b: int = (color * 25) % 255

		return r,g,b

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
		r,g,b = self.__color_to_rgb(player.getColor())

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
			# TODO Color handling has to be changed

			player = HumanPlayer()
			player.setName(playername)
			player.setColor(int(r/25))

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