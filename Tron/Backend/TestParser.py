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



		pass



if __name__ == '__main__':
	unittest.main()