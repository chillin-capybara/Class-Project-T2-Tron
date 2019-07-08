# Quelle: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble
import re
import logging
import time
from datetime import datetime
import json
######## import own modules ############################
from Backend.Classes.GameClient import GameClient
CLIENT: GameClient = GameClient()
from ..mainUI import GameApp, GameUI
from collections import namedtuple
from Backend.Classes.GameServer import GameServer
datapath = "Tron/data.json"

######## Load the kv files into Menu.py ############################
Builder.load_file('kvfilesmenu/mainmenufloat.kv')
Builder.load_file('kvfilesmenu/createservermenufloat.kv')
Builder.load_file('kvfilesmenu/searchforlobbiesmenufloat.kv')
Builder.load_file('kvfilesmenu/lobbymenufloat.kv')
Builder.load_file('kvfilesmenu/creatematchmenufloat.kv')
Builder.load_file('kvfilesmenu/settingsmenufloat.kv')
Builder.load_file('kvfilesmenu/statisticsmenufloat.kv')
Builder.load_file('kvfilesmenu/aboutmenufloat.kv')
Builder.load_file('kvfilesmenu/gamestartmenu.kv')
Builder.load_file('kvfilesmenu/pausemenu.kv')
Builder.load_file('kvfilesmenu/connectionlostmenufloat.kv')
Builder.load_file('kvfilesmenu/gameovermenu.kv')
Builder.load_file('kvfilesmenu/globalcustomwidgets.kv')

######## Class Definitions of the Screens ############################
class MainMenuFloat(Screen):
	def loadplayerdata(self) -> None:
		"""
		Load the Player Name from data.json
		Load the Player Color from data.json

		Args: -
		Return: -
		"""
		try:
			filef = open(datapath)
			data = json.load(filef)
			playername = data[0]
			color = data[1]
			playercolor = (color[0], color[1], color[2])
			CLIENT.me.setName(playername)
			CLIENT.me.setColor(playercolor)
		except:
			savedata = ("Enter_Name", (0,0,0))
			with open(datapath, 'w', encoding='utf-8') as outfile:
				json.dump(savedata,outfile)


	def quit(self) -> None:
		#CreateServerMenuFloat.statusServer(self, False, 0)
		#self.server.Stop()
		#self.client.Stop()
		exit()

class CreateServerMenuFloat(Screen):

	def statusServer(self, statusswitch, numberlobbies):
		"""
		Call open server function and sends number of lobbies

		Args:
			statusswitch(boolean)
			numberlobbies (int)
		Return:
			-
		"""
		self.statusswitch = statusswitch
		self.numberlobbies = numberlobbies

		if self.statusswitch:
			logging.info('Create Server with %d Lobbies' % self.numberlobbies)
			self.server=GameServer(self.numberlobbies)
			self.server.Start()
			
		else:
			logging.info('Stopping Server...')
			self.server.Stop()

class SearchForLobbiesMenuFloat(Screen):

	def getPlayerdata(self,test):
		print("Updating screen... %s" % test)

		outputname = CLIENT.me.getName()
		print(outputname, flush= True)
		if outputname != '':
			self.ids.explainmenuLabel.text = ('Here you can Enter the Lobby as %s' % outputname)
		else:
			pass

		color = CLIENT.me.getColor()
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.explainmenuLabel.background_color=playercolor

	def getavailableLobbies(self):
		"""
		Get the Lobbies which are available

		Args:
			Lobbies (list): IP & Port
		Return:
			-
		"""
		# Lobby = namedtuple('Lobby', ['host', 'port'])
		# lobby1 = Lobby("192.168.1.1", 20)
		# lobby2 = Lobby("10.0.0.1", 9984)
		# lobby1.host
		CLIENT.discover_lobby()
		listlobbies = CLIENT.lobbies
		count_lobbies = listlobbies.__len__()
		for i in range(0,count_lobbies):
			lobby = listlobbies[i]
			if i == 0:
				self.ids.lobby1Label.text = 'Lobby %d: Host: %s with Port %d' % (i+1, lobby.host, lobby.port)
			elif i == 1:
				self.ids.lobby2Label.text = 'Lobby %d: Host: %s with Port %d' % (i+1, lobby.host, lobby.port)
			elif i == 2:
				self.ids.lobby3Label.text = 'Lobby %d: Host: %s with Port %d' % (i+1, lobby.host, lobby.port)
			elif i == 3:
				self.ids.lobby4Label.text = 'Lobby %d: Host: %s with Port %d' % (i+1, lobby.host, lobby.port)
			elif i == 4:
				self.ids.lobby5Label.text = 'Lobby %d: Host: %s with Port %d' % (i+1, lobby.host, lobby.port)
			else:
				pass

	def updatechosenLobby(self, currentlobby):
		"""
		Sets variable for choosen Lobby

		Args:
			Lobby (int):
		Return:
			Lobby (int)
		"""
		self.currentlobby = currentlobby

		self.lobby = int(self.currentlobby)
		
		print('Lobby: %d has been choosen.' % (self.lobby), flush = True)
		return self.lobby

	def enterLobby(self):
		"""
		Sends Lobby to Server

		Args:
			-
		Return:
			-
		"""

		print('Enter Lobby %s' % (self.lobby))
		CLIENT.enter_lobby(self.lobby-1)

