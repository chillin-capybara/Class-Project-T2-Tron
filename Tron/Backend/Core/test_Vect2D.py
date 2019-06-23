import unittest
import math
from Vect2D import Vect2D

class TestVect2D(unittest.TestCase):
	"""
	Test the Vect2D class functionality
	"""
	def test_setters(self):
		"""Test exceptions for false typing"""
		t = Vect2D(0,0)

		with self.assertRaises(TypeError):
			t.x = True

		with self.assertRaises(TypeError):
			t.x = 5j

		with self.assertRaises(TypeError):
			t.x = "Hello"
		
		with self.assertRaises(TypeError):
			t.y = True

		with self.assertRaises(TypeError):
			t.y = "Hello"

		with self.assertRaises(TypeError):
			t.y = 5j
		
		# Check the constructor for validation
		with self.assertRaises(TypeError):
			t = Vect2D("Hello", "Bello")


	def test_length(self):
		t = Vect2D(1,1)
		self.assertAlmostEqual(t.length(), math.sqrt(2))
		 
		