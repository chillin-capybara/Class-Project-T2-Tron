from .AbstractMatch import AbstractMatch
from .BasicComm import BasicComm
from .HumanPlayer import HumanPlayer
from ..Core.matrix import getActPos
from ..Core.matrix_splitter import MatrixSplitter
from ..Core.Hook import Hook
from ..Core.globals import *
from ..Core.ThreadCollection import ThreadCollection
from typing import List
import logging
import socket
import time
import threading

SPLITTER = MatrixSplitter()

class MatchClient(AbstractMatch):

	__comm: BasicComm = None
	__recv_dict: dict = None

	__current_matrix_seq: int = 0      # Currently received packet sequence number
	__recv_seq_start: int     = None
	__player_id: int = 0

	__last_direction_seq: int = 0
	__current_seq: int = 0
	__clientsock: socket.socket = None

	__hook_me: Hook = None # Hook to get the player of the client

	__threadcollection: ThreadCollection = None # Initialize a threadcollection

	def __init__(self, host: str, name: str, parent, hook_me):
		"""
		Initialize a new instanc of MatchClient with the match parameter

		Args:
			host (str): IP address of the server host
			name (str): Name of the match
			parent ([type]): Parent object of the instance (Lobby)
		"""
		self.__parent__ = parent

		self.__recv_dict = {}

		# Initialize comm protocol & Attach event handlers
		self.__comm = BasicComm()
		self.__comm.EUpdateField += self.handle_update_field

		# Set a hook to the current player
		self.__hook_me = hook_me

		self.__parent__ = parent

		self.__threadcollection = ThreadCollection()

		super().__init__(host, name, MATCH_DEFAULT_FEATURES) # Initialzie a default match

	@property
	def player_id(self) ->int:
		"""
		Player ID of the current player on the server
		"""
		return self.__player_id

	def set_port(self, port:int):
		"""
		Set the port of the match when the match is started

		Args:
			port (int): Port of the match (for UDP)
		"""
		self._port = port

	def set_features(self, features: List[str]):
		"""
		Set the features of the match from a feature query in the lobby

		Args:
			features (List[str]): List of features as a string list
		"""
		self._feat_players = self.get_feature_value_int('Players', features)
		self._feat_lifes   = self.get_feature_value_int('lifes', features)

		try:
			# Try to set the feature slots
			self._feat_slots = self.get_feature_value_int('Slots', features)
		except:
			pass

	def set_current_player_id(self, pid:int):
		"""
		Set the player ID of the current player to the ID the server gives

		Args:
			pid (int): Server distributed player ID
		"""
		self.__player_id = pid
	
	def open(self):
		"""
		Connect to a new match as a client, which is already joined
		"""
		logging.info("Starting Match Client to match %s on %s at port %d" % (self.name, self.host, self.port))
		senderthread = threading.Thread(target=self.__sender_thread)
		receiverthread = threading.Thread(target=self.__receiver_thread)

		# Append the threads to the collection
		self.__threadcollection += senderthread
		self.__threadcollection += receiverthread

		# Start all the threads
		self.__threadcollection.start_all()

	def close(self):
		"""
		Close the the client to the match.
		NOTE
			This destroys the sockets, and terminates all threads
		"""
		logging.info("Closing match client...")
		self.__clientsock.close()

		# Wait for all the threads to finish
		self.__threadcollection.join_all()

		logging.info("Match client successfully closed with all its threads!")

		# Call the close event
		self.EClose(self)


	def __receiver_thread(self):
		"""
		Receiver thread of the client to receive updates
		"""
		logging.info("Starting the match client thread...")
		# Create client socket
		while self.__clientsock == None: # Wait until socket OK
			pass

		while True:
			data, conn = self.__clientsock.recvfrom(UDP_RECV_BUFFER_SIZE)
			#logging.info("Received: %s" % str(data))
			dec = data.decode("UTF-8")
			seq, message = dec.split(" ", 1)
			packet = bytes(message, "UTF-8")
			self.__comm.process_response(packet)

			seq = int(seq)
			self.__current_matrix_seq = seq # Set the current sequence the client is processing
			self.__current_seq = int(seq)

		logging.info("Exiting client receiver thread")

	def __sender_thread(self):
		"""
		Sender thread for direction changes in client
		"""
		logging.info("Starting client sender thread...")
		presock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		ini = True
		while True:
			vel = self.__hook_me().getVelocity()
			packet = self.__comm.new_direction(self.__player_id, (vel.x, vel.y))
			seq = bytes("%d " % self.__last_direction_seq, "UTF-8")
			packet = seq + packet
			self.__last_direction_seq += 1
			presock.sendto(packet, (self.host, self.port))
			#logging.info("Position info updated!")
			if ini:
				self.__clientsock = presock
				ini = False
			#logging.info("NEW DIRECTION SEND!")
			time.sleep(0.01) # Send the

		logging.info("Exiting client sender thread")

	def handle_update_field(self, sender, key:tuple, matrix:list):
		"""
		Handler an update of the arena sent from the server

		Args:
			sender ([type]): [description]
			keys (tuple): [description]
			matrix (list): [description]
		"""
		if key == (1,1):
			if len(self.__recv_dict) > 0 :
				# Check if we have a complete message
				dict_len    = len(self.__recv_dict)
				awaited_len = self.__current_matrix_seq - self.__recv_seq_start

				if dict_len == awaited_len:
					# Update the arena's matrix
					#logging.info("New matrix updated!")
					# Update the track of the player
					reconstructed_matrix = SPLITTER.matrix_collapse(self.__recv_dict)

					# Update the tracks for all the players
					pid = 1
					for player in self.players:
						player.update_player_track(reconstructed_matrix,pid)
						pid +=1

					self.__hook_me().update_player_track(reconstructed_matrix, self.__player_id)
					pl_me = self.__hook_me()
					newtrack = self.__hook_me().getTrack()
					try:
						pos = getActPos(reconstructed_matrix, self.arena.matrix, self.__player_id)
						x = pos[0]
						y = pos[1]
						self.__hook_me().setPosition(x,y) # Update the client position based on the matrix
					except Exception as e:
						#logging.warning("Cannot get position diff.: %s" % str(e))
						pass
					self._arena.update_matrix(self.__recv_dict)

			self.__push_to_dict = True
			self.__recv_dict.clear() #Empty the receive buffer
			#logging.info("DICT STATUS: %s" % str(self.__recv_dict))

			self.__recv_dict[key] = matrix

			# Set the starting sequence number of the receiver
			self.__recv_seq_start = self.__current_matrix_seq
		else:
			if self.__push_to_dict:
				# Add elements with other then key (1,1)
				self.__recv_dict[key] = matrix

	def life_udpate(self, player_id:int, score:int):
		"""
		Update the life of the player with the selected player id
		
		Args:
			player_id (int): Player ID
			score (int): Lifes remaining
		Raises:
			IndexError: Player ID does not exists
			ValueError: Lifes smaller than 0
		"""
		self._players[player_id].set_lifes(score)