class LobbyMenuFloat(Screen):
	def getLobbyInformation(self):
		"""
		Get the Information of the available Lobbies

		Args:
			Lobbies (list): name; game; features
		Return:
			-
		"""
		# Match = namedtuple('Match', ['name', 'game', 'features'])
		# match1 = Match("Letsfight", 'Tron', '3 Players; 4 Lives')
		# match2 = Match("FullHouse123", 'Tron', '5 Players; 8 Lives')
		# match3 = Match("Pong", 'Pong', '2 Players; 1 Lives')
		# match4 = Match("Alone", 'Minecraft', '1 Players; 1 Live; 3 Zombies; a Million Bricks')
		# listmatches = [match1, match2, match3, match4]

		CLIENT.lobby.list_matches('Tron')
		listmatches = CLIENT.lobby.matches
		print(listmatches)
		count_matches = listmatches.__len__()
		for i in range(0,count_matches):
			match = listmatches[i]
			print("%s %s %s " % (match.name, match.game, match.featureString))
			if i == 0:
				self.ids.match1nameLabel.text = match.name
				self.ids.match1gameLabel.text = match.game
				self.ids.match1featureLabel.text = match.featureString
			elif i == 1:
				self.ids.match2nameLabel.text = match.name
				self.ids.match2gameLabel.text = match.game
				self.ids.match2featureLabel.text = match.featureString
			elif i == 2:
				self.ids.match3nameLabel.text = match.name
				self.ids.match3gameLabel.text = match.game
				self.ids.match3featureLabel.text = match.featureString
			elif i == 3:
				self.ids.match4nameLabel.text = match.name
				self.ids.match4gameLabel.text = match.game
				self.ids.match4featureLabel.text = match.featureString
			elif i == 4:
				self.ids.match5nameLabel.text = match.name
				self.ids.match5gameLabel.text = match.game
				self.ids.match5featureLabel.text = match.featureString
			else:
				pass
	def updatechosenMatch(self, currentmatch):
		"""
		Sets variable for choosen Lobby

		Args:
			Lobby (int):
		Return:
			Lobby (int)
		"""
		self.currentmatch = currentmatch

		self.match = int(self.currentmatch)
		
		print('Lobby: %d has been choosen.' % (self.match), flush = True)
		return self.match

	def joinMatch(self):

		CLIENT.join_match(self.match - 1)

class CreateMatchMenuFloat(Screen):
	
	def createMatch(self, numberplayer, numberlifes, matchname):

		self.numberplayer = numberplayer
		self.numberlifes = numberlifes
		self.matchname = matchname

		print('Create Match with %d players, %d lifes and name %s' % (self.numberplayer, self.numberlifes, self.matchname))
		settings = {
			'Players' : self.numberplayer,
			'Lifes' : self.numberlifes
		}
		CLIENT.lobby.create_match('Tron', self.matchname, settings)

	def validateInput(self, inpt):

		self.inpt = inpt

		try:
			lastcharacter = self.inpt[-1:]
			x = re.findall("[a-zA-Z0-9_]", lastcharacter)
			if len(x) == 1:
			#if len(parsspace) == 1:
				self.ids.gamenameTextInput.text = inpt

			else:
				#self.openBubble(lastcharacter)
				rightstring = self.inpt[:-1]
				self.ids.gamenameTextInput.text = rightstring

		except Exception as e:
			logging.warning(str(e))

	# def openBubble(self, character):

	# 	#arrow_pos='top_mid', text='Character %s is not allowed' % character
	# 	self.bubble = Bubble()

	# 	self.add_widget(self.bubble)
	# 	time.sleep(1)
	# 	self.bubble.clear_widgets()

