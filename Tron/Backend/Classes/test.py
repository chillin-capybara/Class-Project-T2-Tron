def myfunc(sender, pi, ipip):
	"""
	"""
	pass
myc = myfunc.__code__.co_varnames
print(myc)


class TestClass(object):
	def myfun(self, t1, t2):
		pass

obj = TestClass()
myc = obj.myfun.__code__.co_varnames
print(myc)