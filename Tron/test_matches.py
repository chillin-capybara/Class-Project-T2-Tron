# Client for Tron game
import sys
import os
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron')

# IMPORT LOGGING AND MAIN FRAMEWORKS
import click # Click for command framework
import logging, coloredlogs
import time

logger = logging.getLogger()
coloredlogs.install(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', level='DEBUG', hostname=False)

# Import dependencies
from Tron.Backend.Classes.GameClient import GameClient

def draw_matrix(matrix):
	os.system('clear')
	linestr = ""
	for row in matrix:
		for col in row:
			linestr += "%d " % col
		print(linestr, flush=True)
		linestr = ""

def on_matches_update(sender, matches):
	"""
	Print out the newly updated matches
	"""
	os.system('clear')
	print("%s \t\t\t %s" % ("Matchname", "Features"))
	# Print out the list of matches
	for match in matches:
		print("%s \t\t %s" % (match.name, match.get_feature_string()))

	print("")
	print("Last update: %d" % time.perf_counter())


if __name__ == '__main__':
	client = GameClient()

	client.me.setColor((255,0,0))
	# Attach the event handler
	client.OnMatchesUpdate += on_matches_update

	logging.info("Discovering Lobbies")
	client.discover_lobby()
	time.sleep(1)

	logging.info("Entering lobby 1")
	client.enter_lobby(0)
	time.sleep(1)

	# Create a new game
	logging.info("Creating match")
	client.lobby.create_match("Tron", "Testmatch", {'Players': 1, 'Lifes': 10})
	time.sleep(0.1)

	# Create a new game
	logging.info("Creating match")
	client.lobby.create_match("Tron", "TM2", {'Players': 4, 'Lifes': 29})
	time.sleep(0.1)

	# Create a new game
	logging.info("Creating match")
	client.lobby.create_match("Tron", "Test3", {'Players': 9, 'Lifes': 2})
	time.sleep(0.1)

	while True:
		# Join  the match
		logging.info("Joining the match")
		client.lobby.list_matches('Tron')
		time.sleep(5)
