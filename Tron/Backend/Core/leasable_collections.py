from .Event import Event

class LeaseError(Exception):
	"""
	Exception for signing that an object is already leased.
	"""
	pass


class LockError(Exception):
	"""
	Exception for signing that an object has an error concerning
	it's locker object's status.
	"""


class LeasableObject(object):
	"""
	Wrapper class for an object lease
	"""
	__index = 0             # Index of the leaseable object
	__obj = None            # Stored object
	__leased = False        # Flag for lease status
	__locker: object = None

	def __init__(self, obj, index: int):
		"""
		Initialize a LeasableObject with for wrapping the original instance.
		Args:
			obj (Any): Object to lease
		"""
		# Set the lease to False at every initialization
		self.__leased = False

		# Set the locker to None
		self.__locker = None

		# Store the object / reference locally
		self.__obj = obj

		self.__index = index

	def get_index(self):
		"""
		Get the index of the current object in the collection.
		Return:
			int: Index
		"""
		return self.__index

	def is_leased(self):
		"""
		Determine wether an object is leased or not.
		Returns:
			bool
		"""
		return self.__leased

	def is_free(self):
		"""
		Determine wether an object is free or not.
		Returns:
			bool
		"""
		return self.__leased != True

	def __lease_base(self):
		"""
		"""

		# Lease the object
		self.__leased = True

		# Return the object wrapper
		return self

	def lease(self):
		"""
		Lease the wrapped object from the collection
		NOTE
			This uses the object itself, for locking it.
		Returns:
			LeaseableObject: Object Wrapper of the leaseable object
		"""
		# Use this object reference as the locker
		return self.lease_lock(self)

	def lease_lock(self, locker: object):
		"""
		Lease the wrapped object using a locker object, to protect it from
			being freed.
		Args:
			locker (object): Any object to use as locker
		Returns:
			LeaseableObject: Object Wrapper of the leaseable object
		"""
		# If the object is leased, return error
		if self.is_leased():
			raise LeaseError("The object is already leased.")

		# Store the object reference of the locker locally
		self.__locker = locker

		# Lease the object
		self.__leased = True

		# Return the object wrapper
		return self

	def getObj(self):
		if self.is_leased():
			return self.__obj
		else:
			raise LeaseError("Cannot access the wrapped object, when it's not leased!")

	def free(self) -> None:
		"""
		Free the leased object if it is leased by `lease()`.
			Uses the object itself to free the object.
		Raises:
			LeaseError: The object is not leased
			LockError:  The object cannot be relesed using itself as a locker
		"""
		self.free_lock(self)

	def free_lock(self, locker: object):
		"""
		Free the leased object if it is leased by `lease()`.
			Uses the `locker` object to free the object.
		Raises:
			LeaseError: The object is not leased
			LockError:  The object cannot be relesed using itself as a locker
		"""
		if self.is_leased():
			if self.__locker is locker:
				self.__locker = None
				self.__leased = False
			else:
				raise LockError("Cannot free. The object is locked by another reference.")
		else:
			raise LeaseError("The object is not leased")



