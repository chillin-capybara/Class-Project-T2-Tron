from .AbstractMatch import AbstractMatch
from .HumanPlayer import HumanPlayer
from ..Core.Router import *
from .BasicComm import BasicComm
from ..Core.leasable_collections import LeasableObject, LeasableList, LeaseError
from typing import List
from ..Core.Exceptions import ServerError
from ..Core.ThreadCollection import ThreadCollection
from .BasicComm import BasicComm
from .RectangleArena import RectangleArena, DieError
from ..Core.Event import Event
from ..Core.Hook import Hook
from ..Core.globals import *
from ..Core.matrix import matrix_split
import threading
import logging
import socket
import time
import random
import os

# TODO REMOVE THIS
def draw_matrix(matrix):
	os.system('clear')
	linestr = ""
	for row in matrix:
		for col in row:
			linestr += "%d " % col
		print(linestr, flush=True)
		linestr = ""

def generate_random_player_data(sizeX, sizeY, feat_players, directions):
	# Randomly position the players

	# Don't put players at the very end of the arena: Apply padding
	padding = 10 # 10% Padding
	xmin = int(sizeX/padding)
	ymin = int(sizeY/padding)
	xmax = int(sizeX - xmin)
	ymax = int(sizeY - ymin)

	# Create a list of game coordinates
	list_x = list(range(xmin,xmax))
	list_y = list(range(ymin,ymax))

	# Choose random staring points and coordinates for every player
	chx = random.choices(list_x, k=feat_players+1)
	chy = random.choices(list_y, k=feat_players+1)
	pos = []
	for i in range(0,feat_players+1):
		pos = (chx[i], chy[i])
		direct = random.choice(directions)
		yield pos, direct # Generate a new value

