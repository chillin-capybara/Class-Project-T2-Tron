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
		#matrix: list = [[1,2,3],[4,5,6],[7,8,9]]
		matrix: list = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
		# matrix: list = [[1,2,3,4,5,6,7]]
		# matrix: list = [[1],[2],[3],[4],[5],[6]]
		# matrix: list = [[1]]
		splitted_matrix: dict = testObject.matrix_split(matrix, (5,5))
		print(splitted_matrix ) # Or any other split condition
		reconstructed_matrix: list = testObject.matrix_collapse_opt(splitted_matrix)
		print (reconstructed_matrix)
		# Requirement
		self.assertTrue(matrix == reconstructed_matrix)

if __name__ == "__main__":
	unittest.main()