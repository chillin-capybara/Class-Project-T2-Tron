
class TrackError(Exception):
	"""
	Signals an error with an invalid track object.
	"""
	pass

class CommError(Exception):
	"""
	Signals an error with the client-server communication.
	"""
	pass

class ServerError(Exception):
	"""
	Signals an error in the Game server mode
	"""
	pass