class SettingsMenuFloat(Screen):
	def loadplayerdata(self) -> None:
		"""
		Load the Player Name from data.json
		Load the Player Color from data.json

		Args: -
		Return: -
		"""
		filef = open(datapath)
		data = json.load(filef)
		playername = data[0]
		color = data[1]
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.nameTextInput.hint_text=("Current Playername: %s" % playername)
		self.ids.colordisplayLabel.background_color=playercolor
		
	def savechanges(self, playername: str, color: tuple) -> None:
		"""
		Saves the Player Name to backend and data.json
		Saves the Player Color to backend and data.json 

		Args:
			playername (str): new playername / old playername from data.json
			color (tuple): new color / old color from data.json
		Return: -
		"""
		# sends playername and color to backend, but if ist wasnt changed, it sends the data of data.json to backend
		filef = open(datapath)
		loaddata = json.load(filef)
		if playername == "":
			playername = loaddata[0]
			CLIENT.me.setName(playername)
			print("Playername stayed: %s" % playername)
		else:
			CLIENT.me.setName(playername)
			print("Playername changed to: %s" % playername)

		if color == (0, 0, 0):
			playercolor = loaddata[1]
			color = (playercolor[0], playercolor[1], playercolor[2])
			CLIENT.me.setColor(color)
			print("Color stayed: %s" % str(color))
		else:
			CLIENT.me.setColor(color)
			print("Color changed to: %s" % str(color))

		#saves the current playername and color in the json file data.json
		savedata = (playername, color)
		with open(datapath, 'w', encoding='utf-8') as outfile:
			json.dump(savedata,outfile)

	def validateInput(self, inpt: str) -> None:
		"""
		Validates the input of the playername text field

		Args: input (str): the playername
		Return: -
		"""
		self.inpt = inpt
		try:
			lastcharacter = self.inpt[-1:]
			x = re.findall("[a-zA-Z0-9_]", lastcharacter)
			if len(x) == 1:
				self.ids.nameTextInput.text = inpt
			else:
				rightstring = self.inpt[:-1]
				self.ids.nameTextInput.text = rightstring

		except Exception as e:
			logging.warning(str(e))

class StatisticsMenuFloat(Screen):
	def loadplayerdata(self) -> None:
		"""
		Load the Player Name from data.json
		Load the Player Color from data.json

		Args: -
		Return: -
		"""
		filef = open(datapath)
		data = json.load(filef)
		playername = data[0]
		color = data[1]

		outputname = "Player Name: %s" % playername
		self.ids.nameLabel.text = outputname

		sol = "Color: %s" % str(color)
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.colorLabel.text = sol
		self.ids.showcolorLabel.background_color = playercolor

class AboutMenuFloat(Screen):
    pass

class GameStartMenu(Screen):

	def destroyserver(self):
		pass

class PauseMenu(Screen):

	def resumeGame(self):
		"""
		Send Resumesignal to server

		Args:
			-
		Return:
			-
		"""
		#call resume game function
		self.game_is_running = True

	def startGame(self):
		"""
		Send Startsignal to server and begin countdown

		Args:
			-
		Return:
			-
		"""
		start_game = GameApp()
		start_game.run()

	def exitGame(self):
		"""
		Send exitgame signal to server

		Args:
			-
		Return:
			-
		"""
		#call exit game function
		raise NotImplementedError

class ConnectionLostMenuFloat(Screen):
	pass

