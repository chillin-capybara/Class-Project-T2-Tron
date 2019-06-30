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


def matrix_collapse(s: dict):
	"""
	Collapse a splitted matrix
	
	Args:
		s (dict): Splitted matrix in format of matrix_slits output
	"""
	# Take the first array and add everything to it
	oneone = s[(1,1)]
	