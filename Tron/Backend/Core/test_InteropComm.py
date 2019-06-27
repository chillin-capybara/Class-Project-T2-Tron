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
		# Reversibility check
		matrix: list = [[1,2,3],[4,5,6][7,8,9]]
		splitted_matrix: dict = InteropComm.matrix_split(matrix, (2,2)) # Or any other split condition
		reconstructed_matrix: list = InteropComm.matrix_collapse(splitted_matrix)
		# Requirement
		self.assertTrue(matrix == reconstructed_matrix)