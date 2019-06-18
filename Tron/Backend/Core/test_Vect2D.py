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
		"""
		check the vector lenght  
		"""
		t = Vect2D(1,1)
		self.assertAlmostEqual(t.length(), math.sqrt(2))
		 
	def test_addition(self):
		"""
		check the result after vector addition
		test is done with integer values
  		"""
		t = Vect2D(3,2)
		tCopied = Vect2D(3,2)
		v = Vect2D(6,11)
		t.__add__(v)
		self.assertEqual(tCopied.x + v.x, t.x) 
		self.assertEqual(tCopied.y + v.y, t.y)

	def test_skalar_mul(self):
		"""
		check the correctness of scalar multiplication
		of 2 Vect2D vectors
		"""
		t = Vect2D(3,2)
		v = Vect2D(1,2)
		result = t.__mul__(v)
		self.assertEqual(t.x * v.x + t.y * v.y, result)
		

  
if __name__ == '__main__':
    unittest.main()