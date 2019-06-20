from .Client import Client
from .TCPClientThreads import SenderClientThread, ReceiverClientThread
from .JSONComm import JSONComm
from .CommProt import CommProt
from ..Core.Exceptions import ClientError
import socket


"""
Realisation of TCP Client Interface for TCP Client
"""
class TCPCLient(Client):
    
	__host = ""                 # Server Host IP
	__port = 0                  # Server Port
	__sock = None 				# Cleintsocket
	__bufferSize = 4096
	__Comm = JSONComm()

	def __int__(self, host = "", port=23456):
		"""
		Initialize TCP Client on the given host IP and port
		Args: 
			host (str): IPv4 adress of host (any = "")
			port (int): Port number of the Server
		Raises: 
			TypeError: Not valid types
			ValueError: Port Number is invalid
		"""
        
		# if not type(host) == str:
		# 	raise TypeError 

		# if not type(port) == int:
		# 	raise TypeError

		# if not type(port) == int:
		# 	raise TypeError

		# try:
		# 	# Create IPv4 TCP socket:
		# 	self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROT_TCP)
		# 	self.__sock.connect ((host.port))
		# except Exception as e:
		# 	# raise ClientError
		# 	raise ClientError(str(e))


	def attachPlayersUpdated(self, callback):
		"""
		TODO: DOC
		"""
		raise NotImplementedError

	def Connect(self, server, port):
		"""
		Connect to the server using the port

		Args:
			server (str): IP address of the server
			port (int):   Port of the server
		
		Raises:
			TypeError: The type of the input parameters is not valid
			ValueError: The value of the input parameters is invalid, 
				(negative port, etc..)
		"""

		if not type(server) == str:
			raise TypeError 

		if not type(port) == int:
			raise TypeError

		if port not in range(0,2**16-1):
			raise ValueError

		try:
			# Create IPv4 TCP socket:
			self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.__sock.connect ((server, port))
		except Exception as e:
			# raise ClientError
			raise ClientError(str(e))
		# communicate ACK
		# communicate 

  
	def Disconnect(self):
		"""
		Disconnect from a connected game server.

		Raises:
			ClientError: Not connected to any server
		"""
		try:
			self.__sock.close()
		except self.__sock.timeout:
			raise ClientError()
			
	def Scan(self, port):
		"""
		Scan for available servers on the given port number.

		Args:
			port (int): Port number

		Raises:
			TypeError: The port is not an int
			ValueError: The port number is invalid
		
		Returns:
			iter: Iterable collection of the available servers
		"""
		raise NotImplementedError

	def __create_threads(self, sock: socket.socket):
		"""
		Create send and receive threads for connection to the server

		Args:
			sock (socket): Accepted connection socket
			player_id (int): Index of the player on the client
		Raises:
			TypeError: sock is not a socket
			ServerError: ???
		"""
		senderThread = SenderClientThread(sock, 0, self.__Comm)
		receiverThread = ReceiverClientThread(sock, 0, self.__Comm)

		# Start the Threads
		senderThread.start()
		receiverThread.start()
	
	def Start(self):
		
		try:
			# Start recieving on socket
			# TODO: Start new thread for client_socket
			self.__create_threads(self.__sock)
			input("Waiting...")

		except:
			pass
			