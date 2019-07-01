import logging, coloredlogs
from Backend.Classes.Game import Game

GAME = Game()
GAME.setPlayerName("Robot -be -be")

logger = logging.getLogger()
coloredlogs.install(level='DEBUG')

from Backend.Classes.TCPCLient import TCPCLient

client = TCPCLient(GAME)
client.Connect("127.0.0.1", 9876)