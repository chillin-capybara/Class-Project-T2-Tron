# Server for Tron game

# IMPORT LOGGING AND MAIN FRAMEWORKS
import click # Click for command framework
import logging, coloredlogs

logger = logging.getLogger()
coloredlogs.install(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s', level='DEBUG', hostname=False)

# Import dependencies
from Backend.Classes.GameServer import GameServer

if __name__ == "__main__":
	server = GameServer(1, (20,20)) # With 5 lobbies
	server.Start(loop = True)
