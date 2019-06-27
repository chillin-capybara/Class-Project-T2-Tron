class InteropComm(object):
	"""
	Implements Communication methods and functions for 
	the Interoperability tests
	"""
	def matrix_split(matrix: list, max_size: tuple) -> dict:
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
				
				for currentRow in range (currentSplittedMatrixRow * max_size[0] , (currentSplittedMatrixRow+1) * max_size[0]):
					for currentColumn in range (currentSplittedMatrixColumn* max_size[1], (currentSplittedMatrixColumn+1)* max_size[1]):
						if currentColumn > 0 : matrixString += ","
						matrixString += str(matrix[currentRow][currentColumn]) # add to the string the matrix item
					matrixString += ";"
				
				newDictElement = {(currentSplittedMatrixRow,currentSplittedMatrixColumn) : matrixString}
				dictionary.update(newDictElement)
				matrixString = ""
		
		return dictionary

	def matrix_collapse(splitted_matrix: dict) -> list:
		"""
		Build the splitted matrix together
		"""

		pass 
	matrix = [[1,2,3],[4,5,6],[7,8,9]]
	dictionary = matrix_split(matrix, (3,1))
	print (dictionary)