class LeasableList(object):
	"""
	Create a list of object that can be leased and released
	"""
	__collection: list = None
	__orig_list: list = None

	__OnLease: Event  = None
	__OnFree: Event   = None
	__OnUpdate: Event = None

	@property
	def OnLease(self):
		"""
		Event when a new lease from the collection happens
		"""
		return self.__OnLease

	@OnLease.setter
	def OnFree(self, new):
		self.__OnLease = new

	@property
	def OnFree(self):
		"""
		Event when an element is freed in the collection
		"""
		return self.__OnFree

	@OnFree.setter
	def OnFree(self, new):
		self.__OnFree = new

	@property
	def OnUpdate(self):
		"""
		Event when a lease or a free action occures
		"""
		return self.__OnUpdate

	@OnUpdate.setter
	def OnUpdate(self, new):
		self.__OnUpdate = new

	def __init__(self, init_list:list):
		"""
		"""
		# Check the list's type
		if type(init_list) is not list:
			raise TypeError

		self.__collection = []

		self.__OnFree   = Event()
		self.__OnLease  = Event()
		self.__OnUpdate = Event()

		# Store a copy of the original list, to avoid changes by refefence
		self.__orig_list = init_list.copy()

		# Create a collection of leaseable objects
		index = 0
		for obj in self.__orig_list:
			self.__collection.append(LeasableObject(obj, index))
			index += 1

	def count_all(self) -> int:
		"""
		Get the numner of all (free + leased) object in the collection
		Returns:
			int
		"""
		return len(self.__collection)

	def count_free(self) -> int:
		"""
		Get the number of free (leaseable elements) in the collection
		Returns:
			int
		"""
		return sum(1 for obj in self.__collection if obj.is_free() == True)

	def count_leased(self) -> int:
		"""
		Get the number of leased in the collection
		Returns:
			int
		"""
		return sum(1 for obj in self.__collection if obj.is_leased() == True)

	def lease(self) -> LeasableObject:
		"""
		Lease a new object from the collection, when there is one available
		Raises:
			LeaseError: No free oject available
		Returns:
			LeaseableObject: Wrapped object of lease
		"""
		# Get the first not leased object in the collection and return it
		for obj in self.__collection:
			obj: LeasableObject
			if obj.is_free():

				# Call the events
				self.OnLease(self)
				self.OnUpdate(self)

				return obj.lease() # Set the lease of the object

		# No instances found
		raise LeaseError("The collections has no leaseable objects left")

	def lease_lock(self, locker: object) -> LeasableObject:
		"""
		Lease a new object from the collection, when there is one available
		Raises:
			LeaseError: No free oject available
		Returns:
			LeaseableObject: Wrapped object of lease
		"""
		# Get the first not leased object in the collection and return it
		for obj in self.__collection:
			obj: LeasableObject
			if obj.is_free():

				# Call the events
				self.OnLease(self)
				self.OnUpdate(self)

				return obj.lease_lock(locker) # Set the lease of the object

		# No instances found
		raise LeaseError("The collections has no leaseable objects left")

	def free(self, obj: LeasableObject):
		"""
		Free the leased objec `obj` when it is leased by `lease()`
		Args:
			obj (LeaseableObject): object to free
		Raises:
			ValueError: The object is not in the collection
			LeaseError: The object already free
			LockError:  The object was locked by another object
		"""
		# Check the type of the collection
		if type(obj) is not LeasableObject:
			raise TypeError

		# Check if the object is in the collection
		if obj in self.__collection:

			# Call the events
			self.OnFree(self)
			self.OnUpdate(self)

			obj.free()
		else:
			raise ValueError("The object is not part of this collection")

	def free_lock(self, obj: LeasableObject, locker: object):
		"""
		Free the leased objec `obj` when it is leased by `lease()`
		Args:
			obj (LeaseableObject): object to free
			locker (object): Locker object, used to lock the instance
		Raises:
			ValueError: The object is not in the collection
			LeaseError: The object already free
			LockError:  The object was locked by another object
		"""
		# Check the type of the collection
		if type(obj) is not LeasableObject:
			raise TypeError

		# Check if the object is in the collection
		if obj in self.__collection:

			# Call the events
			self.OnFree(self)
			self.OnUpdate(self)

			obj.free()
		else:
			raise ValueError("The object is not part of this collection")

	def lease_lock_collection(self):
		"""
		Wraps the `lease_lock` function using the collection itself as the locker
		"""
		return self.lease_lock(self)

	def free_lock_collection(self, obj: LeasableObject):
		"""
		Wraps the `free_lock` function using the collection itself as the locker
		"""
		self.free_lock(obj, self)

	def free_all(self):
		"""
		Free all the leased elements in the collection.
		WARNING:
			Only works, when all objects are self-locked
			Only use this function, if you're sure that you have no object references left.
		"""
		for obj in self.__collection:
			obj: LeasableObject
			obj.free()
		
		# Call the events
		self.OnFree(self)
		self.OnUpdate(self)
