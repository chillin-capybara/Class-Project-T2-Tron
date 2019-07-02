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