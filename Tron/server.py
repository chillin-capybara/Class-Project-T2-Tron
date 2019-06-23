# Server for Tron game

# IMPORT LOGGING AND MAIN FRAMEWORKS
import click # Click for command framework
import logging, coloredlogs

logger = logging.getLogger()
coloredlogs.install(level='DEBUG')

# IMPORT GAME
from Backend.Classes.TCPServer import TCPServer

@click.command()
@click.option('--ip', help="IP address to listen on", default="")
@click.option('--port', help="Port to listen on", default=23)
def main(ip, port):
	"""
	Start a Tron Game Server on this local machine by defining
	the server properties via command line
	"""
	logging.error("This is a debug message")
	click.pause()

if __name__ == '__main__':
	main()
