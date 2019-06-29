class Hook(object):
	"""
	Callback wrapper class for creating Hooks to parent instances.
	"""
	
	__hook = None

	def __init__(self):
		"""
		Intialize an empty hook.
		"""
		self.__hook = None
	
	def delegate(self, function):
		"""
		Set the deletage method of the hook.

		Args:
			function (callable): Function to call.
		"""
		if self.__hook is not None:
			raise SyntaxError("The hook is already delegated.")

		if callable(function):
			self.__hook = function
	
	def override(self, function):
		"""
		Override an exixsting delegated hook.
		
		Args:
			function (callable): Function to call
		"""
		if callable(self.__hook):
			if callable(function):
				self.__hook = function
			else:
				raise TypeError("The passed argument is not callble")
		else:
			raise SyntaxError("The hook was not yet delegated")
	
	def is_delegated(self) -> bool:
		"""
		Get if the hook is already delegated, or not.
		
		Returns:
			bool: True = Valid callback is presented, False = Not yet delegated
		"""
	
	def __call__(self, *args, **kwargs):
		"""
		Call the delegated hook function with any parameters
		Returns:
			Result of the hook function
		Raises:
			SyntaxError: The hook was not yet delegated
		"""
		if callable(self.__hook):
			return self.__hook(*args, **kwargs)
		else:
			raise SyntaxError("The hook is not yet delegated.")