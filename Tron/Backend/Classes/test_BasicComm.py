import sys
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron')

from Tron.Backend.Classes.BasicComm import BasicComm
from Tron.Backend.Classes.HumanPlayer import HumanPlayer
from Tron.Backend.Core.Event import Event
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
		PLAYER.setColor((25,25,25))
		packet = COMM.client_ready(PLAYER)
		original = utf8("JOIN_MATCH Joe 25,25,25")
		self.assertEqual(
			packet,
			original
		)

		# Test Random player data 1
		PLAYER.setName('Jesus')
		PLAYER.setColor((2,2,2))
		packet = COMM.client_ready(PLAYER)
		original = utf8("JOIN_MATCH Jesus 2,2,2")
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
		PLAYER.setColor((2,2,2))
		packet = COMM.client_ready(PLAYER)
		ptype, player = COMM.process_response(packet)
		self.assertEqual(ptype, COMM.CLIENT_READY)
		self.assertTrue(player == PLAYER)

		# Test with sample data 2
		PLAYER.setName('EverydayJoe')
		PLAYER.setColor((1,1,1))
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
	
	def test_err_incorrect_cmd(self):
		"""
		Test the incorrect command message
		"""

		# Test if the message is correct
		msg = COMM.error_incorrect_cmd()
		self.assertEqual(msg, utf8("ERR_CMD_NOT_UNDERSTOOD"))
	
	def test_process_err_incorrect_cmd(self):
		"""
		Test the processing of incorrect command messaged
		"""

		COMM.EServerError: Event
		COMM.EServerError.reset_called()

		msg = COMM.error_incorrect_cmd()
		mtype, res = COMM.process_response(msg)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(res, "ERR_CMD_NOT_UNDERSTOOD")
		self.assertEqual(COMM.EServerError.was_called(), True)

	def test_failed_to_create(self):
		"""
		Test the failed to create message
		"""
		# Sample data 1
		reason = "Name already taken"
		packet = COMM.failed_to_create(reason)
		original = utf8("ERR_FAILED_TO_CREATE Name already taken")
		self.assertEqual(packet, original)

		# Sample data 2
		reason = "Color already reserved"
		packet = COMM.failed_to_create(reason)
		original = utf8("ERR_FAILED_TO_CREATE Color already reserved")
		self.assertEqual(packet, original)

		# Empty reason -> ValueError
		reason = ""
		with self.assertRaises(ValueError):
			packet = COMM.failed_to_create(reason)

		# TypeError
		with self.assertRaises(TypeError):
			COMM.failed_to_create(2)

		with self.assertRaises(TypeError):
			COMM.failed_to_create([])

	def test_process_failed_to_create(self):
		"""
		Test the processing of a failed to create message
		"""
		# Sample data 1
		packet = COMM.failed_to_create("This is the reason...")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "Failed to create match. Reason: %s" % "This is the reason...")

		# Sample data 2
		packet = COMM.failed_to_create("Reason2")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "Failed to create match. Reason: %s" % "Reason2")
	
	def test_failed_to_join(self):
		"""
		Test the failed to join messages
		"""
		# Sample data 1
		reason = "Name already taken"
		packet = COMM.failed_to_join(reason)
		original = utf8("ERR_FAILED_TO_JOIN Name already taken")
		self.assertEqual(packet, original)

		# Sample data 2
		reason = "Color already reserved"
		packet = COMM.failed_to_join(reason)
		original = utf8("ERR_FAILED_TO_JOIN Color already reserved")
		self.assertEqual(packet, original)

		# Empty reason -> ValueError
		reason = ""
		with self.assertRaises(ValueError):
			packet = COMM.failed_to_join(reason)

		# TypeError
		with self.assertRaises(TypeError):
			COMM.failed_to_join(2)

		with self.assertRaises(TypeError):
			COMM.failed_to_join([])

	def test_game_not_exists(self):
		"""
		Test the game not exists error message
		"""
		# Sample data 1
		reason = "Game1"
		packet = COMM.game_not_exists(reason)
		original = utf8("ERR_GAME_NOT_EXIST Game1")
		self.assertEqual(packet, original)

		# Sample data 2
		reason = "TestGame"
		packet = COMM.game_not_exists(reason)
		original = utf8("ERR_GAME_NOT_EXIST TestGame")
		self.assertEqual(packet, original)

		# Empty reason -> ValueError
		reason = ""
		with self.assertRaises(ValueError):
			packet = COMM.game_not_exists(reason)

		# TypeError
		with self.assertRaises(TypeError):
			COMM.game_not_exists(2)

		with self.assertRaises(TypeError):
			COMM.game_not_exists([])
	
	def test_disconnecting_you(self):
		"""
		Test the disconnecting you message
		"""
		# Sample data 1
		reason = "Just because"
		packet = COMM.disconnect_client(reason)
		original = utf8("DISCONNECTING_YOU Just because")
		self.assertEqual(packet, original)

		# Sample data 2
		reason = "This is the reason 2"
		packet = COMM.disconnect_client(reason)
		original = utf8("DISCONNECTING_YOU This is the reason 2")
		self.assertEqual(packet, original)

		# Empty reason -> ValueError
		reason = ""
		with self.assertRaises(ValueError):
			packet = COMM.disconnect_client(reason)

		# TypeError
		with self.assertRaises(TypeError):
			COMM.disconnect_client(2)

		with self.assertRaises(TypeError):
			COMM.disconnect_client([])
	
	def test_leaving_match(self):
		"""
		Test a leaving match message generation
		"""
		# Sample data 1
		reason = "Just because"
		packet = COMM.leaving_match(reason)
		original = utf8("LEAVING_MATCH Just because")
		self.assertEqual(packet, original)

		# Sample data 2
		reason = "This is the reason 2"
		packet = COMM.leaving_match(reason)
		original = utf8("LEAVING_MATCH This is the reason 2")
		self.assertEqual(packet, original)

		# Empty reason -> ValueError
		reason = ""
		with self.assertRaises(ValueError):
			packet = COMM.leaving_match(reason)

		# TypeError
		with self.assertRaises(TypeError):
			COMM.leaving_match(2)

		with self.assertRaises(TypeError):
			COMM.leaving_match([])

	

if __name__ == '__main__':
	unittest.main()