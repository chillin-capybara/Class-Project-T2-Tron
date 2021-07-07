from Backend.Core.InteropComm import InteropComm

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



spl = InteropComm()
matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
splitted = spl.matrix_split(matrix,(2,2))

ms = matrix_to_string(matrix)
print(ms)
print()
a = string_to_matrix(ms)
print(a)

print(a == ms)