class MatchServer(AbstractMatch):
	"""
	Server class of the match to be hosted with. Supports server sockets,
	player updates and sends out game arena updates.

	Events:

		OnPlayerWin(sender, player_id): is triggered, when a player wins the match

		OnMatchTerminated(sender, reason): is triggered when the match is closed due
			to errors or by admin
	"""
	_comm: BasicComm = None

	__player_slots : LeasableList = None # Slots of available player_ids

	__port_lease: LeasableObject = None
	__threadcollection: ThreadCollection = None

	# Server UDP socket to send and receive data
	__udpsock: socket.socket = None
	__player_addresses: list = None
	__current_conn = None # Current connection address, to validate, which player sends it

	__seq_send: List[int] = None # List to track which sequence number to send for which client
	__last_activity = None # Clock time, when the last direction update was performed
	__require_close = False

	router: Router = None

	EStart: Event = None
	ELifeUpdate: Event = None # Event to call when a player's life has to be updated
	OnPlayerWin: Event  = None  # Event to be called when a player wins
	OnMatchTerminated: Event = None # Event to be called when the match is close by admin

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

			# Create the player slots (ID=0 is reserved for an empty player)
			self.__player_slots = LeasableList(list(range(1,self._feat_players+1)))
			logging.info("Slots created: %s" % str(list(range(1,self._feat_players+1))))

			# Add slot updater for the server
			self._feat_slots = self.feat_players
			self.__player_slots.OnUpdate += self.on_update_slots

			# Create the list to store the connections to the players
			self.__player_addresses = []

			# Initialize the array to track the sequence numbers
			self.__seq_send = []
			for i in range(0, self.feat_players+1):
				self.__seq_send.append(0)

			# Initialize the communication protocoll
			self._comm = BasicComm()

			# Add event handlers
			self._comm.ENewDirection += self.handle_new_direction

			# Create a collection of thread to maintain
			self.__threadcollection = ThreadCollection()

			# Initialize the local events of the match
			# Event to notify the joined playes to that the match is starting
			# ANCHOR Event inits
			self.EStart = Event('port', 'player_ids', 'players')
			self.ELifeUpdate = Event('player_id', 'score')
			self.OnPlayerWin = Event('player_id')
			self.OnMatchTerminated = Event('reason')

			# Initialize the command router
			self.router = Router()
			self.router.add_default(self.base_default)
			self.router.add_route('watch', self.base_watch)
			self.router.add_route('ls', self.base_ls)
			self.router.add_route('stat', self.base_stat)

		except LeaseError as err_lease:
			err_msg = "Cannot create match, the server has run out of ports. %s" % str(err_lease)
			logging.error(err_msg)
			raise ServerError(err_msg)
		except Exception as err:
			err_msg = "Cannot create match. Reason: %s" % str(err)
			logging.error(err_msg)
			raise ServerError(err_msg)

	def randominze_player_positions(self):
		"""
		Set the player positions to random at the beginning
		"""
		# Use the generator to create new player data and set the players starting
		ini_data = generate_random_player_data(self.arena.sizeX, self.arena.sizeY,
														self.feat_players, MATCH_PLAYER_DIRECTIONS)
		iter_ini_data = iter(ini_data)

		for player in self.players: # self.players property already ignores player zero
			pos, vel = next(iter_ini_data)
			# Set the default values for the players
			player.setPosition(pos[0], pos[1])
			player.setVelocity(vel[0], vel[1])

	def on_update_slots(self, sender:LeasableList):
		"""
		Update the available slots on the server

		Args:
			sender (LeasableList): Caller object of the event
		"""
		self._feat_slots = sender.count_free()
		logging.debug("Server available slots updated to %d" % self._feat_slots)

	def open(self):
		"""
		Open a match for clients to join. Initialize threads and start the UDP game server
		"""
		logging.info("Starting the udp game server on port %d" % self.port)
		sender = threading.Thread(target=self.__sender_thread, name="MatchSenderThread")
		receiver = threading.Thread(target=self.__receiver_thread, name="MatchReceiverThread")
		updater = threading.Thread(target=self.__field_updater_thread, name="MatchUpdaterThread")

		# Randomize the player positions when the match opens
		self.randominze_player_positions()

		# Add all the threads to the thread collection
		self.__threadcollection.append(sender)
		self.__threadcollection.append(receiver)
		self.__threadcollection.append(updater)

		# Start all the threads
		self.__threadcollection.start_all()

	def close(self, join=True, terminate = True):
		"""
		Close the match, and clean up the leases and sockets after the processes.
		"""
		logging.info("Closing the match is requested")
		try:
			# Free all the given player slots
			self.__player_slots.free_all()

			# Give back the port lease
			self.__port_lease.free()
		except:
			pass

		# Set a close flag
		self.__require_close = True

		# Destroy the socket
		try:
			self.__udpsock.shutdown(socket.SHUT_RDWR)  # Shutdown both ends of the socket
			self.__udpsock.close()                     # Close the socket, as is
		except:
			pass # Ignorable error

		if terminate:  # When the termination of the match was requested
			self.OnMatchTerminated(self, reason="The match was closed by the server on request")

		logging.debug("Waiting for all the match threads to finish...")
		if join:
			self.__threadcollection.join_all()

		logging.info("Match %s is successfully close.", self.name)

		# Call the close event
		self.EClose(self)

	def __receiver_thread(self):
		"""
		Receive the direction updates from players, and the game start request
		"""
		try:
			logging.info("Initializing UPD Game server on port %d" % self.port)
			# Create and bind the socket onto the match's port
			self.__updsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			self.__updsock.bind(("", self.port))

			while True:
				if self.__require_close:
					logging.debug("Closing the match receiver on request...")
					break

				data, conn = self.__updsock.recvfrom(UDP_RECV_BUFFER_SIZE)
				self.__current_conn = conn # For validating the player id
				if conn not in self.__player_addresses:
					self.__player_addresses.append(conn)

				seq, msg = data.decode("UTF-8").split(" ", 1) # Split the sequence number and the message
				packet = bytes(msg, "UTF-8") # Convert the packet back to bytes
				self._comm.process_response(packet) # Process the response of the packet
		except Exception as e:
			logging.error("Match handler stopped. Reason: %s" % str(e))

	def __sender_thread(self):
		"""
		Send the updates of the matrix to every player that is in the list of addresses
		"""
		logging.info("Starting sender thread to keep the clients updated")
		try:
			while True:

				if self.__require_close:
					logging.debug("Closing the match sender thread on request")
					break

				try:
					cindex = 0
					for conn in self.__player_addresses:
						# Get the matrix to send: Always get a freash matrix
						matrix = self._arena.matrix

						# Split the matrix -> Send every part as an update request to the client
						splitted = matrix_split(matrix, MAX_MATRIX_SIZE[0], MAX_MATRIX_SIZE[1])
						for key in splitted.keys():
							packet = self._comm.update_field(key, splitted[key])
							seq = bytes("%d " % self.__seq_send[cindex], "UTF-8")
							packet = seq + packet

							# Constantly send updates to every client
							self.__updsock.sendto(packet, conn)
							self.__seq_send[cindex] += 1 # Increment the sent index
							#logging.debug("Update sent with seq: %s" % str(seq))

						# Increment the index of the connection
						cindex += 1
					time.sleep(0.1)

				except Exception as e:
					logging.warning("Error while sending. %s" , str(e))
		except Exception as e:
			logging.error("Game updater has stopped. Reason: %s" , str(e))

	def __field_updater_thread(self):
		"""
		Update the field with stepping the players to the current direction
		"""
		# Wait until all the players are ready
		logging.info("Wait until all players press ready...")
		all_ready = False
		while not all_ready:
			all_ready = True
			for player in self.players:
				if not player.is_ready():
					all_ready = False

		logging.info("All players ready, starting the match.")
		while True:
			try:
				#draw_matrix(self.arena.matrix)
				#print("--------- Players: ------------")
				pid = 1 # IGNORE PLAYER ZERO
				alive = 0
				for player in self.players:
					try:
						if player.is_alive():
							alive += 1
							player.step(self.arena.sizeX, self.arena.sizeY)

							#logging.info("Payer %d stepped on %s" % (pid, str(player.getPosition())))
							self._arena.player_stepped(pid, player.getPosition())
					except DieError:
						player.die() # Call the die function on the player
						try:
							self.ELifeUpdate(self, player_id=pid, score=player.lifes) # Call the life update event
						except OSError:
							# BROKEN PIPE -> KICK PLAYER
							# NOTE The player ID should be freed by the lobby thread
							self.kick_player(pid)

						#logging.info("Player ID=%d '%s' died. Has %d / %d lifes left" % (pid, player.getName(), player.lifes, self.feat_lifes))
					finally:
						#print("%d; %s \t| %s | %s | %d" % (pid, player.getName(), str(player.getVelocity()), str(player.getPosition()), player.lifes), flush=True)
						pid += 1

					# TODO REMOVE THIS DUMMY PRINTOUT
			except Exception as e:
				logging.warning("Error while updating player positions. Reason: %s" % str(e))

			time.sleep(0.5) # 2 Updates per second

			if self.__require_close:
				logging.info("Closing the field updater on request")
				break

			# Check when a player wins the game
			if alive == 1 and self.feat_players > 1:
				pid = 1
				for player in self.players:
					if player.is_alive():
						self.OnPlayerWin(self, player_id=pid)
						logging.info("Player %s won the game. Closing the server...", player.getName())
					pid +=1

				# Stop the thread
				break
			elif alive == 0:
				# If there is no players alive, stop the match...
				logging.info("All player are dead. Closing the server...")
				break  # Stop the server

			# Check if the match is in idle, when yes -> Close it
			if self.is_idle():
				break # Stop the updater thread loop

		# Close automatically everything, when the main thread stops
		self.close(join=False, terminate=False)

	def kick_player(self, player_id:int):
		"""
		Kick a player from the match by the player ID

		Args:
			player_id (int): Player ID of the player
		"""
		# NOTE This should make possible that another client can later continue from this status
		player = self._players[player_id]
		player.setVelocity(0,0) # Set the velocity of the player to zero

	def check_for_start(self):
		if self.__player_slots.count_free() == 0:
			logging.info("Match %s is full, starting the match..." % self.name)

			# Start the match server
			self.open()

			# Generate the params string from the players
			player_ids = list(range(1,self.feat_players+1))
			players = self._players[1:] # Ignore player 0

			# All slots reserved
			self.EStart(self, port=self.port, player_ids=player_ids, players=players)

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

			dx, dy = requester_player.getVelocity().to_tuple()
			dxnew, dynew = direction

			# Check if the direction to choose is valid
			if (dx == -dxnew and dxnew != 0) or (dy == -dynew and dynew != 0):
				#logging.debug("Invalid direction from %s to %s" % (str((dx,dy)), str((dxnew, dynew))))
				pass
			else:
				requester_player.setVelocity(dxnew, dynew)
		except Exception as exc: #pylint: disable=broad-except
			logging.warning(str(exc))
		finally:
			# Update the last activity time
			self.__last_activity = time.perf_counter()

	def lease_player_id(self, player:HumanPlayer) -> LeasableObject:
		"""
		Lease a player if, from the collection of player IDs.

		NOTE
			The Lease has to be freed, when a player disconnects

		Returns:
			LeasableObject: Leased player id, wrapped in a LeaseableObject
		Raises:
			ValueError: When the playername or color is already taken in the match
		"""

		# Check if the playername & color is already taken
		for pl in self.players:
			if (pl.getName() is not "") and (pl.getColor() == player.getColor()):
				raise ValueError("The color {} is already taken".format(str(player.getColor())))
			if pl.getName() == player.getName():
				raise ValueError("The playername {} is already taken".format(player.getName()))
		
		# Let all the player properties to be taken from the Lobby
		lease = self.__player_slots.lease()
		pid = lease.getObj()

		# Set the lifes of the newly joined player!
		player.set_lifes(self.feat_lifes)
		self._players[pid] = player

		return lease

	def is_idle(self):
		"""
		Check if the players were in idle for MATCH_IDLE_TIMEOUT seconds, and
		close the match, if yes.
		"""
		if self.__last_activity is not None:
			# Only when there was an activity in the match before
			if time.perf_counter() - self.__last_activity > MATCH_IDLE_TIMEOUT:
				return True
			else:
				return False
		else:
			return False

	def handle_lobby_stop(self, sender):
		"""
		Handle when the lobby thread was stopped, and stop the game server

		Args:
			sender (Lobby): Caller of the event
		"""
		try:
			self.close(join = False)
		except:
			pass # Error can be ignored

	def base_ls(self):
		"""
		List the players of the match
		"""
		try:
			for player in self.players:
				print("{:<20s}   COLOR: {}".format(player.getName(), str(player.getColor())), flush=True)
			print("%d players were listed" % len(self.players))
		except:
			print("Players cannot be listed.", flush=True)

	def base_stat(self):
		"""
		Show the stats of the match
		"""
		try:
			print("Players joined / Max players: %d / %d" % (self.__player_slots.count_leased(), self.feat_players), flush=True)
			print("Size of the arena is %d x %d" % (self.arena.sizeX, self.arena.sizeY), flush=True)
		except:
			print("Cannot show the match stats", flush=True)

	def base_watch(self):
		"""
		Display the current match in the terminal
		"""
		try:
			while True:
				os.system('clear')
				draw_matrix(self.arena.matrix)
				print("---- Players ----")
				for pl in self.players:
					print("{:<15s}   POS: {:<10s}   DIR: {:<10s} LIFES: {}".format(pl.getName(), str(pl.getPosition()), str(pl.getVelocity()), pl.lifes), flush=True)
				time.sleep(1)
		except KeyboardInterrupt:
			pass # Close the watcher
		except:
			print("Error while watching the game.", flush=True)

	def base_default(self):
		"""
		Command not recognizeable
		"""
		print("Command cannot be recognized", flush=True)

	def base(self, base=""):
		"""
		Base command processor
		"""
		while True:
			ins = input("%s >>>" % base)
			if ins == "cd ..":  # Go back to the parent
				return
			else:
				self.router.run(ins)
