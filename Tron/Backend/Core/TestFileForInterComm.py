from InteropComm import InteropComm


testObject = InteropComm()
matrix = [[1,2,3],[4,5,6],[7,8,9]]
matrix = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
matrix: list = [[1,2,3,4,5,6,7]]
max_size = (1,1)
dictionary = testObject.matrix_split(matrix, max_size)
motherMatrix = testObject.matrix_collapse_opt(dictionary)
#print (dictionary)


