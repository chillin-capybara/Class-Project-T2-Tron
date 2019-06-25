import sys
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron')

from Tron.Backend.Classes.BasicComm import BasicComm
from Tron.Backend.Classes.HumanPlayer import HumanPlayer
import unittest

COMM = BasicComm()
PLAYER = HumanPlayer()

def utf8(string: str):
	return bytes(string, "UTF-8") + b'\x00'


class test_BasicComm(unittest.TestCase):
	"""
	Test the basic communication protocoll
	"""

	def test_client_ready(self):
		"""
		Test the client_ready function
		"""

		# Test Random player data 1
		PLAYER.setName('Joe')
		PLAYER.setColor(1)
		packet = COMM.client_ready(PLAYER)
		original = utf8("JOIN_MATCH Joe 25,25,25")
		self.assertEqual(
			packet,
			original
		)

		# Test Random player data 1
		PLAYER.setName('Jesus')
		PLAYER.setColor(2)
		packet = COMM.client_ready(PLAYER)
		original = utf8("JOIN_MATCH Jesus 50,50,50")
		self.assertEqual(
			packet,
			original
		)


if __name__ == '__main__':
	unittest.main()