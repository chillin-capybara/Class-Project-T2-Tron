import array

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
		# check if the matrix just consist of int 
		# if not all(isinstance(item, int) for item in list):
		# 	raise TypeError

		if  (type(max_size[0]) != int) | (type(max_size[1]) != int):
			raise TypeError
		else:
			if (max_size[0] > len(matrix)) | (max_size[1] > len(matrix[0])):
				raise ValueError

		matrixArray = [[0 for x in range(max_size[1])] for y in range(max_size[0])] #initialize Array for splitted matrices
		dictionary = {(0,0):matrixArray}
		matrixRowCount            = len(matrix)
		matrixColumnCount         = len(matrix[0])
		#calculate new, splitted matrix dimensions
		splittedMatrixRowCount    = matrixRowCount // max_size[0] # how much Rows has the matrix, that consist of splitted parts
		splittedMatrixColumnCount = matrixColumnCount // max_size[1] # how much Columns has the matrix, that consist of splitted parts

		#check if one extra iteration for "smaller" child matrices needed
		if (matrixRowCount - splittedMatrixRowCount * max_size[0]) > 0: splittedMatrixRowCount += 1
		if (matrixColumnCount - splittedMatrixColumnCount * max_size[0]) > 0: splittedMatrixColumnCount += 1

		currentRow                = 0 # Row Counter for the loop
		currentColumn             = 0 # Cloumn Counter for the loop

		currentSplittedMatrixRow = 0
		currentSplittedMatrixColumn = 0

		
		for currentSplittedMatrixRow in range (0, splittedMatrixRowCount):
			for currentSplittedMatrixColumn in range (0, splittedMatrixColumnCount):
				# process each "Child" of the Mother matrix
				matrixArray = self.processChildMatrix(currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount)
				newDictElement = {(currentSplittedMatrixRow,currentSplittedMatrixColumn) : matrixArray}
				dictionary.update(newDictElement)
				matrixArray = [[0 for x in range(max_size[1])] for y in range(max_size[0])] #reset Array for splitted matrices

		
		return dictionary

	def processChildMatrix (self, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount):
		"""
		wright down all the Elements of the "Child" Matrix
		"""
		matrixArray = [[0 for x in range(max_size[1])] for y in range(max_size[0])] #initialize Array for splitted matrices

		for currentRow in range (currentSplittedMatrixRow * max_size[0] , (currentSplittedMatrixRow+1) * max_size[0]):
			if currentRow + 2 > matrixRowCount: break
			for currentColumn in range (currentSplittedMatrixColumn * max_size[1], (currentSplittedMatrixColumn + 1) * max_size[1]):
				if currentColumn + 2 > matrixColumnCount: break

				matrixRow = currentRow - max_size[0]*currentSplittedMatrixRow
				matrixColumn = currentColumn - max_size[1]*currentSplittedMatrixColumn

				matrixArray[matrixRow][matrixColumn] = matrix[currentRow][currentColumn]

				#if (max_size[1] > 1) & (((currentColumn+1)//(currentSplittedMatrixColumn+1)) < max_size[1]) : matrixString += ","
			#if (max_size[0] > 1) & ((currentRow+1)//(currentSplittedMatrixRow+1) < max_size[0]) : matrixString += ";"
					
		return matrixArray

	def matrix_collapse(self, splitted_matrix: dict) -> list:
		"""
		Build the splitted matrix together
		"""
		motherMatrix: list

		#calculate the dimension of the future new mother matrix
		lastTuple = splitted_matrix.keys()[-1]
		splittedMatrixRowCount, splittedMatrixColumnCount = lastTuple
		
		for currentSplit in range (0,len(splitted_matrix)):
			
			matrixString = splitted_matrix.values[currentSplit]
			for currentCharacterCounter in range (0, len(matrixString - 1)):
				currentCharacter = matrixString [currentCharacterCounter]
				if (currentCharacter != ",") & (currentCharacter != ";"): 
					motherMatrix[motherRow][motherColumn] = int(currentCharacter)

		return motherMatrix




