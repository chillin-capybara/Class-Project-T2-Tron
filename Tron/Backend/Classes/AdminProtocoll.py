from typing import List
import re

class Route:
	__expression: str = None
	__callback   = None

	def __init__(self, expression: str, callback):
		if not isinstance(expression, str):
			raise TypeError("The expression is not a string")
		
		if not callable(callback):
			raise TypeError("The callback is not callble")

		self.__expression = '^' + expression + '$'
		self.__callback = callback
	
	@property
	def expression(self) -> str:
		"""
		Regual expression of the route
		"""
		return self.__expression
	
	@property
	def callback(self):
		return self.__callback
	
	def __call__(self, args=None):
		"""
		Call the route with the given position arguments
		
		Args:
			args (list): List of positional arguments
		"""
		if args == None:
			self.__callback()
		else:
			self.__callback(*args)


class Router:
	__routes: List[Route] = None
	__default_callback = None

	def __init__(self,):
		# Initialize an empty colleciton of lists
		self.__routes = []
	
	def run(self, string: str):
		"""
		Run the route expressions in the input string
		
		Args:
			string (str): Input string
		"""
		for route in self.__routes:
			matches = list(re.finditer(route.expression, string))  # Find the possible matches
			if len(matches) > 0:
				# When there are matches
				rmatch = matches[0]

				if len(rmatch.groups()) > 0:
					# Fetch the arguments from the regex
					args = list(rmatch.groups())

					# Call the function with the arguments
					route(args)
				else:
					# Call without arguments
					route()
				# Stop the loop, the route was found
				return
		
		# No route was found yet -> Take the default route
		self.__default_callback()

	def add_route(self, regex, callback):
		new_route = Route(regex, callback)
		self.__routes.append(new_route)
	
	def add_default(self, callback):
		"""
		Add a default route when no other routes can be found
		
		Args:
			callback (function): Function to call when no route was found
				The callback has to have one position argument
		"""
		self.__default_callback = callback