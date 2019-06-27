import unittest
from InteropComm import InteropComm

class TestInterComm (unittest.TestCase):
	"""
	Test the InterComm dunctionality
	"""



	def test_matrix_split(self):
		"""
		"""
		pass

	def test_matrix_collapse(self):
		"""
		"""
		pass

	def test_reversibility(self):
		"""
		"""
		testObject = InteropComm()
		# Reversibility check
		matrix: list = [[1,2,3],[4,5,6],[7,8,9]]
		splitted_matrix: dict = testObject.matrix_split(matrix, (2,2)) # Or any other split condition
		reconstructed_matrix: list = testObject.matrix_collapse(splitted_matrix)
		# Requirement
		self.assertTrue(matrix == reconstructed_matrix)

if __name__ == "__main__":
	unittest.main()