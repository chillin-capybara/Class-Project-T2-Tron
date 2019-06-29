import threading
import socket
import logging
from .BasicComm import BasicComm
from .Lobby import Lobby
from ..Core.Event import Event
from ..Core.Hook import Hook
from ..Core.globals import *

class Broadcaster(object):
	"""
	Broadcaster for Lobby advertising and Discovery
	"""

	__comm : BasicComm = None
	__host : str = ""
	__port : int = LOBBY_DISCOVERY_PORT
	__resp_to = None # Adress of the connection to respond, to
	__sockfd : socket.socket = None
	__hook_lobbies : Hook = None
	__thread : threading.Thread = None

	def __init__(self, hook_lobbies):
		"""
		Initialize a Broadcaster to the server.
		Details:
			Setup threads and request-response policites
		"""

		# Initialize Communication Protocoll
		self.__comm = BasicComm()

		# Attach event handlers
		self.__comm.EDiscoverLobby += self.handle_discover_lobby

		# Create Hook to get the list of lobbies
		self.__hook_lobbies = Hook()
		self.__hook_lobbies.delegate(hook_lobbies)

		# Setup the thread
		self.__thread = threading.Thread(target=self.__thread_handler)


	def Start(self, host: str = "", port:int = LOBBY_DISCOVERY_PORT):
		"""
		Start the lobby discovery thread.
		
		Args:
			host (str, optional): IP Adress of the host adapter. Defaults to "".
			port (int, optional): Port number of the discovery port. Defaults to LOBBY_DISCOVERY_PORT.
		Raises:
			TypeError:  Invalid argument parameters
			ValueError: Invalid port range
		"""
		if type(host) is not str:
			raise TypeError
		if type(port) is not int:
			raise TypeError
		
		# Start the thread
		self.__thread.start()
	
	def Stop(self):
		"""
		Stop the discovery broadcaster.
		NOTE:
			Closing the socket causes the thread to close.
		"""
		# Close the socket
		self.__sockfd.close()
	
	def __thread_handler(self):
		"""
		Thread body function for the lobby discovery protocol
		"""

		try:
			logging.info("Starting lobby discovery broadcaster on port %d..." % self.__port)
			# Setup an UDP Server socket
			self.__sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

			while True:
				# Receive a discovery request
				packet, conn = self.__sockfd.recvfrom(LOBBY_DISCOVERY_RECV_SIZE)
				self.__resp_to = conn

				try:
					self.__comm.process_response(packet)
				except Exception as e:
					logging.warning(str(e))
					logging.warning('Invalid message received: %s' % (str(packet)))
		except Exception as e:
			# Error occured
			logging.error("The discovery protocol aborted. Reason: %s" % str(e))

		logging.info("Lobby discovery broadcaster stopped!")

	
	def handle_discover_lobby(self, sender):
		"""
		Handler the EDiscoverLobby Event.
		Reply to the client and log actions.
		
		Args:
			sender ([type]): self.__comm
		"""
		try:
			# Send back the response: For every lobby
			for lobby in self.__hook_lobbies():
				lobby : Lobby
				resp = self.__comm.lobby(lobby.port)

				self.__sockfd.sendto(resp, self.__resp_to)
		except Exception as e:
			# Log errors
			logging.error("Error sending a discovery response. Reason: %s" % str(e))
