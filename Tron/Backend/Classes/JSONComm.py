from CommProt import CommProt
import json

class JSONComm(CommProt):
	"""
	Communication protocoll implementation using JSON format
	"""

	def string_to_bytes(self, string):
		"""
		Convert a string to an encoded byte array

		Args:
			string (str): String to convert
		Returns:
			bytes: Encoded string
		"""
		if type(string) == str:
			return bytes(string, "UTF-8")
		else:
			raise TypeError
	
	def dict_to_jsonbytes(self, dict):
		"""
		Convert a Dictionary to JSON String, then to encoded byte array

		Args:
			dict (dict): Dictionary
		Returns:
			bytes: Encoded dictionary
		"""
		return self.string_to_bytes(json.dumps(dict))


	def server_error(self, msg):
		"""
		Get a byte coded server error message

		Args:
			msg (str):	Error description (message)
		
		Returns:
			bytes
		NOTE:
			{"type":"server_error", "message": "this is the message"}
		"""
		msgdict = {'type': 'server_error', 'message': msg}
		return self.dict_to_jsonbytes(msgdict)
	
	def client_error(self, msg):
		"""
		Get a byte coded client error message

		Args:
			msg (str): Error description (message)
		Returns:
			bytes
		NOTE:
			{"type":"server_error", "message": "this is the message"}
		"""
		pass