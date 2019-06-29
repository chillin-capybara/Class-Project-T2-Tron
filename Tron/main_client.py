# Server for Tron game

# IMPORT LOGGING AND MAIN FRAMEWORKS
import click # Click for command framework
import logging, coloredlogs

logger = logging.getLogger()
coloredlogs.install(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', level='DEBUG', hostname=False)

# Import dependencies
from Backend.Classes.GameClient import GameClient

if __name__ == '__main__':
	client = GameClient()
	while True:
		print("(1) Discover lobbies")

		user_in = input("Select an option: ")
		if user_in == "1":
			client.discover_lobby()
	