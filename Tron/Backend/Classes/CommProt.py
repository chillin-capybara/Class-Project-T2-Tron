
class CommProt:
	"""
	Client-Server communikation protocol interface
	"""

	def client_ready(self, player):
		"""
		Get a byte coded client ready message

		Args:
			player: Player	Player Object of the Client

		Returns:
			bytes
		"""
  
		clientReadyMsg = 'clientReady' + player.getName(self) #TODO check getName is a string
  		clientReadyMsg +=  '\r\n'
		bClientReadyMsg = clientReadyMsg.encode('UTF-8') #TODO check bClientReadyMsg is bytes
    
		return bClientReadyMsg
	
	def server_ready(self, game):
		"""
		Get a byte coded server ready message

		Args:
			game: Game	Game object of the current game
							running on the server
		Returns:
			bytes
		"""

		serverReadyMsg = 'serverReady' + game.getName(self) #TODO check getName is a string
  		serverReadyMsg +=  '\r\n'
		bServerReadyMsg = serverReadyMsg.encode('UTF-8') #TODO check bServerReadyMsg is bytes
  
		return bServerReadyMsg
	
	def server_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg: str	Error description (message)
		
		Returns:
			bytes
		"""

		serverErrorMsg = 'serverError: ' + msg
		serverErrorMsg += '\r\n'
		bServerErrorMsg = serverErrorMsg.encode('UTF-8') #TODO check bServerErrorMsg is bytes

		return bServerErrorMsg
	
	def client_error(self, msg):
		"""
		Get a byte coded client error message

		Args:
			msg: str	Error description (message)
		Returns:
			bytes
		"""
		
 		clientErrorMsg = 'clientError: ' + msg
		clientErrorMsg += '\r\n'
		bClientErrorMsg = clientErrorMsg.encode('UTF-8') #TODO check bClientErrorMsg is bytes

		return bClientErrorMsg
	
	def client_start(self):
		"""
		Get a byte coded client start message

		Returns:
			bytes
		"""
		clientStartMsg = 'clientStart'
		clientStartMsg += '\r\n'
		bClientStartMsg = clientStartMsg.encode('UTF-8') #TODO check bClientStartMsg is bytes
		
		return bClientStartMsg
	
	def countdown(self, seconds):
		"""
		Get a byte coded countdown message (server-side)

		Returns:
			bytes
		"""
  
		serverCountdownMsg = 'serverCountdown: ' + seconds
		serverCountdownMsg += '\r\n'
		bServerCountdownMsg = serverCountdownMsg.encode('UTF-8')	
  
		return bServerCountdownMsg
	
	def ingame(self, game):
		"""
		Get a byte coded in-game message for continous synchronization
			between client and server
		Args:
			game: Game	Game object of the current game running on the
							server
		Return:
			bytes
		"""
  
		inGameMsg = 'inGame: ' + game.getName(self)
		inGameMsg += '\r\n'
		bInGameMsg = inGameMsg.encode('UTF-8')

		return bInGameMsg

	def pause(self):
		"""
		Get a byte coded pause request

		Returns:
			bytes
		"""
  
		pauseRequest = 'pauseRequest'
		pauseRequest += '\r\n'
		bPauseRequest = pauseRequest.encode('UTF-8')

		return bPauseRequest

	def continue_game(self, seconds):
		"""
		Get a byte coded continue request

		Returns:
			bytes
		"""
  
		continueRequest = 'continueRequest'
		continueRequest += '\r\n'
		bContinueRequest = continueRequest.encode('UTF-8')

		return bContinueRequest
	
	def ack_pause(self):
		"""
		Get a byte response for acknowledging a pause

		Returns:
			bytes
		"""

		pauseAck = 'pauseAck'
		pauseAck += '\r\n'
		bPauseAck = pauseAck.encode('UTF-8')
  	
		return bPauseAck

	def ack_continue(self):
		"""
		Get a byte response for acknowledging a continue_game action

		Returns:
			bytes
		"""
		continueAck = 'continueAck'
		continueAck += '\r\n'
		bContinueAck = continueAck.encode('UTF-8')
  	
		return bContinueAck
	
	def exit_game(self):
		"""
		Get a byte request for exiting a running game
		
		Returns:
			bytes
		"""
		exitGameRequest = 'exitGameRequest'
		exitGameRequest += '\r\n'
		bExitGameRequest = exitGameRequest.encode('UTF-8')

		return bExitGameRequest
	
	def end_game(self):
		"""
		Get a byte request for ending a running game

		Returns:
			bytes
		"""
		endGameRequest = 'endGameRequest'
		endGameRequest += '\r\n'
		bEndGameRequest = endGameRequest.encode('UTF-8')

		return bEndGameRequest
	
	def revenge(self):
		"""
		Get a byte request for requesting a revenge

		Returns:
			bytes
		"""
		revengeGameRequest = 'revengeGameRequest'
		revengeGameRequest += '\r\n'
		bRevengeGameRequest = revengeGameRequest.encode('UTF-8')

		return bRevengeGameRequest
	
	def ack_revenge(self):
		"""
		Get a byte response for accepting a revenge

		Returns:
			bytes
		"""
		revengeAck = 'revengeAck'
		revengeAck += '\r\n'
		bRevengeAck = revengeAck.encode('UTF-8')
  	
		return bRevengeAck

	

