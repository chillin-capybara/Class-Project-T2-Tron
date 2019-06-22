import logging, coloredlogs

logger = logging.getLogger()
coloredlogs.install(level='DEBUG')

from Backend.Classes.TCPCLient import TCPCLient

client = TCPCLient()
client.Connect("127.0.0.1", 9877)
client.Start()


