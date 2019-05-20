import unittest
import math
from Vect2D import Vect2D

class TestVect2D(unittest.TestCase):
	"""
	Test the Vect2D class functionality
	"""
	def test_coordinates(self):
		with self.assertRaises(TypeError):
			t = Vect2D(1j, True)


	def test_length(self):
		t = Vect2D(1,1)
		self.assertAlmostEqual(t.length(), math.sqrt(2))
	
	def test_angle(self):
		# Angle of the x unit
		t = Vect2D(1,0)
		self.assertAlmostEqual(t.angle(), 0)

		# Angle of the y unit
		t = Vect2D(0,1)
		self.assertAlmostEqual(t.angle(), math.pi/2)

		# 45deg
		t = Vect2D(1,1)
		self.assertAlmostEqual(t.angle(), math.pi/4)

		#135deg
		# TODO Add more tests
		 
		