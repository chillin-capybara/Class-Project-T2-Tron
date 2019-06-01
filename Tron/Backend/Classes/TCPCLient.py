from Client import Client
from Core.Event import Event

class TCPCLient(Client):
	PayersUpdated = Event()

	def attachPlayersUpdated(self, callback):
		if callable(callback):
			self.PayersUpdated.attach(callable)
		else:
			raise TypeError