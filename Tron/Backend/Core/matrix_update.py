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
		game field.
		if there are no difference between old and new game fields detected,
		(-666,-666) tuple returns

		Args:
			matrix(nested list) - actual game field matrix
			old_matrix(list): last game field matrix
			player_id(int): the player id
		Returns:
			playersPos (tuple): actual player position
		Raises:
			ValueError: if the matrices are the same
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

		try:
			actualPositionTuple = (actualPosition[0][0] + 1, actualPosition[1][0] + 1 )
		except Exception as e:
			logging.info("Player %d doesn't move:" %(player_id) + str(e))
			raise ValueError
		else:
			logging.info("Player %d moved to x: %d, y: %d" %(player_id, actualPositionTuple[0], actualPositionTuple[1]))
			return actualPositionTuple


	def getActDirection (self, matrix, old_matrix, player_id: int, old_position: tuple) -> tuple:
		"""
		calculate the actual direction of the player
		in case of messy input data returns (0,0)

			Args:
				matrix (nested list): matrix of the game field
				old_matrix (nested list): (old) matrix of the game field
				player_id (int): id of the player
				old_position (tuple): the actual position of the object
			Returns:
				movDir (tuple): Velocity direction of the player
		"""


		try:
			actualPos = self.getActPos (matrix, old_matrix, player_id)
		except Exception as e:
			logging.error ("Position update failed" + str(e))
			movDir = (0,0)
		else:
			movDir = ( actualPos[0]-old_position[0], actualPos[1]-old_position[1] )


		if (movDir[0] == 0) & (movDir[1] == 0):
			logging.warning ( "Player does not move" )
			# movDir already (0,0)

		if ( abs(movDir[0]) > 1 ) | ( abs(movDir[1]) > 1 ):
			logging.warning ( "Direction update failed: distance too big" )
			movDir = (0,0)

			# raise ValueError
		if (abs (movDir[0]) == 1) & (abs (movDir[1] == 1)):
			logging.warning ( "Direction update failed: diagonal movement" )
			movDir = (0,0)

		return movDir
