from ..Core.Event import Event
import logging

class StateMaschine:
	"""
	TODO:DOCSTRING
	"""

	INIT               = 0
	CLIENT_READY       = 1
	CLIENT_ERROR       = 2
	CLIENT_WAITING     = 3
	CLIENT_COUNTDOWN   = 4
	CLIENT_INGAME      = 5
	CLIENT_PAUSE       = 6
	CLIENT_ENDGAME     = 7
	EXIT_STATE         = 8

	state = INIT
	EStateChange = Event('oldstate', 'newstate')

	@staticmethod
	def change(newstate):
		"""
		TODO: DOCSTRING
		"""
		if (type(newstate) is not int):
			raise TypeError
		
		StateMaschine.EStateChange(oldstate=StateMaschine.state, newstate=newstate)
		oldstate = StateMaschine.state 
		StateMaschine.state = newstate
		logging.debug("Client State changing from %d to %d" (oldstate, newstate))
	
def on_state_change(sender, oldstate, newstate):
	"""
	TODO: DOCSTRING
	"""

	if newstate == StateMaschine.INIT:
		pass
	elif newstate == StateMaschine.CLIENT_READY:
		pass
	elif newstate == StateMaschine.CLIENT_ERROR: 
		pass
	elif newstate == StateMaschine.CLIENT_WAITING: 
		pass
	elif newstate == StateMaschine.CLIENT_COUNTDOWN: 
		pass
	elif newstate == StateMaschine.CLIENT_INGAME: 
		pass
	elif newstate == StateMaschine.CLIENT_PAUSE: 
		pass
	elif newstate == StateMaschine.CLIENT_ENDGAME: 
		pass
	elif newstate == StateMaschine.EXIT_STATE: 
		pass


#StateMaschine.change(2)