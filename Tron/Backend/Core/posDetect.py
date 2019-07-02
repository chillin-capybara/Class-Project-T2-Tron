import numpy as np
import logging

class posDetect (object):
	"""
	implementing of the detection of the player's positions 
	out of 2 matrices, which represent actual and last 
	game field state
	"""

	def getActPos (self, matix, old_matrix, player_id) -> tuple:
		"""
		get the actual Positions of the players on the 
		game field
		
		Args:
			matrix(nested list) - actual game field matrix
			old_matrix(list): last game field matrix
			player_id(int): the player id
		Returns:
			playersPos (tuple): actual player position
		"""

		if type( player_id ) != int:
			raise TypeError
		else:
			if player_id < 0:
				raise ValueError

		# init
		matrix = np.array((matix))
		old_matrix = np.array ((old_matrix))

		difference = matrix - old_matrix


		playerTrack = np.where (difference == player_id, difference, difference*0) # we assume for now that player Track consist of one tuple
		actualPosition = np.nonzero(playerTrack)

		actualPositionTuple = (actualPosition[0][0] + 1, actualPosition[1][0] + 1 )
		logging.warning("Player %d moved to x: %d, y: %d" %(player_id, actualPositionTuple[0], actualPositionTuple[1]))
		return actualPositionTuple