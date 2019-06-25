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
	def test_process_client_ready(self):
		"""
		Test the processing of the client_ready messages
		"""

		# Sampel DATA
		PLAYER.setName('Jesus')
		PLAYER.setColor(2)
		packet = COMM.client_ready(PLAYER)
		ptype, player = COMM.process_response(packet)
		self.assertEqual(ptype, COMM.CLIENT_READY)
		self.assertTrue(player == PLAYER)

		# Test with sample data 2
		PLAYER.setName('EverydayJoe')
		PLAYER.setColor(10)
		packet = COMM.client_ready(PLAYER)
		ptype, player = COMM.process_response(packet)
		self.assertEqual(ptype, COMM.CLIENT_READY)
		self.assertTrue(player == PLAYER)



	def test_client_ready_ack(self):
		"""
		Test the client_ready ack message
		"""
		# Test with ID=0
		packet = COMM.client_ready_ack(0)
		original = utf8("MATCH_JOINED 0")
		self.assertEqual(
			packet,
			original
		)
		# Test with ID=1
		packet = COMM.client_ready_ack(1)
		original = utf8("MATCH_JOINED 1")
		self.assertEqual(
			packet,
			original
		)
	
	def test_process_client_ready_ack(self):
		"""
		Process the client_ready acknowledgement
		"""
		# Test with random data 0
		packet = COMM.client_ready_ack(0)
		ptype, player_id = COMM.process_response(packet)
		self.assertEqual(ptype, COMM.CLIENT_READY_ACK)
		self.assertEqual(player_id, 0)

		# Test with random data 100
		packet = COMM.client_ready_ack(100)
		ptype, player_id = COMM.process_response(packet)
		self.assertEqual(ptype, COMM.CLIENT_READY_ACK)
		self.assertEqual(player_id, 100)

if __name__ == '__main__':
	unittest.main()