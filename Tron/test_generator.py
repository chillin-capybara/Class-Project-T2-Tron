# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"^log"

test_str = "log"

matches = list(re.finditer(regex, test_str))  # Find the possible matches
rmatch = matches[0]

if len(rmatch.groups()) > 0:
	# Call with args
	args = list(rmatch.groups())
	print("Call with n = %s arguments %s" % (len(rmatch.groups()), str(args)))
else:
	# Call without arguments
	print("Only command")