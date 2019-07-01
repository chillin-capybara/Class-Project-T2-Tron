a = [[1,2,3],[4,5,6],[7,8,9]]

##set variables for splitting
row_max = 2
col_max = 1

##get size of matrix
x_matr = len(a[0])
y_matr = len(a)
print('Matrix has %d columns and %d rows' % (x_matr, y_matr))

##initialize pre
pre = []

##catch row
##cr = row_max - (row_max - i)

##catch column
## [a:b]
## a = 

#get all rows in row_max
c_row = a[0:row_max]
print(c_row)

result = {}

## Diese variable zeigt auf das 1 Element c_row
b = 0
## b kann von 0 hochgezählt werden bis max row_max oder beim letzten was noch 

## Diese variable zeigt auf das 2 Element c_row
c = 1

## Diese variable zeigt auf das 1 Element im Element X der Liste c_row
d = 0

## Diese variable zeigt auf das 2 Element im Element X der Liste c_row 
e = 1

## Diese variable zeigt auf das 3 Element im Element X der Liste c_row
f = 2

## Diese variable zeigt auf das 1 Element c_row
g = 0

##
h = 0

##
j = 1

##
k = 2

## d_row ist die Liste der Elemente in den Reihen row_max bis 2xrow_max oder der restlichen Reihen
d_row = a[row_max:]

##c_row ist die Liste der Elemente in den Reihen 0 bis row_max
c_row = a[0:row_max]


print(c_row)

pre.append(c_row[b][d:col_max+h])
pre.append(c_row[c][d:col_max+h])
print('(1,1): %s' % str(pre))

result[(1,1)] = pre.copy()
pre.clear()

pre.append(c_row[b][e:col_max+j])
pre.append(c_row[c][e:col_max+j])
print('(1,2): %s' % str(pre))

result[(1,2)] = pre.copy()
pre.clear()

pre.append(c_row[b][f:col_max+k])
pre.append(c_row[c][f:col_max+k])
print('(1,3): %s' % str(pre))

result[(1,3)] = pre.copy()
pre.clear()

print(d_row)

pre.append(d_row[g][d:col_max])
print('(2,1): %s' % str(pre))

result[(2,1)] = pre.copy()
pre.clear()

pre.append(d_row[g][e:col_max+1])
print('(2,2): %s' % str(pre))

result[(2,2)] = pre.copy()
pre.clear()

pre.append(d_row[g][f:col_max+2])
print('(2,3): %s' % str(pre))

result[(2,3)] = pre.copy()
pre.clear()



print(result)



######################################################################

A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
i, j = 1, 2
A[i][j]
