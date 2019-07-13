from .BasicComm import BasicComm
from .Lobby import Lobby
from ..Core.globals import *
from .HumanPlayer import HumanPlayer
from .MatchClient import MatchClient
from ..Core.Event import Event

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

	__me : HumanPlayer = None
	__entered_lobby : Lobby = None

	EError : Event = None # Event to be called, when an error happens
	EMatchJoined : Event = None
	EMatchStarted : Event = None
	EMatchEnded : Event = None

	def __init__(self):
		"""
		Initialize the game client.
		"""

		# Initialize the communication protocol
		self.__comm = BasicComm()

		# Initialize the list of the lobbies
		self.__lobbies = []

		# Initialize local events
		self.EError = Event('msg')
		self.EMatchJoined = Event('matchname')
		self.EMatchStarted = Event()
		self.EMatchEnded = Event('reason')

		# Append the lobby event handler to the comm
		self.__comm.ELobby += self.handle_lobby

		# Initialize the client Player
		self.__me = HumanPlayer()
		self.__me.setName("WorkingJoe")
		self.__me.setColor((54,66,78))

	@property
	def me(self):
		"""
		Get the clien't player object
		"""
		return self.__me
	@property
	def lobbies(self) -> List[Lobby]:
		"""
		Get the list of lobbies discovered
		
		Returns:
			List[Lobby]: Lobbies discovered
		"""
		return self.__lobbies
	
	@property
	def lobby(self) -> Lobby:
		"""
		Entered lobby, when in a lobby
		"""
		return self.__entered_lobby
	
	@property
	def match(self) -> MatchClient:
		"""
		Selected match to enter
		"""
		return self.lobby.match
	
	def enter_lobby(self, index: int):
		"""
		Index of the lobby in the list of the lobbies to enter.
		
		Args:
			index (int): Index of the lobby
		"""
		# Say hello to the lobby
		self.__lobbies[index].say_hello()

		# Set the entered lobby
		self.__entered_lobby = self.__lobbies[index]

	def join_match(self, index:int):
		"""
		Join the selected match from the client
		
		Args:
			index (int): Index of the selected match
		"""
		self.lobby.join_match(index)
		

	def get_me(self):
		"""
		Hook, to get the client's player object
		"""
		return self.__me
	
	def discover_lobby(self):
		"""
		Request the servers to list the lobbies on the network.
		"""
		try:
			# Empty the list
			self.__lobbies.clear()

			logging.info("Discovering lobbies...")
			# Create socket
			sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			# Turn on the broadcast
			sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			#sockfd.bind(("", LOBBY_DISCOVERY_PORT))

			packet = self.__comm.discover_lobby()

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
		lobby = Lobby(host, port, self.get_me)
		lobby.EError += self.handle_EError # Add callback to the error handler
		lobby.EMatchJoined += self.handle_EMatchJoined # Add callback for match joins
		lobby.EMatchStarted += self.handle_match_started
		lobby.EMatchEnded += self.on_match_ended
		self.__lobbies.append(lobby)

	def handle_EError(self, sender, msg: str):
		"""
		Handle errors from the lobby objects
		
		Args:
			sender ([type]): Lobby that has error
			msg (str): Error message
		"""
		# Pass along the event
		self.EError(self, msg=msg)

	def handle_lobby(self, sender, port: int):
		"""
		Handle the lobby response from the server
		
		Args:
			sender (CommProt): self.__comm
			port (int): Port number of the lobby
		"""
		self.__add_lobby(self.__last_server, port)
		logging.debug("New lobby discovered: %s:%d" % (self.__last_server, port))
	
	def handle_EMatchJoined(self, sender, matchname: str):
		"""
		Handle the event of the Lobby, when the client can join into a match
		
		Args:
			sender ([type]): Caller of the event
			player_id (int): Player ID on the server
		"""
		logging.info("Notifying the user, that to wait for the match start.")
		self.EMatchJoined(self, matchname=matchname)
	
	def handle_match_started(self, sender):
		logging.info("Tell the UI to start the match.")
		self.EMatchStarted(self)
	
	def close(self):
		"""
		Close the game client with closing all the lobby threads
		"""
		# Close the lobby
		self.lobby.close()
	
		
	def on_match_ended(self, sender, reason):
		"""
		Handle when a match was ended by the server
		
		Args:
			sender (MatchClient): Caller of the Event
			reason (str): Reason of the match's end
		"""
		# Pass the Event along
		self.EMatchEnded(self, reason)

