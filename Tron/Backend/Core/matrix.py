import numpy as np
from .Vect2D import Vect2D
from typing import List

def partial(a: list, max_row:int, max_col:int, dim_row:int, dim_col:int, i:int,j:int):
	"""
	Get a partial matrix of the matrix a using the sizes of a and the maximal
	size of the partial matrices

	Args:
		a (list): Matrix to get partials of
		max_row (int): Maximal number of rows in the partial
		max_col (int): Maximal number of columns in the parti
		dim_row (int): Count of rows in the matri
		dim_col (int): Count of columns in the matrix
		i (int): Partial matrix row index
		j (int): Partial matrix column index

	Returns:
		list: (i,j) Partial matrix in list representation
	"""
	# I DON'T KNOW WHY THIS WORKS; BUT WORKS -> DON'T TOUCH IT!!!!
	pre = []
	rows = a[(i-1) * max_row:min(i*max_row,dim_row)]
	if j > 1:
		x = 1
	else:
		x = 0
	for row in rows:
		ifrom = (j-1)*max_col
		ito = min(j*max_col,dim_col)
		pre.append(row[ifrom:ito])
	return pre

def matrix_split(a: list, max_row:int, max_col:int):
	"""
	Split a matrix into partial matrices with limitations regarding each partial matrix

	Args:
		a (list): Matrix to split
		max_row (int): Maximal number of rows in a partial matrix
		max_col (int): Maximal number of columns in a partial matrix

	Returns:
		dict: {(1,1): [[],[],...], (1,2): ..., (2,3): ... ...}
	"""
	# Get the dimensions of the matrix
	dim_row = len(a)
	dim_col = len(a[0])

	# Calculate the maximal dict indexes
	if dim_row % max_row == 0:
		i_max = int(dim_row / max_row)
	else:
		i_max = int(dim_row/max_row) + 1

	if dim_col % max_col == 0:
		j_max = int(dim_col / max_col)
	else:
		j_max = int(dim_col/max_col) + 1

	result = {}

	# Calculate every partial and apppend them to the results
	for i in range (1, i_max+1):
		for j in range(1, j_max+1):
			result[(i,j)] = partial(a,max_row,max_col,dim_row,dim_col,i,j)

	return result


def split_tostr(split:dict)-> str:
	"""
	Turn the splitted version of the matrix (dict) into a string

	Args:
		split (dict): Splitted matrix

	Returns:
		str: String representation of the splitted matrix
	"""
	pass

def matrix_to_string(matrix:list) -> str:
	"""
	Convert a (partial) matrix into a string

	Args:
		matrix (list): Matrix to format as string

	Returns:
		str: String formatted matrix
	"""
	first = True
	out = ""
	for row in matrix:
		if first:
			out += str(row).strip('[]\'').replace("'", "").replace(" ", "")
			first = False
		else:
			out += ";"+str(row).strip('[]\'').replace("'", "").replace(" ", "")
	return out

def string_to_matrix(string:str) -> list:
	"""
	Convert a string formatted matrix into a matrix

	Args:
		string (str): String formatted matrix representations

	Returns:
		list: List representation of the matrix
	"""
	out = []
	rows = string.split(";")
	for each_row in rows:
		rowlist = each_row.split(",")
		rowlist = list(map(int, rowlist))
		out.append(rowlist)

	return out

def getActPos (matix:List[list], old_matrix:List[list], player_id) -> tuple:
	"""
	get the actual Positions of the players on the
	game field.
	if there are no difference between old and new game fields detected,
	(-666,-666) tuple returns

	Args:
		matrix(nested list) - actual game field matrix
		old_matrix(list): last game field matrix
		player_id(int): the player id
	Returns:
		playersPos (tuple): actual player position
	Raises:
		ValueError: if the matrices are the same
	"""

	if type(player_id) != int:
		raise TypeError

	if player_id < 0:
		raise ValueError

	maxY = len(matix) - 1

	# init
	matrix = np.array((matix))
	old_matrix = np.array((old_matrix))

	difference = matrix - old_matrix

	# we assume for now that player Track consist of one tuple
	playerTrack = np.where(difference == player_id, difference, difference*0)
	actualPosition = np.nonzero(playerTrack)

	try:
		actualPositionTuple = (actualPosition[0][0], actualPosition[1][0])
	except Exception:
		raise ValueError
	else:
		return actualPositionTuple[1], maxY - actualPositionTuple[0]

def get_player_track(matrix: List[list], player_id:int) -> List[Vect2D]:
	"""
	Get the list of points a player already visited

	Args:
		matrix (list): Matrix representation of the game fields
		player_id (int): ID of the player

	Returns:
		List[Vect2D]: list of positions on the arena, the player already visited
	"""
	mylist = []
	maxY = len(matrix[0]) - 1
	for row in range(0, len(matrix)):
		# Go through all the rows and find the indexes
		for col in range(0, len(matrix[0])):
			# Go through the columns of the matrix
			if matrix[row][col] == player_id:
				mylist.append(Vect2D(col, maxY - row))

	return mylist

def getActDirection (actualPos:tuple, old_position: tuple) -> tuple:
	"""
	Calculate the actual direction of the player
	in case of messy input data returns (0,0)

	Args:
		actualPos (tuple): the actual position of the object
		old_position (tuple): the old position of the object
	Returns:
		tuple: Velocity direction of the player
	"""
	x,y = old_position
	xnew, ynew = actualPos

	xdir = 0
	ydir = 0

	if xnew > x:
		xdir = 1
	elif xnew < x:
		xdir = -1

	if ynew > y:
		ydir = 1
	elif ynew < y:
		ydir = -1

	if xdir == ydir:
		raise ValueError  # No direction possible

	return xdir, ydir

def matrix_collapse_opt(splitted_matrix: dict) -> list:
	"""
	collapse splitted matrices "childes" to the mother matrix
	using numpy
		Args:
			splitted_matrix: dict - input splits as a dictionary
		Returns:
			motherMatrix: list - resulting matrix as a nested list
		Raises:
			TODO
	"""
	allKeysList = list(splitted_matrix.keys())
	lastKey = allKeysList[len(allKeysList) - 1]  # fetch matrix dimensions

	motherMatrix = np.array(())  # init mother array

	for currentRow in range (1, lastKey[0] + 1):

		# init row with 1st column
		rowOfMotherMatrix = np.array((splitted_matrix[(currentRow, 1)]))

		# start with 2nd column, because 1st already init
		for currentColumn in range (2, lastKey[1] + 2):
			# handle the the transition between mother rows
			if currentColumn == ((lastKey[1])+1):
				if (currentRow == 1):
					motherMatrix = rowOfMotherMatrix
				else:
					motherMatrix = np.vstack((motherMatrix, rowOfMotherMatrix))
				break
			# handle transition between column inside of the row
			childMatrix = np.array(splitted_matrix[(currentRow, currentColumn)])
			rowOfMotherMatrix = np.hstack((rowOfMotherMatrix, childMatrix))

	motherMatrix = motherMatrix.tolist()

	return motherMatrix
