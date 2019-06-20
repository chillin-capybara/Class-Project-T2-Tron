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
	
	def test_client_ingame(self):
		"""
		Test the client_ingame messages
		"""
		comm: CommProt = JSONComm()
		player = Factory.Player("Test", 1)
		
		# Test for random datasets
		self.assertEqual(
			comm.client_ingame(player),
			bytec('{"type": "client_ingame", "playername": "Test", "color": 1, "x": 0, "y": 0, "vx": 0, "vy": 0, "timestamp": %d}' % get_timestamp())
		)

		# Test for changed position
		player.setPosition(1,2)

		# Test for random datasets
		self.assertEqual(
			comm.client_ingame(player),
			bytec('{"type": "client_ingame", "playername": "Test", "color": 1, "x": 1, "y": 2, "vx": 0, "vy": 0, "timestamp": %d}' % get_timestamp())
		)

		# Test changed velocity
		player.setVelocity(8,9)
		self.assertEqual(
			comm.client_ingame(player),
			bytec('{"type": "client_ingame", "playername": "Test", "color": 1, "x": 1, "y": 2, "vx": 8, "vy": 9, "timestamp": %d}' % get_timestamp())
		)

		# Check for exceptions
		with self.assertRaises(TypeError):
			comm.client_ingame(1)

		# Check for exceptions
		with self.assertRaises(TypeError):
			comm.client_ingame("Stringy")
		
		# Check for exceptions
		with self.assertRaises(TypeError):
			comm.client_ingame(None)

	
	def test_process_client_ready(self):
		"""
		Test the client ready message processor
		"""
		comm = JSONComm()
		player = Factory.Player("Test", 1)

		# Test for a request for SAMPLE DATA
		testmsg = comm.client_ready(player)
		self.assertEqual(
			comm.process_response(testmsg),
			(comm.CLIENT_READY, player)
		)

		# Test for a request for Sample DATA
		player.setName("Artem")
		player.setColor(2)
		testmsg = comm.client_ready(player)
		self.assertEqual(
			comm.process_response(testmsg),
			(comm.CLIENT_READY, player)
		)


		# Test for a Changed Player
		testmsg = comm.client_ready(player)
		player.setName("Marcell")
		player.setColor(1)
		self.assertEqual(
			comm.process_response(testmsg)[0],
			CommProt.CLIENT_READY # CHECK IF THE TYPE IS CORRECT
		)
		self.assertNotEqual(
			comm.process_response(testmsg)[1], # CHECK IF PLAYER IS CHANGED
			player
		)

		# Check for other types
		self.assertNotEqual(
			comm.process_response(testmsg)[1], # CHECK IF PLAYER IS CHANGED
			"Hello"
		)

		self.assertNotEqual(
			comm.process_response(testmsg)[1], # CHECK IF PLAYER IS CHANGED
			0
		)

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
	
	def test_process_client_error(self):
		"""
		Test the client error message processor
		"""
		comm = JSONComm()

		# Empty string
		msg = comm.client_error("")
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.CLIENT_ERROR, "")
		)

		# Empty string
		msg = comm.client_error("Test Error Message")
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.CLIENT_ERROR, "Test Error Message")
		)

		# Test inequality
		msg = comm.client_error("Test Error Message")
		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.CLIENT_ERROR, "")
		)

		msg = comm.client_error("")
		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.CLIENT_ERROR, "X")
		)
	
	def test_process_server_error(self):
		"""
		Test the server error message processor
		"""
		comm = JSONComm()

		# Empty string
		msg = comm.server_error("")
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.SERVER_ERROR, "")
		)

		# Empty string
		msg = comm.server_error("Test Error Message")
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.SERVER_ERROR, "Test Error Message")
		)

		# Test inequality
		msg = comm.server_error("Test Error Message")
		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.SERVER_ERROR, "")
		)

		msg = comm.server_error("")
		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.SERVER_ERROR, "X")
		)

	def test_process_countdown(self):
		"""
		Test the countdown message processor
		"""
		comm = JSONComm()

		msg = comm.countdown(1)
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.COUNTDOWN, 1)
		)

		msg = comm.countdown(100)
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.COUNTDOWN, 100)
		)

		# Test for invalid value
		with self.assertRaises(ValueError):
			comm.process_response(bytec('{"type": "countdown", "seconds": 0, "timestamp": %d}' % get_timestamp()))

		# Test for invalid Type
		with self.assertRaises(TypeError):
			comm.process_response(bytec('{"type": "countdown", "seconds": "Hello", "timestamp": %d}' % get_timestamp()))
		
		# Test for invalid value
		with self.assertRaises(ValueError):
			comm.process_response(bytec('{"type": "countdown", "seconds": -1, "timestamp": %d}' % get_timestamp()))

	def test_process_revenge(self):
		"""
		Test the processing of a revenge request
		"""
		comm = JSONComm()

		msg = comm.revenge()
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.REVENGE, True)
		)

		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.REVENGE, False)
		)
	
	def test_process_revenge_ack(self):
		"""
		Test the processing of the revenge request 
		"""
		comm = JSONComm()

		msg = comm.revenge_ack()
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.REVENGE_ACK, True)
		)

		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.REVENGE_ACK, False)
		)
	
	def test_process_exit_game(self):
		"""
		Test the processing of exit game request
		"""
		comm = JSONComm()

		msg = comm.exit_game()
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.EXIT_GAME, True)
		)
		self.assertNotEqual(
			comm.process_response(msg),
			(CommProt.REVENGE_ACK, False)
		)
	
	def test_process_client_ingame(self):
		"""
		Test the processing of a client ingame message
		"""
		comm = JSONComm()
		pla : HumanPlayer = Factory.Player("Test", 1)
		pla.setPosition(1,1)
		pla.setVelocity(2,2)

		# RANDOM DATA
		msg = comm.client_ingame(pla)
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.CLIENT_INGAME, pla)
		)
		

		pla = Factory.Player("Test", 1)
		pla.setPosition(-1,-20)
		pla.setVelocity(10,-3)

		# RANDOM DATA
		msg = comm.client_ingame(pla)
		self.assertEqual(
			comm.process_response(msg),
			(CommProt.CLIENT_INGAME, pla)
		)

		pla = Factory.Player("Test", 1)
		pla.setPosition(-1,-20)
		msg = comm.client_ingame(pla)

		pla.setPosition(10,-3)


		# RANDOM DATA NOT EQUAL
		self.assertFalse(
			pla == comm.process_response(msg)[1]
		)