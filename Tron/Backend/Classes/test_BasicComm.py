# brief:  Unit tests for Basic Comm Protocol
# author: Marcell Pigniczki (marcell.pigniczki@tum.de)

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

	def test_process_failed_to_join(self):
		"""
		Test the processing of a failed to join message
		"""
		# Sample data 1
		packet = COMM.failed_to_join("This is the reason...")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "Failed to join the game. Reason: %s" % "This is the reason...")

		# Sample data 2
		packet = COMM.failed_to_join("Reason2")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "Failed to join the game. Reason: %s" % "Reason2")

	def test_process_game_not_exists(self):
		"""
		Test the processing of a game not exists error message
		"""
		# Sample data 1
		packet = COMM.game_not_exists("Mygame 1")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "The game you want to join does not exist: Mygame 1")

		# Sample data 2
		packet = COMM.game_not_exists("GameofGames")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "The game you want to join does not exist: GameofGames")
	
	def test_process_disconnecting_client(self):
		"""
		Test the processing of a disconnecting you message
		"""
		# Sample data 1
		packet = COMM.disconnect_client("This is the reason...")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "You were disconnected by the server. Reason: %s" % "This is the reason...")

		# Sample data 2
		packet = COMM.disconnect_client("Reason2")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.SERVER_ERROR)
		self.assertEqual(message, "You were disconnected by the server. Reason: %s" % "Reason2")
	
	def test_process_leaving_match(self):
		"""
		Test the processing of a leaving match message
		"""
		# Sample data 1
		packet = COMM.leaving_match("This is the reason...")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.EXIT_GAME)
		self.assertEqual(message, "Client is leaving the match. Reason: %s" % "This is the reason...")

		# Sample data 2
		packet = COMM.leaving_match("Reason2")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.EXIT_GAME)
		self.assertEqual(message, "Client is leaving the match. Reason: %s" % "Reason2")
	
	def test_game_ended(self):
		"""
		Test the message generation of game ended message
		"""
		# Sample data 1
		reason = "Just because"
		packet = COMM.game_ended(reason)
		original = utf8("GAME_ENDED Just because")
		self.assertEqual(packet, original)

		# Sample data 2
		reason = "This is the reason 2"
		packet = COMM.game_ended(reason)
		original = utf8("GAME_ENDED This is the reason 2")
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
	
	def test_process_game_ended(self):
		"""
		Test the game ended message processor
		"""
		# Sample data 1
		packet = COMM.game_ended("This is the reason...")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.GAME_ENDED)
		self.assertEqual(message, "Game ended! Reason: %s" % "This is the reason...")

		# Sample data 2
		packet = COMM.game_ended("Reason2")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.GAME_ENDED)
		self.assertEqual(message, "Game ended! Reason: %s" % "Reason2")
	
	def test_discover_lobby(self):
		"""
		Test the discover lobby message
		"""
		packet = COMM.discover_lobby()
		self.assertEqual(packet, utf8("DISCOVER_LOBBY"))
	
	def test_process_discover_lobby(self):
		"""
		Test the discover lobby processor
		"""
		# Reset event call counter
		COMM.EDiscoverLobby.reset_called()

		packet = COMM.discover_lobby()
		mtype, mess = COMM.process_response(packet)

		# Check the correct type
		self.assertEqual(
			mtype,
			COMM.DISCOVER_LOBBY
		)

		# Check the correct message
		self.assertEqual(
			mess,
			"DISCOVER_LOBBY"
		)

		# Check if the event was called
		self.assertTrue(COMM.EDiscoverLobby.was_called())
	
	def test_lobby(self):
		"""
		Test the lobby message
		"""

		# Test a random port
		packet = COMM.lobby(54053)
		self.assertEqual(
			packet,
			utf8("LOBBY 54053")
		)


		# Test the last port in range
		packet = COMM.lobby(54100)
		self.assertEqual(
			packet,
			utf8("LOBBY 54100")
		)

		# Test invalid port range
		with self.assertRaises(ValueError):
			COMM.lobby(54009)
		with self.assertRaises(ValueError):
			COMM.lobby(54101)

		# Test invalid port type
		with self.assertRaises(TypeError):
			COMM.lobby("54101")
		
		with self.assertRaises(TypeError):
			COMM.lobby(True)
		
		with self.assertRaises(TypeError):
			COMM.lobby(False)

		with self.assertRaises(TypeError):
			COMM.lobby([])
	
	def test_process_lobby(self):
		"""
		Test the lobby message processing
		"""
		COMM.ELobby.reset_called()
		packet = COMM.lobby(54053)
		mtype, mport = COMM.process_response(packet)

		self.assertEqual(mtype, COMM.LOBBY)
		self.assertEqual(mport, 54053)
		self.assertTrue(COMM.ELobby.was_called())

		COMM.ELobby.reset_called()
		packet = COMM.lobby(54100)
		mtype, mport = COMM.process_response(packet)

		self.assertEqual(mtype, COMM.LOBBY)
		self.assertEqual(mport, 54100)
		self.assertTrue(COMM.ELobby.was_called())
	
	def test_list_game(self):
		"""
		Test the list games command
		"""
		# Static text test
		packet = COMM.list_games()
		self.assertEqual(
			packet,
			utf8("LIST_GAMES")
		)
	
	def test_process_list_game(self):
		"""
		Test the processing of a list games command
		"""

		COMM.EListGames.reset_called() # Reset event flag
		packet = COMM.list_games()
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.LIST_GAMES)
		self.assertEqual(message, "LIST_GAMES")
		self.assertTrue(COMM.EListGames.was_called())
	
	def test_available_games(self):
		"""
		Test the generation of available games command message.
		NOTE:
			This implementation only supports Tron
		"""
		packet = COMM.available_games(['Tron'])
		self.assertEqual(
			packet,
			utf8("AVAILABLE_GAMES Tron")
		)
	
	def __test_process_available_games(self):
		"""
		Test the message processing of available games
		"""
		COMM.EAvailableGames.reset_called()
		packet = COMM.available_games()
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.AVAILABLE_GAMES)
		self.assertEqual(message, ['Tron'])
		self.assertTrue(COMM.EAvailableGames.was_called())

		COMM.EAvailableGames.reset_called()
		packet = utf8("AVAILABLE_GAMES Tron,Pong")
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.AVAILABLE_GAMES)
		self.assertEqual(message, ['Tron', 'Pong'])
		self.assertTrue(COMM.EAvailableGames.was_called())

	def test_hello(self):
		"""
		Test the hello message
		"""
		# Sampel Data 1
		PLAYER.setName("WorkingJoe")
		packet = COMM.hello(PLAYER, ['BASIC'])
		self.assertEqual(
			packet,
			utf8("HELLO WorkingJoe BASIC")
		)

		# SAMPLE DATA 2
		PLAYER.setName("Vlad")
		packet = COMM.hello(PLAYER, ['BASIC', 'COOLStuff', 'MStuff'])
		self.assertEqual(
			packet,
			utf8("HELLO Vlad BASIC,COOLStuff,MStuff")
		)

	def test_process_hello(self):
		"""
		Test the processing of the hello message
		"""
		# Sampel Data 1
		COMM.EHello.reset_called()
		PLAYER.setName("WorkingJoe")
		packet = COMM.hello(PLAYER, ['BASIC'])
		mtype, playername, features = COMM.process_response(packet)
		self.assertEqual(
			mtype,
			COMM.HELLO
		)
		self.assertEqual(playername, "WorkingJoe")
		self.assertEqual(features, ['BASIC'])
		self.assertTrue(COMM.EHello.was_called())


		# Sample data 2: 2 features
		COMM.EHello.reset_called()
		PLAYER.setName("WorkingJoe")
		packet = COMM.hello(PLAYER, ['BASIC', 'DIMS', 10,10,50,50])
		mtype, playername, features = COMM.process_response(packet)
		self.assertEqual(
			mtype,
			COMM.HELLO
		)
		self.assertEqual(playername, "WorkingJoe")
		self.assertEqual(features, ['BASIC', 'DIMS', '10', '10', '50', '50']) # Numbers come back as string
		self.assertTrue(COMM.EHello.was_called())

	
	def test_welcome(self):
		"""
		Test the welcome message generation from the server
		"""
		# Only 1 feature
		packet = COMM.welcome(['BASIC'])
		self.assertEqual(
			packet,
			utf8("WELCOME BASIC")
		)

		# DIMS feature
		packet = COMM.welcome(['BASIC', 'DIMS', 10, 10, 50, 50])
		self.assertEqual(
			packet,
			utf8("WELCOME BASIC,DIMS,10,10,50,50")
		)
	
	def test_process_welcome(self):
		"""
		Test the welcome message processor
		"""
		# Test with 1 feature
		COMM.EWelcome.reset_called()
		packet = COMM.welcome(['BASIC'])
		mtype, features = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.WELCOME)
		self.assertEqual(features, ['BASIC'])
		self.assertTrue(COMM.EWelcome.was_called())

		# Test with 1 (DIMS) feature
		COMM.EWelcome.reset_called()
		packet = COMM.welcome(['BASIC', 'DIMS', 10, 10, 50, 50])
		mtype, features = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.WELCOME)
		self.assertEqual(features, ['BASIC', 'DIMS', '10', '10', '50', '50'])
		self.assertTrue(COMM.EWelcome.was_called())
	
	def test_create_match(self):
		"""
		Test the create match command messages
		"""
		packet = COMM.create_match('Tron', 'game1', ['Players,4,Lifes,3'])
		self.assertEqual(
			packet,
			utf8("CREATE_MATCH Tron game1 Players,4,Lifes,3")
		)

		packet = COMM.create_match('Tron', 'awsomeee', ['Players,1'])
		self.assertEqual(
			packet,
			utf8("CREATE_MATCH Tron awsomeee Players,1")
		)
	
	def test_match_created(self):
		"""
		Test the match created message
		"""
		packet = COMM.match_created()
		self.assertEqual(
			packet,
			utf8("MATCH_CREATED")
		)
	
	def test_list_matches(self):
		"""
		Test the list matches command
		"""
		packet = COMM.list_matches('Tron')
		self.assertEqual(
			packet,
			utf8("LIST_MATCHES Tron")
		)

		packet = COMM.list_matches('Pong')
		self.assertEqual(
			packet,
			utf8("LIST_MATCHES Pong")
		)

		with self.assertRaises(ValueError):
			COMM.list_matches("")
		
		with self.assertRaises(TypeError):
			COMM.list_matches(0)
		
		with self.assertRaises(TypeError):
			COMM.list_matches([])
	
	def  test_games(self):
		"""
		Test the listing of matches
		// TODO  add more tests, exception testing
		"""

		packet = COMM.games('Tron', ['game1', 'game2'])
		self.assertEqual(
			packet,
			utf8("GAMES Tron game1,game2")
		)
	
	def test_match_features(self):
		"""
		Test the match features query message
		"""

		packet = COMM.match_features('Tron')
		self.assertEqual(
			packet,
			utf8("MATCH_FEATURES Tron")
		)

		packet = COMM.match_features('Pong')
		self.assertEqual(
			packet,
			utf8("MATCH_FEATURES Pong")
		)

		# Typeerrors
		with self.assertRaises(TypeError):
			COMM.match_features(0)
		with self.assertRaises(TypeError):
			COMM.match_features([])
		with self.assertRaises(TypeError):
			COMM.match_features(True)
		
		# Value Errors
		with self.assertRaises(ValueError):
			COMM.match_features("")
	
	def test_match(self):
		"""
		Test the MATCH message with listing the match features
		"""
		packet = COMM.match('Tron', 'game1', ['Players',4])
		self.assertEqual(
			packet,
			utf8("MATCH Tron game1 Players,4")
		)

		packet = COMM.match('Tron', 'game1', ['Players',4,'Lifes',2])
		self.assertEqual(
			packet,
			utf8("MATCH Tron game1 Players,4,Lifes,2")
		)
	
	def test_match_started(self):
		"""
		Test the MATCH_STARTED message generation.
		// TODO make more test cases
		"""
		# Just 1 sample data
		p1 = HumanPlayer()
		p1.setColor((1,1,1))
		p2 = HumanPlayer()
		p2.setColor((2,2,2))
		p3 = HumanPlayer()
		p3.setColor((3,3,3))
		packet = COMM.match_started(50400, [0,1,2], [p1, p2, p3])
		self.assertEqual(
			packet,
			utf8("MATCH_STARTED 50400 0,1,1,1,1,2,2,2,2,3,3,3")
		)
	
	def test_process_create_match(self):
		"""
		Test the process create match function
		"""
		# Test with 2 features
		COMM.ECreateMatch.reset_called()
		packet = COMM.create_match('Tron', 'game1', ['Players',4,'Lifes',3])
		mtype, mgame, mname, mfeatures = COMM.process_response(packet)

		self.assertEqual(mtype, COMM.CREATE_MATCH)
		self.assertEqual(mgame, 'Tron')
		self.assertEqual(mname, 'game1')
		self.assertEqual(mfeatures, ['Players','4','Lifes','3'])
		self.assertTrue(COMM.ECreateMatch.was_called())

		# Test with 1 feature
		COMM.ECreateMatch.reset_called()
		packet = COMM.create_match('Pong', 'gamep', ['Players',2])
		mtype, mgame, mname, mfeatures = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.CREATE_MATCH)
		self.assertEqual(mgame, 'Pong')
		self.assertEqual(mname, 'gamep')
		self.assertEqual(mfeatures, ['Players','2'])
		self.assertTrue(COMM.ECreateMatch.was_called())

	def test_process_match_created(self):
		"""
		Test the match_created ack processing
		"""
		COMM.EMatchCreated.reset_called()
		packet = COMM.match_created()
		mtype, message = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.MATCH_CREATED)
		self.assertEqual(message, "MATCH_CREATED")
		self.assertTrue(COMM.EMatchCreated.was_called())
	
	def test_process_list_matches(self):
		"""
		Test the processing of a list matches request
		"""

		COMM.EListMatches.reset_called()
		packet = COMM.list_matches('Tron')
		mtype, mgame = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.LIST_MATCHES)
		self.assertEqual(mgame, 'Tron')
		self.assertTrue(COMM.EListGames.was_called())

		COMM.EListMatches.reset_called()
		packet = COMM.list_matches('LongerTestgamename')
		mtype, mgame = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.LIST_MATCHES)
		self.assertEqual(mgame, 'LongerTestgamename')
		self.assertTrue(COMM.EListGames.was_called())
	
	def test_process_games(self):
		"""
		Test the games message processor
		"""
		# Sample data 1
		COMM.EGames.reset_called()
		packet = COMM.games('Tron', ['New', 'Old', 'Three'])
		mtype, mgame, mlist = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.GAMES)
		self.assertEqual(mgame, 'Tron')
		self.assertEqual(mlist, ['New', 'Old', 'Three'])
		self.assertTrue(COMM.EGames.was_called())

		# Sample Data 2
		COMM.EGames.reset_called()
		packet = COMM.games('Pong', ['New'])
		mtype, mgame, mlist = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.GAMES)
		self.assertEqual(mgame, 'Pong')
		self.assertEqual(mlist, ['New'])
		self.assertTrue(COMM.EGames.was_called())
	
	def test_process_match_features(self):
		"""
		Test the match features message processor
		"""
		COMM.EMatchFeatures.reset_called()
		packet = COMM.match_features('game1')
		mtype, game = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.MATCH_FEATURES)
		self.assertEqual(game, 'game1')
		self.assertTrue(COMM.EMatchFeatures.was_called())

		COMM.EMatchFeatures.reset_called()
		packet = COMM.match_features('RandomGame')
		mtype, game = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.MATCH_FEATURES)
		self.assertEqual(game, 'RandomGame')
		self.assertTrue(COMM.EMatchFeatures.was_called())
	
	def test_process_match(self):
		"""
		Test process MATCH messages
		"""
		COMM.EMatch.reset_called()
		packet = COMM.match('Tron', 'game1', ['Players',3,'Lifes',5])
		mtype, mgame, mname, mfeatures = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.MATCH)
		self.assertEqual(mgame, 'Tron')
		self.assertEqual(mname, 'game1')
		self.assertEqual(mfeatures, ['Players','3','Lifes','5'])
		self.assertTrue(COMM.EMatch.was_called())

		COMM.EMatch.reset_called()
		packet = COMM.match('Pong', 'gp', ['Players',2])
		mtype, mgame, mname, mfeatures = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.MATCH)
		self.assertEqual(mgame, 'Pong')
		self.assertEqual(mname, 'gp')
		self.assertEqual(mfeatures, ['Players','2'])
		self.assertTrue(COMM.EMatch.was_called())

	def test_process_match_started(self):
		"""
		Test the processing of a match started message.
		"""
		p1 = HumanPlayer()
		p1.setColor((50,50,50))
		p2 = HumanPlayer()
		p2.setColor((99,99,99))
		COMM.EMatchStarted.reset_called()
		packet = COMM.match_started(50449, [0,1], [p1,p2])
		mtype, mport, lists = COMM.process_response(packet)
		self.assertEqual(mtype, COMM.MATCH_STARTED)
		self.assertEqual(mport, 50449)
		self.assertEqual(lists, [(0,50,50,50), (1,99,99,99)])
		self.assertTrue(COMM.EMatchStarted.was_called())
	
if __name__ == '__main__':
	unittest.main()