from .BasicComm import BasicComm
from .Lobby import Lobby
from ..Core.globals import *

import logging
import socket
from typing import List

class GameClient(object):
	"""
	Main client object for Tron Game
	"""

	__comm : BasicComm = None
	__last_server : str = None
	__lobbies : List[Lobby]  = None

	def __init__(self):
		"""
		Initialize the game client.
		"""

		# Initialize the communication protocol
		self.__comm = BasicComm()

		# Initialize the list of the lobbies
		self.__lobbies = []
	
	def discover_lobby(self):
		"""
		Request the servers to list the lobbies on the network.
		"""
		try:
			logging.info("Discovering lobbies...")
			# Create socket
			sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			# Turn on the broadcast
			sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			#sockfd.bind(("", LOBBY_DISCOVERY_PORT))

			packet = self.__comm.discover_lobby()

			# Append the lobby event handler to the comm
			self.__comm.ELobby += self.handle_lobby

			# Send out the discovery packet
			sockfd.sendto(packet, ('<broadcast>', LOBBY_DISCOVERY_PORT))
			logging.debug("Discovery message sent to %s:%d" % (LOBBY_DISCOVERY_ADDR, LOBBY_DISCOVERY_PORT))
			sockfd.settimeout(LOBBY_DISCOVER_TIMEOUT) # Give 2 seconds to not receive anything

			while True:
				resp, conn = sockfd.recvfrom(LOBBY_DISCOVERY_RECV_SIZE)
				self.__last_server = conn[0] # Pass the IP adress of the server along
				self.__comm.process_response(resp) # Process the lobby discover messages
		except socket.timeout:
			logging.info("All vailable lobbies listed. Waiting time %d" % LOBBY_DISCOVER_TIMEOUT)
		except Exception as e:
			logging.error("Error occured while listing the lobbies: %s" %  str(e))
	
	def __add_lobby(self, host: str, port: int) -> None:
		"""
		Add a lobby to the list of lobbies on the server
		
		Args:
			host (str): IP adress of the lobby's server
			port (int): Port of the lobby
		"""
		self.__lobbies.append(Lobby(host, port))


	def handle_lobby(self, sender, port: int):
		"""
		Handle the lobby response from the server
		
		Args:
			sender (CommProt): self.__comm
			port (int): Port number of the lobby
		"""
		self.__add_lobby(self.__last_server, port)
		logging.debug("New lobby discovered: %s:%d" % (self.__last_server, port))




