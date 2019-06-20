# Server for Tron game

# IMPORT LOGGING AND MAIN FRAMEWORKS
import click # Click for command framework
import logging, coloredlogs

logger = logging.getLogger()
coloredlogs.install(level='DEBUG')

# IMPORT GAME
from Backend.Classes.TCPServer import TCPServer


def main(ip, port, player_nr):
	"""
	Start a Tron Game Server on this local machine by defining
	the server properties via command line
	"""
	logging.info("Intializing server...")

	# Configure TCP Server
	server = TCPServer(host=ip, port=port)
	server.setPlayerNumber(player_nr)

	server.Start()

if __name__ == '__main__':
	main("", 9877, 2)
