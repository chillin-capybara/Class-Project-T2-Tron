from .CommProt import CommProt
from .Player import Player

def bytemsg(func):
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

	@bytemsg
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