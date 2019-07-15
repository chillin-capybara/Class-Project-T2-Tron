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

if __name__ == '__main__':
	client = GameClient()

	client.me.setColor((255,0,0))

	logging.info("Discovering Lobbies")
	client.discover_lobby()
	time.sleep(1)

	logging.info("Entering lobby 1")
	client.enter_lobby(0)
	time.sleep(1)

	# Create a new game
	logging.info("Creating match")
	client.lobby.create_match("Tron", "Testmatch", {'Players': 1, 'Lifes': 10})
	time.sleep(1)

	# Join  the match
	logging.info("Joining the match")
	client.lobby.list_matches('Tron')
	time.sleep(2)
	client.join_match(0)

	client.me.setVelocity(1,0)

	time.sleep(2)
	client.i_am_ready()

	# List the player colors
	pid = 1
	for player in client.match.players:
		print("Player %d has the color %s" % (pid, player.getColor()))
		print("Player %d has n   lifes %d" % (pid, player.lifes))
		pid += 1

	while True:
		# TODO Update the game matrix every second
		matrix = client.match.arena.matrix
		#draw_matrix(matrix)
		players = client.match.players
		os.system('clear')
		for player in players:
			print("PLAYER POS: %s" % str(player.getPosition()))
			print("PLAYER VEL: %s" % str(player.getVelocity()))
			print("PLAYER LIF: %s" % str(player.lifes))
