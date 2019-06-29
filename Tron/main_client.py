# Client for Tron game
import sys
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron')

# IMPORT LOGGING AND MAIN FRAMEWORKS
import click # Click for command framework
import logging, coloredlogs

logger = logging.getLogger()
coloredlogs.install(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', level='DEBUG', hostname=False)

# Import dependencies
from Tron.Backend.Classes.GameClient import GameClient

if __name__ == '__main__':
	client = GameClient()
	while True:
		print("(1) Discover lobbies")
		print("(2) Enter the first lobby")

		user_in = input("Select an option: ")
		if user_in == "1":
			client.discover_lobby()
		elif user_in == "2":
			client.lobbies[0].say_hello()
	