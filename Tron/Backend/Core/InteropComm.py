class InteropComm(object):
	"""
	Implements Communication methods and functions for 
	the Interoperability tests
	"""

	def matrix_split(self, matrix: list, max_size: tuple) -> dict:
		"""
		Split the given matrix into the parts, 
		which have maximum size max_size
			Args:
			Returns:
			Raises:
		"""
		matrixString = "" # string where the splits will be parsed
		dictionary = {(0,0):matrixString}
		matrixRowCount            = len(matrix)
		matrixColumnCount         = len(matrix[0])
		#calculate new, splitted matrix dimensions
		splittedMatrixRowCount    = matrixRowCount // max_size[0] # how much Rows has the matrix, that consist of splitted parts
		splittedMatrixColumnCount = matrixColumnCount // max_size[1] # how much Columns has the matrix, that consist of splitted parts

		currentRow                = 0 # Row Counter for the loop
		currentColumn             = 0 # Cloumn Counter for the loop

		currentSplittedMatrixRow = 0
		currentSplittedMatrixColumn = 0
		
		for currentSplittedMatrixRow in range (0, splittedMatrixRowCount):
			for currentSplittedMatrixColumn in range (0, splittedMatrixColumnCount):
				# process each "Child" of the Mother matrix
				matrixString = self.processChildMatrix(currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix)
				newDictElement = {(currentSplittedMatrixRow,currentSplittedMatrixColumn) : matrixString}
				dictionary.update(newDictElement)
				matrixString = ""
		
		return dictionary

	def matrix_collapse(self, splitted_matrix: dict) -> list:
		"""
		Build the splitted matrix together
		"""

		pass 
	def processChildMatrix (self, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix):
		"""
		wright down all the Elements of the "Child" Matrix
		"""
		matrixString = ""
		for currentRow in range (currentSplittedMatrixRow * max_size[0] , (currentSplittedMatrixRow+1) * max_size[0]):
			for currentColumn in range (currentSplittedMatrixColumn * max_size[1], (currentSplittedMatrixColumn + 1) * max_size[1]):
				matrixString += str(matrix[currentRow][currentColumn]) # add to the string the matrix item
				if (max_size[1] > 1) & (currentColumn+1 < max_size[1]) : matrixString += ","
			if (max_size[0] > 1) & (currentRow+1 < max_size[0]) : matrixString += ";"
					
		return matrixString




