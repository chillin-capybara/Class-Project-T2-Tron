import unittest
from RectangleArena import RectangleArena

class TestRectangleArena(unittest.TestCase):
	"""
	Test the RectangleArena functionality
	"""

	def test_getName(self):
		"""
		test the getName functionality
		"""
		testArenaName = "testArenaName"
		testArenaSize = (10,10)
		testArena = RectangleArena(testArenaName, testArenaSize, 2, 2)
		# test if the Name is given correctly
		self.assertEqual(testArena.getName(), testArenaName)
		# test if Name can not be too long or to short
		# test if Name can not be other types then string

	def test_str(self): #TODO: redo test properly, now it is the same as test_getName
		"""
		test the __str__ functionality
		"""
		testArenaName = "testArenaName"
		testArenaSize = (10,10)
		testArena = RectangleArena(testArenaName, testArenaSize, 2, 2)
		
		#print (str(testArena))
		self.assertEqual(str(testArena), testArenaName)
	
	def test_getSize(self):
		"""
		test the getSize functionality
		"""
		# test if the size is greater then (4,4)
		with self.assertRaises(ValueError):
			testArena = RectangleArena("testArenaName", (0,0), 2, 2)
		# test if the size of the arena can not be anything else as a positive integer
		with self.assertRaises(ValueError):
			testArena = RectangleArena("testArenaName", (-1,5), 2, 2)
		with self.assertRaises(ValueError):
			testArena = RectangleArena("testArenaName", (6,-2), 2, 2)
		#not an integer case
		with self.assertRaises(TypeError):
			testArena = RectangleArena("testArenaName", (5j,6), 2, 2)
		with self.assertRaises(TypeError):
			testArena = RectangleArena("testArenaName", (7,3.5), 2, 2)

		#not a number case
		with self.assertRaises(TypeError):
			testArena = RectangleArena("testArenaName", ("five",6), 2, 2)
		with self.assertRaises(TypeError):
			testArena = RectangleArena("testArenaName", (6,"ten"), 2, 2)

		


if __name__ == '__main__':
	unittest.main()