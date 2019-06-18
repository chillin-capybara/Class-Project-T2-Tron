import time

def get_timestamp() -> int:
	"""
	Get the current timestamp in the moment of the function call

	Returns:
		int: Current timestamp in UNIX format
	"""
	return int(time.time())