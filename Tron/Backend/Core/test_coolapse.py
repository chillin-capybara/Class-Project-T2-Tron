
d = {
	(1,1): [[1,2],[4,5]],
	(1,2): [[3],[6]],
	(2,1): [[7.8]],
	(2,2): [[9]]
}

result = []

# Get the highest partial matrix indexes
max_x = 0
max_y = 0
for x,y in d.keys():
	max_x = max(x, max_x)
	max_y = max(y, max_y)

# Create the empty nested list for the matrix
for i in range(0, max_x):
	result.append([])

# Now lets add the elements
for x,y in d.keys():
	max_x = max(x, max_x)
	max_y = max(y, max_y)