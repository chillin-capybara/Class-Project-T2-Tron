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
##import own modules
#from ..mainUI import GameApp, GameUI
from Backend.Classes.GameClient import GameClient
from collections import namedtuple
from Backend.Classes.GameServer import GameServer

CLIENT = GameClient()

Builder.load_file('kvfilesmenu/gameovermenu.kv')
Builder.load_file('kvfilesmenu/connectionlostmenu.kv')
Builder.load_file('kvfilesmenu/searchforservermenu.kv')
Builder.load_file('kvfilesmenu/createservermenu.kv')
Builder.load_file('kvfilesmenu/pausemenu.kv')
Builder.load_file('kvfilesmenu/mainmenu.kv')
Builder.load_file('kvfilesmenu/statisticsmenu.kv')
Builder.load_file('kvfilesmenu/settingsmenu.kv')
Builder.load_file('kvfilesmenu/aboutmenu.kv')
Builder.load_file('kvfilesmenu/gamestartmenu.kv')
Builder.load_file('kvfilesmenu/connectionlostmenufloat.kv')
Builder.load_file('kvfilesmenu/searchforservermenufloat.kv')
Builder.load_file('kvfilesmenu/createservermenufloat.kv')
Builder.load_file('kvfilesmenu/searchforlobbiesmenufloat.kv')
Builder.load_file('kvfilesmenu/lobbymenufloat.kv')
Builder.load_file('kvfilesmenu/creatematchmenufloat.kv')
Builder.load_file('kvfilesmenu/mainmenufloat.kv')
Builder.load_file('kvfilesmenu/globalcustomwidgets.kv')

def ErrorPopup(sender, msg):

	popup = Popup(title='ERROR', content=Label(text = msg ), size_hint=(None, None), size=(400, 400))

	popup.open()

CLIENT.EError += ErrorPopup

def handle_ematchJoined(sender, matchname):

	popup = Popup(title='Match Joined', content=Label(text = 'Waiting for %s to start...' % matchname), size_hint=(None, None), size=(400, 400), auto_dismiss=False)

	popup.open()

CLIENT.EMatchJoined += handle_ematchJoined

def handle_ematchStarted(sender):

	screen_manager.current = 'gamestartmenu'
	#CLIENT.me.startgame

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

class ConnectionLostMenu(Screen):

	#Fehlt: Game Start Button

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

class SearchForServerMenu(Screen):

	ip = '-'
	port = 0

	def debug(self, inpt):

		self.inpt = str(inpt)

		print(self.inpt)

	def getserverOnline(self):
		"""
		Get the server which are online

		Args:
			server_ip (list): Time the player was in the game
		Return:
			String
		"""
		
		raise NotImplementedError

	def connecttoServer(self, inputIp, inputPort):
		"""
		Sends IP and Port to Server

		Args:
			inputIp (str):
			inputPort (str):
		Return:
			inputIp (str):
			inputPort (int):
		"""

		self.inputIp = inputIp
		self.inputPort = int(inputPort)

		#GAME.ConnectToServer(self.inputIp, self.inputPort)
		print('Connect to Server with IP: %s and Port: %d' % (self.inputIp, self.inputPort))


	def updateconnecttoserverButton(self, inputIp, inputPort):
		"""
		Takes IP from Input at Search for Server Menu

		Args:
			inputIp (str):
			inputPort (str):
		Return:
			change String in connectinotoserverButton
		"""
		self.inputIp = inputIp
		self.inputPort = inputPort
		if inputIp:
			output = 'Connect to the Server with IP %s and Port %s' % (self.inputIp, self.inputPort)
			self.ids.connecttoserverButton.text = output
		
		elif inputPort:
			output = 'Connect to the Server with IP %s and Port %s' % (self.inputIp, self.inputPort)
			self.ids.connecttoserverButton.text = output

		else:
			pass

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

class CreateServerMenu(Screen):
	arena = 1
	difficulty = 1


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

class MainMenu(Screen):
    pass

class SettingsMenu(Screen):

	nameplayer, colorplayer = 'Seppl', 1
	
	def savechanges(self, playername: str, color: tuple):
		"""
		Set the Player Name 
		TODO(+color needs to be implemented)

		Args:
			playername (str): new playername
		TODO(playercolor (int): new playercolor)
		Return:
			-
		"""
		# Save the name and the color
		#GAME.setPlayerName(playername)
		#GAME.setColor(color)
		# TODO IMPLEMENT RGB Color picker

		print("Playername changed to: %s" % playername)
		print("Color changed to %s" % str(color))


class StatisticsMenu(Screen):
	def refreshstats(self,test):
		print("Updating screen... %s" % test)
		#print("PLAYERNAME: %s" % GAME.getPlayerName())

		#outputname = 'Name: %s' % (GAME.getPlayerName())
		print(outputname, flush= True)
		self.ids.nameLabel.text = outputname

		#color = GAME.getColor()
		sol = "Color: %s" % str(color)
		print(sol)
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.colorLabel.text=sol
		self.ids.showcolorLabel.background_color=playercolor