class GameOverMenu(Screen):

	def getplayedTime(self):
		"""
		Get the played time from the server

		Args:
			player_time (float): Time the player was in the game
		Return:
			String
		"""

		#self.ids.displayplayedtimeLabel.text = time + 'maybe seconds'
		#raise NotImplementedError

	def getwinnerName(self):
		"""
		Get the winner name from the server

		Args:
			winner_name (str): Name of the winner
		Return:
			String
		"""

		#self.ids.displaywinnernameLabel.text = self.winner_name
		raise NotImplementedError

	def getenemiesStatus(self, waiting_for_enemies: bool, enemies_left: bool):
		"""
		Get the status of enemies from the server

		Args:
			waiting_for_enemies (bool): Status other players
			players_enemies (bool): Status other players
		Return:
			String
		"""
		#if waiting_for_enemies == True:
		#	displaytext = 'Please wait for other Players'
		#elif enemies_left == True:
		#	displaytext = 'I am sorry. The other Players left'
		#else:
		#	displatext = 'Server askes you to grab a coffee and wait...'

		#self.ids.statusotherplayersLabel.text = winner_name
		raise NotImplementedError

	def startGame(self):
		"""
		Send Startsignal to server and begin countdown

		Args:
			-
		Return:
			-
		"""
		start_game = GameApp()
		start_game.run()

	def exitGame(self):
		"""
		Closes the client and server

		Args:
			-
		Return:
			-
		"""
		#call functions to close the applicationS
		raise NotImplementedError


	def startGame(self):
		"""
		Send Startsignal to server and begin countdown

		Args:
			-
		Return:
			-
		"""
		#start_game = GameApp()
		#start_game.run()

	def updateArenatype(self, currentarenatype):
		"""
		Sets variable arenatype to 1 or 2

		Args:
			Arenatype (int):
		Return:
			arenatype
		"""
		self.currentarenatype = currentarenatype

		self.arena = int(self.currentarenatype)
		
		print('Arenatype: %d has been choosen.' % (self.arena), flush = True)
		return self.arena 

	def updateDifficulty(self, currentdifficulty):
		"""
		Sets variable arenatype to 1 or 2

		Args:
			Difficulty (int):
		Return:
			difficulty
		"""
		self.currentdifficulty = currentdifficulty

		self.difficulty = int(self.currentdifficulty)
		print('Diffculty: %d has been choosen.' % (self.difficulty), flush = True)
		return self.difficulty
		
	def createServer(self, numberplayer):
		"""
		Call open server function and send difficulty and arenatype

		Args:
			Arenatype (int):
			Difficulty (int):
		Return:
			-
		"""
		self.numberplayer = numberplayer
		#GAME.CreateServer('', 9876, self.numberplayer)
		print('Arenatype: %d, Diffculty: %d and %d Players to play have been choosen.' % (self.arena, self.difficulty, self.numberplayer), flush = True)

	def destroyServer(self):

		print('Destroying Server...')
		#GAME.DestroyServer()

######## Define KV file classes ############################
class BackToMenuButton(Screen):
	
	def changeScreen(self):
		screen_manager.current = 'mainmenufloat'

class ListLabel(Screen):
	pass

class WindowManager(ScreenManager):
	pass

######## Add Screens to the ScreenManager ############################
screen_manager = WindowManager()
screen_manager.add_widget(MainMenuFloat(name='mainmenufloat'))
screen_manager.add_widget(CreateServerMenuFloat(name='createservermenufloat'))
screen_manager.add_widget(SearchForLobbiesMenuFloat(name='searchforlobbiesmenufloat'))
screen_manager.add_widget(LobbyMenuFloat(name='lobbymenufloat'))
screen_manager.add_widget(CreateMatchMenuFloat(name='creatematchmenufloat'))
screen_manager.add_widget(SettingsMenuFloat(name='settingsmenufloat'))
screen_manager.add_widget(StatisticsMenuFloat(name='statisticsmenufloat'))
screen_manager.add_widget(AboutMenuFloat(name='aboutmenufloat'))
screen_manager.add_widget(GameStartMenu(name='gamestartmenu'))
screen_manager.add_widget(PauseMenu(name='pausemenu'))
screen_manager.add_widget(ConnectionLostMenuFloat(name='connectionlostmenufloat'))
screen_manager.add_widget(GameOverMenu(name='gameovermenu'))

class MenuApp(App):

	def build(self):
		Window.clearcolor = (0.2, 0.4, 0.7, 1)
		return screen_manager

if __name__ == '__main__':
	MenuApp().run()

######## Errora and Handlers ############################
def ErrorPopup(sender, msg):

	popup = Popup(title='ERROR', content=Label(text = msg ), size_hint=(None, None), size=(400, 400))

	popup.open()

CLIENT.EError += ErrorPopup

def handle_ematchJoined(sender, matchname):

	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	logging.info('EMatchJoined received by client %s' % timestamp)
	# popup = Popup(title='Match Joined', content=Label(text = 'Waiting for %s to start...' % matchname), size_hint=(None, None), size=(400, 400), auto_dismiss=True)

	# popup.open()

CLIENT.EMatchJoined += handle_ematchJoined

def handle_ematchStarted(sender):

	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	logging.info('EMatchStarted received by client %s' % timestamp)
	screen_manager.current = 'gamestartmenu'
	GameApp(client=CLIENT).run()

CLIENT.EMatchStarted += handle_ematchStarted
