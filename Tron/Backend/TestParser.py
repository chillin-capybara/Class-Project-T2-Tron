import unittest
from parser import parser


class TestParser(unittest.TestCase):
	"""
	"""
	def test_parser (self):

		# WIN
		msg = "you win bloody beetroot 345 %%% hohoho"
		player_name = "CyberJet300"
		self.assertEqual(parser(msg, player_name), 1)

		msg = "you WiN bloody beetroot 345 %%% hohoho"
		self.assertEqual(parser(msg, player_name), 1)

		msg = "you WIN bloody beetroot 345 %%% hohoho"
		self.assertEqual(parser(msg, player_name), 1)

		msg = "you WIN, bloody beetroot 345 %%% hohoho"
		self.assertEqual(parser(msg, player_name), 1)

		msg = "you bloody beetroot 345 %%% hohoho champion motherfucker"
		self.assertEqual(parser(msg, player_name), 1)

		# not loose
		msg = "you are bloody beetroot 345 %%% hohoho motherfucker not died"
		self.assertEqual(parser(msg, player_name), 1)



		# LOOSE
		msg = "you DIE bloody beetroot 345 %%% hohoho"
		self.assertEqual(parser(msg, player_name), -1)

		msg = "lOOse, shit"
		self.assertEqual(parser(msg, player_name), -1)

		msg = "you are died shit"
		self.assertEqual(parser(msg, player_name), -1)

		msg = "you are not winner, shit"
		self.assertEqual(parser(msg, player_name), -1)

		msg = "NOt winner, not not shit"
		self.assertEqual(parser(msg, player_name), -1)

		msg = "you are nO champion, sir"
		self.assertEqual(parser(msg, player_name), -1)

		# ANYTHING ELSE
		msg = "pretfsdf fsdfdsf fdsfsdf fsdfsf pretty 3232 00"
		self.assertEqual(parser(msg, player_name), 0)

		# Test wins
		self.assertEqual(parser("Marcell wins", "marcell"), 1)
		self.assertEqual(parser("You won", "marcell"), 1)
		self.assertEqual(parser("marcell is the best", "marcell"), 1)
		self.assertEqual(parser("marcell is the champion", "marcell"), 1)
		self.assertEqual(parser("marcell is the winner", "marcell"), 1)
		self.assertEqual(parser("You are the winner", "marcell"), 1)
	
	def test_loose_cases(self):
		self.assertEqual(parser("You are a looser", "marcell"), -1)
		self.assertEqual(parser("You lost", "marcell"), -1)
		self.assertEqual(parser("You have lost", "marcell"), -1)
		# self.assertEqual(parser("You've lost", "marcell"), -1)
		self.assertEqual(parser("Marcell lost", "marcell"), -1)
		self.assertEqual(parser("Marcell is a looser", "marcell"), -1)
		self.assertEqual(parser("Marcell lost the game", "marcell"), -1)
		self.assertEqual(parser("Marcell was the worst", "marcell"), -1)
		self.assertEqual(parser("Marcell died", "marcell"), -1)
		self.assertEqual(parser("Marcell is dead", "marcell"), -1)
		self.assertEqual(parser("You are dead", "marcell"), -1)
		self.assertEqual(parser("You have no more lifes", "marcell"), -1)
		self.assertEqual(parser("0 lifes left", "marcell"), -1)




		pass
	
	def test_parser_exceptions(self):
		with self.assertRaises(ValueError):
			parser("asdasd", "")

		with self.assertRaises(ValueError):
			parser("", "asdasd")



if __name__ == '__main__':
	unittest.main()