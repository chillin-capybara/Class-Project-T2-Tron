from .Player import Player
from .Track import Track, LightTrack
# @Marcel, Artem, ich musste einen Punkt davor setzen um auf den Ordner zugreifen zu können
# todo: Implement the Human player according to the UML

class HumanPlayer(Player):
	__track = None

	def __init__(self):
		self.__track = LightTrack()

	def getTrack(self):
		return self.__track
