from CommProt import CommProt
import json

class JSONComm(CommProt):
	"""
	Communication protocoll implementation using JSON format
	"""

	def string_to_bytes(self, string):
		"""
		TODO: DOCSTRING
		"""
		if type(string) == str:
			return bytes(string, "UTF-8")
		else:
			raise TypeError
	
	def dict_to_jsonbytes(self, dict):
		"""
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