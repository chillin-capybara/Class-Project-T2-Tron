a = [
	[1,2,3,4],
	[5,6,7,8],
	[9,10,11,12]
	]


def partial(a: list, max_row:int, max_col:int, dim_row:int, dim_col:int, i:int,j:int):
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

	for i in range (1, i_max+1):
		for j in range(1, j_max+1):
			result[(i,j)] = partial(a,max_row,max_col,dim_row,dim_col,i,j)
	
	return result





b = [
	[1,2,3,4,5],
	[6,7,8,9,10],
	[11,12,13,14,15]
]

c = [
	[1,2,3],
	[4,5,6],
	[7,8,9]
]

print(matrix_split(c, 3,3))