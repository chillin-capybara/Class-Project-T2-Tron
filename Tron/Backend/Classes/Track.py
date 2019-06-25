from ..Core.Vect2D import Vect2D

class Track(object):
	def addEmelement(self, start: Vect2D, end: Vect2D):
		raise NotImplementedError
	
	def getLine(self) -> list:
		raise NotImplementedError

class LightTrack(Track):
	def __init__(self):
		self.__elements = [] # Array of tuples

	def addElement(self, start: Vect2D, end: Vect2D):
		
		if type(start) is not Vect2D:
			raise TypeError
		
		if type(end) is not Vect2D:
			raise TypeError
		
		self.__elements.append((start, end))

	def __generate_line(self):
		for element in self.__elements:
			start: Vect2D = element[0]
			end: Vect2D = element[1]
			yield(start)
		yield(end)

	def getLine(self) -> list:
		return list(self.__generate_line())