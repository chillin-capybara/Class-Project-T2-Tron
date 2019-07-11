import random

def generate_random_player_data(sizeX, sizeY, feat_players, directions):
	# Randomly position the players

	# Don't put players at the very end of the arena: Apply padding
	padding = 10 # 10% Padding
	xmin = int(sizeX/padding)
	ymin = int(sizeY/padding)
	xmax = int(sizeX - xmin)
	ymax = int(sizeY - ymin)

	# Create a list of game coordinates
	list_x = list(range(xmin,xmax))
	list_y = list(range(ymin,ymax))

	# Choose random staring points and coordinates for every player
	chx = random.choices(list_x, k=feat_players+1)
	chy = random.choices(list_y, k=feat_players+1)
	pos = []
	for i in range(0,feat_players+1):
		pos = (chx[i], chy[i])
		direct = random.choice(directions)
		yield pos, direct # Generate a new value

ini_data = iter(generate_random_player_data(100,100,10,[(0,1), (0,-1), (1,0), (-1,0)]))
print(next(ini_data))