class AboutMenu(Screen):
    pass

class GameStartMenu(Screen):

	def destroyserver(self):
		pass

####################################################################
##Main Manu New version
class MainMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Search for Lobbies Menu Float version
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

####################################################################
####################################################################
##Lobby Menu
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
####################################################################
####################################################################
##Create Match Menu Flaot version
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
				self.openBubble(lastcharacter)
				rightstring = self.inpt[:-1]
				self.ids.gamenameTextInput.text = rightstring

		except Exception as e:
			logging.warning(str(e))

	def openBubble(self, character):

		#arrow_pos='top_mid', text='Character %s is not allowed' % character
		self.bubble = Bubble()

		self.add_widget(self.bubble)
		time.sleep(1)
		self.bubble.clear_widgets()

####################################################################
####################################################################
##Connection Lost Manu Float version
class ConnectionLostMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Define KV file classes
class BackToMenuButton(Screen):
	
	def changeScreen(self):
		screen_manager.current = 'mainmenu'

class ListLabel(Screen):
	pass

# class ematchJoinedPopup(Popup):
# 	pass
####################################################################
####################################################################
##Search For Server Menu Float version
class SearchForServerMenuFloat(Screen):

	ip = '-'
	port = 0

	def getPlayerdata(self,test):
		print("Updating screen... %s" % test)
		print("PLAYERNAME: %s" % GAME.getPlayerName())

		outputname = GAME.getPlayerName()
		print(outputname, flush= True)
		self.ids.explainmenuLabel.text = ('Here you can connect to the Server as %s' % outputname)

		color = GAME.getColor()
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.explainmenuLabel.background_color=playercolor

	def debug(self, inpt):

		self.inpt = str(inpt)

		print(self.inpt)

	def getserverOnline(self):
		"""
		Get the server which are online

		Args:
			server_ip (list): Time the player was in the game
		Return:
			String
		"""
		
		raise NotImplementedError

	def connecttoServer(self, inputIp, inputPort):
		"""
		Sends IP and Port to Server

		Args:
			inputIp (str):
			inputPort (str):
		Return:
			inputIp (str):
			inputPort (int):
		"""

		self.inputIp = inputIp
		self.inputPort = int(inputPort)

		GAME.ConnectToServer(self.inputIp, self.inputPort)
		print('Connect to Server with IP: %s and Port: %d' % (self.inputIp, self.inputPort))


	def updateconnecttoserverButton(self, inputIp, inputPort):
		"""
		Takes IP from Input at Search for Server Menu

		Args:
			inputIp (str):
			inputPort (str):
		Return:
			change String in connectinotoserverButton
		"""
		self.inputIp = inputIp
		self.inputPort = inputPort
		if inputIp:
			output = 'Connect to the Server with IP %s and Port %s' % (self.inputIp, self.inputPort)
			self.ids.connecttoserverButton.text = output
		
		elif inputPort:
			output = 'Connect to the Server with IP %s and Port %s' % (self.inputIp, self.inputPort)
			self.ids.connecttoserverButton.text = output

		else:
			pass

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

####################################################################
####################################################################
##Creat Server Menu Float version
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


####################################################################

class WindowManager(ScreenManager):
	pass

screen_manager = WindowManager()
screen_manager.add_widget(MainMenu(name='mainmenu'))
screen_manager.add_widget(MainMenuFloat(name='mainmenufloat'))
screen_manager.add_widget(GameOverMenu(name='gameovermenu'))
screen_manager.add_widget(ConnectionLostMenu(name='connectionlostmenu'))
screen_manager.add_widget(SearchForServerMenu(name='searchforservermenu'))
screen_manager.add_widget(CreateServerMenu(name='createservermenu'))
screen_manager.add_widget(PauseMenu(name='pausemenu'))
screen_manager.add_widget(StatisticsMenu(name='statisticsmenu'))
screen_manager.add_widget(SettingsMenu(name='settingsmenu'))
screen_manager.add_widget(AboutMenu(name='aboutmenu'))
screen_manager.add_widget(GameStartMenu(name='gamestartmenu'))
screen_manager.add_widget(ConnectionLostMenuFloat(name='connectionlostmenufloat'))
screen_manager.add_widget(SearchForServerMenuFloat(name='searchforservermenufloat'))
screen_manager.add_widget(CreateServerMenuFloat(name='createservermenufloat'))
screen_manager.add_widget(SearchForLobbiesMenuFloat(name='searchforlobbiesmenufloat'))
screen_manager.add_widget(LobbyMenuFloat(name='lobbymenufloat'))
screen_manager.add_widget(CreateMatchMenuFloat(name='creatematchmenufloat'))

class MenuApp(App):

	def build(self):
		Window.clearcolor = (0.5, 0.5, 1 , 1)
		return screen_manager

if __name__ == '__main__':
	MenuApp().run()