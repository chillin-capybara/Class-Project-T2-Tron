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
		dictionary = {(1,1):matrixArray}
		matrixRowCount            = len(matrix)
		matrixColumnCount         = len(matrix[0])
		#calculate new, splitted matrix dimensions
		splittedMatrixRowCount    = matrixRowCount // max_size[0] # how much Rows has the matrix, that consist of splitted parts
		splittedMatrixColumnCount = matrixColumnCount // max_size[1] # how much Columns has the matrix, that consist of splitted parts

		#check if one extra iteration for "smaller" child matrices needed
		if (matrixRowCount - splittedMatrixRowCount * max_size[0]) > 0: splittedMatrixRowCount += 1
		if (matrixColumnCount - splittedMatrixColumnCount * max_size[1]) > 0: splittedMatrixColumnCount += 1

		currentRow                = 0 # Row Counter for the loop
		currentColumn             = 0 # Cloumn Counter for the loop

		currentSplittedMatrixRow = 0
		currentSplittedMatrixColumn = 0

		
		for currentSplittedMatrixRow in range (0, splittedMatrixRowCount):
			for currentSplittedMatrixColumn in range (0, splittedMatrixColumnCount):
				# process each "Child" of the Mother matrix
				matrixArray = self.processChildMatrix(currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount)
				newDictElement = {(currentSplittedMatrixRow + 1 ,currentSplittedMatrixColumn + 1) : matrixArray}
				dictionary.update(newDictElement)
				#matrixArray = [[0 for x in range(max_size[1])] for y in range(max_size[0])] #reset Array for splitted matrices

		
		return dictionary

	def processChildMatrixOld (self, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount):
		"""
		wright down all the Elements of the "Child" Matrix
		"""
		 

		#calculate Row und Column Size for the Child matrix
		childMatrixRowCount = matrixRowCount - (currentSplittedMatrixRow + 1) * max_size[0] + 1
		childMatrixColumnCount = matrixColumnCount - (currentSplittedMatrixColumn + 1) * max_size[1] + 1

		#initialize child matrix 
		matrixArray = [[0 for x in range(childMatrixColumnCount)] for y in range(childMatrixRowCount)]

		# right down all the arguments to the child matrix array
		#iterate on rows
		for currentRow in range (currentSplittedMatrixRow * max_size[0] , (currentSplittedMatrixRow+1) * max_size[0]):
			
			#calculate current row of child matrix
			currentChildRow = currentRow - max_size[0]*currentSplittedMatrixRow

			#check if current child row not out of range
			if currentChildRow >= childMatrixRowCount:
				break
			


			# iterate on columns
			for currentColumn in range (currentSplittedMatrixColumn * max_size[1], (currentSplittedMatrixColumn + 1) * max_size[1]):

				#calculate current column of child matrix
				currentChildColumn = currentColumn - max_size[0]*currentSplittedMatrixColumn

				#check if current child column not out of range
				if currentChildColumn >= childMatrixColumnCount:
					break


				#right down mother element into child matrix
				matrixArray[currentChildRow][currentChildColumn] = matrix[currentRow][currentColumn]

					
		return matrixArray


	def processChildMatrix(self, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size, matrix, matrixRowCount, matrixColumnCount):
		"""
		wright down all the Elements of the "Child" Matrix
		"""

		childMatrix: list
		
		childSize = self.getChildSize (matrixRowCount, matrixColumnCount, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size)

		childMatrix = [[0 for x in range( childSize[1] )] for y in range( childSize[0] )]

		# right down all the arguments to the child matrix array
		#iterate on rows
		

		for currentRow in range (currentSplittedMatrixRow * max_size[0] , currentSplittedMatrixRow * max_size[0] + childSize[0] ):
			
			#calculate current row of child matrix
			currentChildRow = currentRow - max_size[0] * currentSplittedMatrixRow

			#check if current child row not out of range
			if currentChildRow >= childSize[0]:
				break

			# iterate on columns
			for currentColumn in range (currentSplittedMatrixColumn * max_size[1], currentSplittedMatrixColumn * max_size[1] + childSize[1] ):

				#calculate current column of child matrix
				currentChildColumn = currentColumn - max_size[1]*currentSplittedMatrixColumn

				#check if current child column not out of range
				if currentChildColumn >= childSize[1]:
					break

				#right down mother element into child matrix
				childMatrix[currentChildRow][currentChildColumn] = matrix[currentRow][currentColumn]

		return childMatrix

 
	def getChildSize (self, matrixRowCount, matrixColumnCount, currentSplittedMatrixRow, currentSplittedMatrixColumn, max_size):
		"""
		calculates the size of the Child matrix in the current position of the Mother matrix
			Returns: childSize tuple
		"""
		#row
		rowDifference = (currentSplittedMatrixRow + 1) * max_size[0] - matrixRowCount

		if rowDifference > 0:
			childSizeRow = max_size[0] - rowDifference
		else: 
			childSizeRow = max_size[0]

		#column
		columnDifference = (currentSplittedMatrixColumn + 1 ) * max_size[1] - matrixRowCount

		if columnDifference > 0:
			childSizeColumn = max_size[1] - columnDifference
		else:
			childSizeColumn = max_size[1]


		# childSizeRow = matrixRowCount - (currentSplittedMatrixRow + 1) * max_size[0] + 1
		# childSizeColumn = matrixColumnCount - (currentSplittedMatrixColumn + 1) * max_size[1] + 1

		childSize = (childSizeRow, childSizeColumn)

		if childSize[0] < 1 | childSize[1] < 1 :
			raise ValueError

		if childSize[0] < max_size[0] | childSize[1] < max_size[1] :
			raise ValueError

		return childSize

	def takeMotherElementToChild (self, currentChildRow, currentChildColumn, currentRow, currentColumn):
		pass



	def matrix_collapseOld(self, splitted_matrix: dict) -> list:
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


	def matrix_collapse (self, splitted_matrix: dict) -> list:
		"""
		"""
		
		allKeysList = list( splitted_matrix.keys() )
		lastKey = allKeysList [ len(allKeysList) - 1 ]	
		firstKey = allKeysList [0]
		
		motherMatrix :list = [0] # init
		bigMotherMatrix = [0]

			
		# iterate over Rows
		for currentRow in range (1, lastKey[0]):

			for currentInsideRow in range ( 0, len( splitted_matrix[ firstKey ] ) - 1 ):
				
				#iterate over Colums
				for currentColumn in range (1, lastKey[1]):
					
					for currentInsideColumn in range ( 0, len( splitted_matrix[ firstKey ][0] ) - 1 ): 
						
						motherMatrixColumn = (currentColumn - 1)*(len( splitted_matrix[ firstKey ][0] ) ) + currentInsideColumn
						motherMatrixRow = (currentRow - 1)*(len( splitted_matrix[ firstKey ] ) )  + currentInsideRow
						
						newElement = splitted_matrix[(currentRow,currentColumn)][currentInsideRow][currentInsideColumn]
						# motherMatrix[motherMatrixRow][motherMatrixColumn].append( newElement )
						motherMatrix[motherMatrixRow].append( newElement )
				bigMotherMatrix[currentRow].append ( motherMatrix )
				motherMatrix = []
		return motherMatrix




	def matrix_collapseOld2 (self, splitted_matrix: dict) -> list:
		"""
		"""

		motherMatrix = self.createMotherMatrix (splitted_matrix)

		#process partikular dict element
		for currentSplit in range(len(splitted_matrix)-1):
			
			
			currentRowRange = len(list(splitted_matrix.values())[currentSplit])-1


			#process one Row in dict element
			for currentRow in range (currentRowRange):
				matrixRowList = list (splitted_matrix.values())[currentSplit] # 

				# currentElementCounterRange = len(matrixRowList)-1

				#process one Element in Row
				for currentElementCounter in range (len(matrixRowList)-1):
					# find mother Matrix positions
					currentSplittedMatrixPosition = list(splitted_matrix.keys())[currentSplit] #should be a tuple					
					motherRow = currentSplittedMatrixPosition[0]
					motherColumn = currentSplittedMatrixPosition[1]


					currentSplittedMatrix = list(splitted_matrix.values())

					splittedMatrixElementValue = currentSplittedMatrix[currentRow][currentElementCounter]

					motherMatrix[motherRow][motherColumn] = splittedMatrixElementValue
		return motherMatrix		

	def createMotherMatrix (self, splitted_matrix):
		"""
		initialize Mother matrix for further calculations
		"""
		#find out, how many splits you have
		lastTuple = list(splitted_matrix.keys())[-1]
		splittedMatrixRowCount, splittedMatrixColumnCount = lastTuple
		lastRow, lastColumn = lastTuple
		#debug
		allKeysList = list( splitted_matrix.keys() )
		lastKey = allKeysList [ len(allKeysList)-1 ]

		#print ( allKeysList ) #debug
		#print ( lastKey ) #debug

		lastRow       = lastKey[0]
		lastColumn    = lastKey[0]

		#check count of row in last row
		#motherMatrixAppendix = list( splitted_matrix.values() )
		rowAppendix = len( list( splitted_matrix.values() ) [lastRow] )
		

		#print (rowAppendix) # debug
		print (list( splitted_matrix.values() ))
		print (list( splitted_matrix.values() ) [1][lastColumn])



		#check count of column in last column
		columnAppendix = len( list( splitted_matrix.values() ) [1][lastColumn] )# we check it in the first row

		# calculate mother Rows
		if splittedMatrixRowCount > 1 :
			if rowAppendix == len( list( splitted_matrix.values() )[lastRow-1] ):
				motherMatrixRowCount = splittedMatrixRowCount * rowAppendix 

			elif rowAppendix < len( list( splitted_matrix.values() )[lastRow-1] ):
				motherMatrixRowCount = ( splittedMatrixRowCount - 1 ) * len( list( splitted_matrix.values() )[lastRow-1] ) + rowAppendix
			else:
				raise ValueError

		# calculate mother Columns
		if splittedMatrixColumnCount > 1 :
			if columnAppendix == len( list( splitted_matrix.values() )[1][lastColumn-1] ):
				motherMatrixColumnCount = splittedMatrixColumnCount * columnAppendix 

			elif columnAppendix < len( list( splitted_matrix.values() )[1][lastColumn-1] ):
				motherMatrixColumnCount = ( splittedMatrixColumnCount - 1 ) * len( list( splitted_matrix.values() )[1][lastColumn-1] ) + columnAppendix
			else:
				raise ValueError

		motherMatrix = [[0 for x in range( motherMatrixColumnCount - 1 )] for y in range( motherMatrixRowCount - 1 )]

		return motherMatrix


