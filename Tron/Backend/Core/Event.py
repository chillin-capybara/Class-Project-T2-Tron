import logging

class Event(object):
	"""
	Event definitions for event based programming in Python
	"""

	__callables = None
	__args:list = None
	__called    = False

	def __init__(self, *args):
		self.__called =  False
		self.__args = []
		self.__callables = []

		# Append the required argument
		self.__args.append('sender')

		# Check if a pattern is given
		if len(args) > 0:
			if 'sender' in args:
				raise ValueError("Cannot redefine sender. It's mandatory.")
			if 'self' is args:
				raise ValueError("Cannot add object-self reference.")

			# Add the prototype arguments to the arg list
			for carg in args:
				self.__args.append(carg)
	
	def reset_called(self):
		"""
		Reset the called status of the event.
		"""
		self.__called = False

	def was_called(self):
		"""
		Get if the event was called since the call-flag was reset.
		Returns:
			bool
		"""
		return self.__called

	def __set_called(self):
		"""
		"""
		self.__called = True

	def attach(self, callback):
		"""
		Attach a callback to an event

		Args:
			callback (callable): Callable to call, when an event fires
		
		Raises:
			TypeError: The passed argument is not a callable
		"""
		if not callable(callback):
			raise TypeError
		
		# If the Event handler prototype is invalid
		if not self.matches_prototype(callback):
			raise SyntaxError("Invalid Event Handler. Correct prototype: %s" % self.get_prototype_string())
		
		logging.debug("%s attached to Event" % (callback.__name__))

		self.__callables.append(callback)
	
	def matches_prototype(self, callback):
		"""
		Check if the callble has all the arguments, the event requires
		Args:
			callback (callable): Event handler to check
		Returns:
			bool
		"""
		# Get the variable names of the callback
		callable_args: list = callback.__code__.co_varnames

		# Check prototype arguments in function
		for arg in self.__args:
			if arg not in callable_args:
				return False
		
		# Check arguments in prototype
		#for arg in callable_args:
		#	if (arg is not "self") and (arg not in self.__args): # Remove the self parameter
		#		return False

		return True
	
	def get_prototype_string(self):
		"""
		Gets the Event handler prototype as a string
		Returns:
			str
		"""
		output = "("
		i = 0
		for arg in self.__args:
			if i == 0:
				output += "%s=" % arg
			else:
				output += ",%s=" % arg
			i += 1
		
		output += ")"
		return output

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
		return self
	
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
		return self
	
	def call(self, sender, *args, **kwargs):
		"""
		Call the event with all the attached event handlers

		Args:
			sender (obj): Object that triggers the event
			...
			...
			Free parameters
			
		Raises:
			Anything that event handlers can raise
		"""

		kwargs['sender'] = sender # Define the sender of the call parameters

		for cb in self.__callables:
			cb(**kwargs)          # Call with values
		
		self.__set_called()
	
	def __call__(self, sender, *args, **kwargs):
		"""
		Call the event with all the attached event handlers

		Args:
			sender (obj): Object that triggers the event
			...
			...
			Free parameters
			
		Raises:
			Anything that event handlers can raise
		"""

		self.call(sender, *args, **kwargs)