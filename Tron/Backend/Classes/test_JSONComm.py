import sys
sys.path.append("/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron")

import unittest
from JSONComm import JSONComm
from CommProt import CommProt
from Tron.Backend.Classes.Factory import Factory
from Tron.Backend.Core.core_functions import get_timestamp
from Tron.Backend.Classes.Player import Player
from Tron.Backend.Classes.HumanPlayer import HumanPlayer

def bytec(string):
	return bytes(string, "UTF-8")

class TestJSONComm(unittest.TestCase):
	"""
	Test JSON Communication protocol
	"""

	def test_client_error(self):
		"""
		Test the client ready message from the JSON Communication class
		"""
		# Create comm prot instance
		comm = JSONComm()

		# Test string message
		self.assertEqual(
			comm.client_error("Test error"),
			bytec('{"type": "client_error", "message": "Test error", "timestamp": %d}' % get_timestamp())
			)
		
		# Message is empty string
		self.assertEqual(
			comm.client_error(""),
			bytec('{"type": "client_error", "message": "", "timestamp": %d}' % get_timestamp())
			)
		
		# Test Case: Message is integer
		with self.assertRaises(TypeError):
			comm.client_error(1)
		
		# Test with array
		with self.assertRaises(TypeError):
			comm.client_error([1,2,3,4])
		
		# Test with array
		with self.assertRaises(TypeError):
			comm.client_error("Teststr".encode("UTF-8"))
		
		with self.assertRaises(TypeError):
			comm.client_error(None)

	def test_server_error(self):
		"""
		Test the client ready message from the JSON Communication class
		"""
		# Create comm prot instance
		comm = JSONComm()

		# Test string message
		self.assertEqual(
			comm.server_error("Server error test"),
			bytec('{"type": "server_error", "message": "Server error test"}')
			)
		
		# Message is empty string
		self.assertEqual(
			comm.server_error(""),
			bytec('{"type": "server_error", "message": ""}')
			)
		
		# Test Case: Message is integer
		with self.assertRaises(TypeError):
			comm.server_error(1)
		
		# Test with array
		with self.assertRaises(TypeError):
			comm.server_error([1,2,3,4])
		
		# Test with array
		with self.assertRaises(TypeError):
			comm.server_error("Teststr".encode("UTF-8"))
		
		with self.assertRaises(TypeError):
			comm.server_error(None)
	
	def test_client_ready_ack(self):
		"""
		Test the client ready acknowledgement message from the server
		"""

		comm = JSONComm()
		
		# Ack with player id = 0
		self.assertEqual(
			comm.client_ready_ack(0),
			bytec('{"type": "client_ready_ack", "player_id": 0, "timestamp": %d}' % get_timestamp())
		)

		# Ack with player id = 1
		self.assertEqual(
			comm.client_ready_ack(1),
			bytec('{"type": "client_ready_ack", "player_id": 1, "timestamp": %d}' % get_timestamp())
		)

		# Client index as string
		with self.assertRaises(TypeError):
			comm.client_ready_ack("Hello")

		# Client index as string
		with self.assertRaises(TypeError):
			comm.client_ready_ack(1+5j)
		
		with self.assertRaises(TypeError):
			comm.client_ready_ack(None)
	
	def test_countdown(self):
		"""
		Test the countdown started message from the server
		"""

		comm = JSONComm()

		# Countdown with 1 sec
		self.assertEqual(
			comm.countdown(1),
			bytec('{"type": "countdown", "seconds": 1, "timestamp": %d}' % get_timestamp())
			)
		
		# Countdown with 100 sec
		self.assertEqual(
			comm.countdown(100),
			bytec('{"type": "countdown", "seconds": 100, "timestamp": %d}' % get_timestamp())
			)
		
		# Test TypeError
		with self.assertRaises(TypeError):
			comm.countdown("Countdown")

		with self.assertRaises(TypeError):
			comm.countdown(None)

		with self.assertRaises(TypeError):
			comm.countdown(1 + 5j)
		
		# Test ValueError
		with self.assertRaises(ValueError):
			comm.countdown(0)
		
		with self.assertRaises(ValueError):
			comm.countdown(-1)
		
		with self.assertRaises(TypeError): # Float gives TypeError!!!
			comm.countdown(0.99999)
		
		with self.assertRaises(ValueError):
			comm.countdown(-100)

	def test_client_ready(self):
		"""
		Test the clienat ready message.
		TODO: Wait until HumanPlayer is implemented!
		"""
		comm = JSONComm()

		# Setup a player object
		player = Factory.Player("", 0)
		player.setName("This is my playername")
		player.setColor(2)
		
		# Normal data test
		self.assertEqual(
			comm.client_ready(player),
			bytec('{"type": "client_ready", "playername": "This is my playername", "color": 2, "timestamp": %d}' % get_timestamp())
		)

		# One word name
		player.setName("Simplename")
		self.assertEqual(
			comm.client_ready(player),
			bytec('{"type": "client_ready", "playername": "Simplename", "color": 2, "timestamp": %d}' % get_timestamp())
		)

		# Empty name
		player.setName("")
		self.assertEqual(
			comm.client_ready(player),
			bytec('{"type": "client_ready", "playername": "", "color": 2, "timestamp": %d}' % get_timestamp())
		)

		# Empty name and color
		player.setName("")
		player.setColor(0)
		self.assertEqual(
			comm.client_ready(player),
			bytec('{"type": "client_ready", "playername": "", "color": 0, "timestamp": %d}' % get_timestamp())
		)

		# Validate exceptions
		with self.assertRaises(TypeError):
			comm.client_ready(1)
		
		with self.assertRaises(TypeError):
			comm.client_ready(1+2j)
		
		with self.assertRaises(TypeError):
			comm.client_ready("Camou Player")

		with self.assertRaises(TypeError):
			comm.client_ready(None)
		
	def test_exit_game(self):
		"""
		Test the exit game message
		"""
		comm: CommProt = JSONComm()

		self.assertEqual(
			comm.exit_game(),
			bytec('{"type": "exit_game", "timestamp": %d}' % get_timestamp())
		)
	
	def test_revenge(self):
		"""
		Test revenge request message
		"""
		comm: CommProt = JSONComm()

		self.assertEqual(
			comm.revenge(),
			bytec('{"type": "revenge", "timestamp": %d}' % get_timestamp())
		)
	
	def test_revenge_ack(self):
		"""
		Test revenge acknowledgement
		"""
		comm: CommProt = JSONComm()

		self.assertEqual(
			comm.revenge_ack(),
			bytec('{"type": "revenge_ack", "timestamp": %d}' % get_timestamp())
		)
	
	# TODO: Write tests for the processor functions
	def test_process_client_ready_ack(self):
		"""
		Test the client ready ack message processor.
		"""
		comm = JSONComm()
		# Test for a request with 0
		testmsg = comm.client_ready_ack(0)
		
		self.assertEqual(
			(CommProt.CLIENT_READY_ACK, 0),
			comm.process_response(testmsg)
		)

		# Test for a request with 100
		testmsg = comm.client_ready_ack(100)
		
		self.assertEqual(
			(CommProt.CLIENT_READY_ACK, 100),
			comm.process_response(testmsg)
		)

		# Test TypeError with string
		testmsg = bytec('{"type": "client_ready_ack", "player_id": "21", "timestamp": %d}' % get_timestamp())
		with self.assertRaises(TypeError):
			comm.process_response(testmsg)
		
		# Test TypeError with float
		testmsg = bytec('{"type": "client_ready_ack", "player_id": 0.987, "timestamp": %d}' % get_timestamp())
		with self.assertRaises(TypeError):
			comm.process_response(testmsg)
	
	def test_process_client_ready(self):
		"""
		Test clietn ready messaage processor
		"""
		comm = JSONComm()
		pl: Player = Factory.Player("Testname", 2)

		# Test for a request with 0
		testmsg = comm.client_ready(pl)

		# TODO: Write testing with Player object