dx, dy = (0,-1)
dxnew, dynew = (0,1)

if (dx == -dxnew and dxnew != 0) or (dy == -dynew and dynew != 0):
	print("Invalid direction from %s to %s" % (str((dx,dy)), str((dxnew, dynew))))
else:
	print("NEW VELOCITY SET")