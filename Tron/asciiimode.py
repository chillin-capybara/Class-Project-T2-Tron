import sys
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron/')

import time

from Tron.Backend.Core.Router import Router, Route
from Tron.Backend.Classes.GameClient import GameClient

ROUTER = Router()
CLIENT = GameClient()

def display(string):
	print(string, flush=True)

def display_head(string):
	display("---- {} ----".format(string))

def base_default():
	display("Command not understood!")

def display_lobby_list():
	"""
	Show all the lobbies available
	"""
	display_head("List of lobbies")
	lid = 0
	for lobby in CLIENT.lobbies:
		display("lobby{:<3d}  |:{}".format(lid, lobby.port))
		lid += 1

def base_discover():
	"""
	Discover the lobbies on the server
	"""
	CLIENT.discover_lobby()

	time.sleep(1)
	display_lobby_list()

def base_enter(lid:int):
	"""
	Enter a lobby
	
	Args:
		lid (int): ID of the lobby
	"""
	try:
		lobby_index = int(lid)
		CLIENT.enter_lobby(lobby_index)
		display("Lobby%d entered!" % lobby_index)
	except Exception as exc:
		display("The lobby cannot be entered. Reason: %s" % str(exc))

def base_list():
	"""
	List matches in a lobby
	"""
	try:
		CLIENT.lobby.list_matches('Tron')
	except Exception as exc:
		display("Matches cannot be listed. Reason: %s" % str(exc))

ROUTER.add_default(base_default)
ROUTER.add_route('discover', base_discover)
ROUTER.add_route('enter lobby(\d+)', base_enter)
ROUTER.add_route('list', base_list)


while True:
	ins = input("/client $ ")
	ROUTER.run(ins)
