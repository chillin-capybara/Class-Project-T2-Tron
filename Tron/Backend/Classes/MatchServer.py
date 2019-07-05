from .AbstractMatch import AbstractMatch
from .HumanPlayer import HumanPlayer
from .Broadcaster import BasicComm
from ..Core.leasable_collections import LeasableObject, LeasableList, LeaseError
from typing import List
from ..Core.Exceptions import ServerError
from ..Core.ThreadCollection import ThreadCollection
from .BasicComm import BasicComm
import logging

class MatchServer(AbstractMatch):
	"""
	Server class of the match to be hosted with. Supports server sockets,
	player updates and sends out game arena updates.
	"""
	_comm: BasicComm = None

	__port_lease: LeasableObject = None
	__threadcollection: ThreadCollection = None

	def __init__(self, available_ports: LeasableList, name: str, features: List[str]):
		"""
		Initialize a new match server with the necessary parameters

		Args:
			available_ports (LeasableList): Available ports to lease one from
			name (str): Name of the match
			features (List[str]): Features of the match as a string list
		"""
		try:
			# Host of the server is always an empty strin
			host = ""
			super().__init__(host, name, features)

			# Lease a port for the server from the collection
			self.__port_lease = available_ports.lease()
			self._port = self.__port_lease.getObj()

			# Initialize the communication protocoll
			self._comm = BasicComm()

			# Add event handlers
			self._comm.ENewDirection = self.handle_new_direction

			# Create a collection of thread to maintain
			self.__threadcollection = ThreadCollection()
		except LeaseError as err_lease:
			err_msg = "Cannot create match, the server has run out of ports. %s" % str(err_lease)
			logging.error(err_msg)
			raise ServerError(err_msg)
		except Exception as err:
			err_msg = "Cannot create match. Reason: %s" % str(err)
			logging.error(err_msg)
			raise ServerError(err_msg)
	
	def open(self):
		"""
		Open a match for clients to join. Initialize threads and start the UDP game server
		"""
		pass


	def close(self):
		"""
		Close the match, and clean up the leases and sockets after the processes.
		"""
		logging.info("Closing the match is requested")

		# Give back the port lease
		self.__port_lease.free()

		logging.debug("Waiting for all the match threads to finish...")
		self.__threadcollection.join_all()

		logging.info("Match %s is successfully close.", self.name)
	
	def handle_new_direction(self, sender, player_id:int, direction:tuple):
		"""
		Handle when a player sets a new direction

		Args:
			player_id (int): ID of the player in the match
			direction (tuple): New direction
		"""
		# Get the IP Adress, who is requesting it
		#requester_host = self.__current_conn[0]
		try:
			#requester_player = self.get_bound_player(requester_host)
			# TODO Implement IP Adress checking
			requester_player = self._players[player_id]

			vel = requester_player.getVelocity() # Vect2D
			if vel.x != direction[0] and vel.y != direction[1]:
				# Log when a player really changes the direction
				logging.info("Player ID=%d, NAME=%s has a new direction %s" % (player_id, requester_player.getName(), str(direction)))

			requester_player.setVelocity(direction[0], direction[1])
		except Exception as exc: #pylint: disable=broad-except
			logging.warning(str(exc))
