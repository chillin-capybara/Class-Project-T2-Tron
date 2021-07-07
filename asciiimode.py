import sys
sys.path.append('/Users/marcellpigniczki/Documents/GitHub/Class-Project-T2-Tron/')

import time
import os
import curses
import keyboard
from typing import List

from Tron.Backend.Core.Router import Router, Route
from Tron.Backend.Classes.GameClient import GameClient
from Tron.Backend.Classes.MatchClient import MatchClient

# Coloring the matrix
from colorama import init
from colorama import Fore, Back, Style
init()

WELCOME = """
  _______ ______ _____  __  __ _____   _______ _____   ____  _   _ 
 |__   __|  ____|  __ \|  \/  |_   _| |__   __|  __ \ / __ \| \ | |
    | |  | |__  | |__) | \  / | | |______| |  | |__) | |  | |  \| |
    | |  |  __| |  _  /| |\/| | | |______| |  |  _  /| |  | | . ` |
    | |  | |____| | \ \| |  | |_| |_     | |  | | \ \| |__| | |\  |
    |_|  |______|_|  \_\_|  |_|_____|    |_|  |_|  \_\\____/|_| \_|
"""      

ROUTER = Router()
CLIENT = GameClient()

CLIENT.me.setName("ASCIII")
CLIENT.me.setColor((255,255,0))
CLIENT.me.setVelocity(1,0)

game_running = False
status_test = ""

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

def on_update_matches(sender, matches: List[MatchClient]):
	os.system('clear')
	display_head("List of available matches")
	for match in matches:
		display("{:<15s}  features: {}".format(match.name, match.get_feature_string()))

def base_list():
	"""
	List matches in a lobby
	"""
	try:
		CLIENT.lobby.list_matches('Tron')
	except Exception as exc:
		display("Matches cannot be listed. Reason: %s" % str(exc))

def base_create(name, num_pl, num_lifes):
	try:
		players = int(num_pl)
		lifes   = int(num_lifes)
		CLIENT.lobby.create_match('Tron', name, {'Players':players, 'Lifes':lifes})
	except Exception as exc:
		display("Error creating match. Reason: %s" % str(exc))

def main(win):
	win.nodelay(True)
	key=""
	win.clear()                
	win.addstr("Detected key:")
	while 1:          
		try:                 
			key = win.getkey()         
			win.clear()                
			win.addstr("Detected key:")
			win.addstr(str(key))
			if key == os.linesep:
				break           
		except Exception as e:
			# No input   
			pass         

def base_ingame(win):
	try:
		curses.start_color()
		# Initialize pre-defined color pairs
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
		curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
		curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
		curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
		curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
		curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)

		win.nodelay(True)
		key=""
		win.clear()                
		while True:
			try:
				key = win.getkey()
				if key == 'a':
					CLIENT.me.setVelocity(-1, 0)
				elif key == 'd':
					CLIENT.me.setVelocity(1, 0)
				elif key == 'w':
					CLIENT.me.setVelocity(0, 1)
				elif key == 's':
					CLIENT.me.setVelocity(0, -1)
			except:
				pass # NO input

			matrix = CLIENT.match.arena.matrix

			# DISPLAY THE STATUS TEXT in the first line
			win.addstr(1, 0, status_test, curses.color_pair(7))

			h = 4
			w = 0
			maxw = 0
			linestr = ""
			for row in matrix:
				for col in row:
					win.addstr(h, w, "%d " % (col), curses.color_pair(col+1))
					w += 2

				h += 1
				maxw = max(w, maxw)
				w = 0
				linestr = ""
			
			# Footer line
			win.addstr(h+1, 0, "Press CTRL + C to exit the game.")

			# And now to list the players on the sidebar
			wstart = maxw + 3
			h = 4
			win.addstr(h, wstart, "|   PLAYERS ")
			h += 1
			win.addstr(h, wstart, "|")
			h += 1

			pid = 1
			for pl in CLIENT.match.players:
				if pid == CLIENT.match.player_id:
					win.addstr(h, wstart, "|  You            {:<2d} / {}".format(pl.lifes, CLIENT.match.feat_lifes), curses.color_pair(pid+1))
				else:
					win.addstr(h, wstart, "|  Player {:<2d}  {:<2d} / {}".format(pid, pl.lifes, CLIENT.match.feat_lifes), curses.color_pair(pid+1))
				win.addstr(h+1, wstart, "| ")
				h += 2

	except KeyboardInterrupt:
		CLIENT.leave_match()
		display("Exiting the match...")

def on_match_started(sender):
	global game_running
	display("The game is starting...")
	game_running = True
	time.sleep(0.5)


def base_join(name):
	global game_running
	try:
		ind = 0
		for match in CLIENT.lobby.matches:
			if match.name == name:
				CLIENT.join_match(ind)  # Join the match
				display("Joining match %s ..." % match.name)
				time.sleep(0.5)
				CLIENT.i_am_ready()  # Tell the server, that you are ready
				display("Waiting for the match to start...")
				time.sleep(1)

				curses.wrapper(base_ingame)
				return
			ind += 1
	except Exception as exc:
		display("Error joining match. Reason: %s" % str(exc))


def on_match_ennded(sender, reason):
	global status_test
	status_test = reason


HELP = [
	("discover", "Discover the available lobbies."),
	("enter [lobby]", "Enter the selected lobby."),
	("list", "List the available matches in the lobby for Tron"),
	("create [matchname] [players] [lifes]", "Create a new match with players and lifes"),
	("join [matchname]", "Join the selected match. (Automatically as READY to play)"),
	("help", "Show all the commands available"),
	("exit", "Exits the client.")
]

def base_help():
	"""
	List the available commands
	"""
	print("---- Available commands ----")
	for syntax, desc in HELP:
		print("{:<40s}   : {}".format(syntax, desc))

def base_exit():
	CLIENT.close()
	raise KeyboardInterrupt


# Event handler for listing the matches
CLIENT.EMatchEnded     += on_match_ennded
CLIENT.OnMatchesUpdate += on_update_matches
CLIENT.EMatchStarted   += on_match_started

ROUTER.add_default(base_default)
ROUTER.add_route(r'discover', base_discover)
ROUTER.add_route(r'enter lobby(\d+)', base_enter)
ROUTER.add_route(r'list', base_list)
ROUTER.add_route(r'create (\w+) (\d+) (\d+)', base_create)
ROUTER.add_route(r'join (\w+)', base_join)
ROUTER.add_route(r'help', base_help)
ROUTER.add_route(r'exit', base_exit)

if __name__ == "__main__":
	display(WELCOME)
	try:
		while True:
			ins = input("/client $ ")
			if(ins == ""):
				pass
			else:
				ROUTER.run(ins)
	except KeyboardInterrupt:
		display("")
		display("Exiting Termi-Tron...")
