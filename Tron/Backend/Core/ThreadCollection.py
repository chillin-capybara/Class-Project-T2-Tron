import threading
from typing import List


class ThreadCollection:
	"""
	Collection of threads to automatically handle.
	This class provides functions to automatically track the threads of the
	collection and wait them to stop in the caller thread.
	"""
	
	__collection: List[threading.Thread] = None

	def __init__(self):
		"""
		Initialize a collection of threads that belong to an object or a process.
		"""
		self.__collection = []

	def append(self, thread: threading.Thread):
		"""
		Append a new thread to the collection

		Args:
			thread (threading.Thread): Thread to append
		Raises:
			TypeError: Invalid argument type
		"""
		if isinstance(thread, threading.Thread):
			self.__collection.append(thread)
		else:
			raise TypeError

	def __iadd__(self, thread: threading.Thread):
		self.append(thread)
		return self

	def remove(self, thread: threading.Thread):
		"""
		Remove a thread from the collection

		Args:
			thread (threading.Thread): Thread to remove
		TODO Raises???
		"""
		if isinstance(thread, threading.Thread):
			self.__collection.remove(thread)
		else:
			raise TypeError

	def __isub__(self, thread: threading.Thread):
		self.remove(thread)
		return self

	def join_all(self, timeout: float = None):
		"""
		Wait for all threads in the collection to finish. This function blocks
		the current	thread until all the threads are closed.
		Args:
			timeout (float, optional): Timeout for the thread.join(). Defaults to None.
		"""
		# Go through the list of all threads
		for each_thread in self.__collection:

			# Check it the thread is alive
			if each_thread.is_alive():
				# Wait until it finishes
				each_thread.join(timeout)
