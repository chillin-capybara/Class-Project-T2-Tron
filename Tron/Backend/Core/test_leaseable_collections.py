import sys
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron')

import unittest
from Tron.Backend.Core.leasable_collections import LeasableList, LeaseError

class TestLeaseableList(unittest.TestCase):
	"""
	Test the functionality of the leaseable list
	"""

	def test_lease_free(self):
		mylist = [1,2,3,4,5,6]
		coll = LeasableList(mylist)

		# Verify the count of elements
		self.assertEqual(len(mylist), coll.count_free())

		# First Lease
		lease1 = coll.lease()
		self.assertEqual(lease1.getObj(), 1) # Check if the first object was released
		self.assertEqual(len(mylist) - 1, coll.count_free()) # Check the sum of free objects

		# Second lease
		lease2 = coll.lease()
		self.assertEqual(lease2.getObj(), 2) # Check if the first object was released
		self.assertEqual(len(mylist) - 2, coll.count_free()) # Check the sum of free objects

		# Third lease
		lease3 = coll.lease()
		self.assertEqual(lease3.getObj(), 3) # Check if the first object was released
		self.assertEqual(len(mylist) - 3, coll.count_free()) # Check the sum of free objects

		# Free up the first lease
		lease1.free()
		self.assertEqual(len(mylist) - 2, coll.count_free())

		# lease 1 is a free instance -> Test if the object is blocked
		with self.assertRaises(LeaseError):
			lease1.getObj()

		# Lease the object again
		lease1 = coll.lease()
		self.assertEqual(lease1.getObj(), 1) # Check if the first object was released
		self.assertEqual(len(mylist) - 3, coll.count_free()) # Check the sum of free objects

		# Lease all the elements
		coll.lease()
		coll.lease()
		coll.lease()

		# Check an invalid lease
		with self.assertRaises(LeaseError):
			coll.lease()
	
	def test_locker_obj(self):
		"""
		Test the locker functionality of the Collection.
		"""
		pass
	
	def test_locker_collection(self):
		"""
		Test the locking functionality of the collection itself
		"""
		pass



if __name__ == '__main__':
	unittest.main()