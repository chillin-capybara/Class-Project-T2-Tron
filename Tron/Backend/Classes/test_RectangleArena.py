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
		testArenaSize = (2,2)
		testArena = RectangleArena(testArenaName, testArenaSize, 2, 2)

		# test if the Name is given correctly
		self.assertEqual(testArena.getName(), testArenaName)

if __name__ == '__main__':
	unittest.main()