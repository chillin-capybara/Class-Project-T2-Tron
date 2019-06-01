class Event(object):
	"""
	Event definitions for event based programming in Python
	"""

	__callables = []

	def attach(self, callback):
		"""
		Attach a callback to an event

		Args:
			callback (callable): Callable to call, when an event fires
		
		Raises:
			TypeError: The passed argument is not a callable
		"""
		if callable(callback):
			self.__callables.append(callback)
		else:
			raise TypeError
	
	def detach(self, callback):
		"""
		Detach a callback from an event

		Args:
			callback (callable): Callable to detach
		
		Raises:
			TypeError: The passed argument is not a callable
			ValueError: The callback is not attached to the event
		"""
		if callable(callback):
			self.__callables.remove(callback)
		else:
			raise TypeError
	
	def detachAll(self):
		"""
		Detach all callbacks from the event
		"""
		self.__callables.clear()
	
	def __iadd__(self, other):
		"""
		Operator Overloading for +=

		Args:
			other (callback): Callable to call, when an event fires
		
		Raises:
			TypeError: other is not callable
		"""
		self.attach(other)
	
	def __isub__(self, other):
		"""
		Operator Overloading for -=

		Args:
			other (callback): Callable to call, when an event fires
		
		Raises:
			TypeError: other is not callable
			ValueError: other is not attached to the event
		"""
		self.detach(other)
	
	def call(self, sender, *args, **kwargs):
		"""
		Call the event with all the attached event handlers
		"""

		for cb in self.__callables:
			cb.__call__()
