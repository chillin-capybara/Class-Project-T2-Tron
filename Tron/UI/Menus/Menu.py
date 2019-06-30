# Quelle: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
#from ..mainUI import GameApp, GameUI
from Backend.Classes.Game import Game
import re
GAME = Game()

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
		start_game = GameApp()
		start_game.run()

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
		start_game = GameApp()
		start_game.run()

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
		GAME.CreateServer('', 9876, self.numberplayer)
		print('Arenatype: %d, Diffculty: %d and %d Players to play have been choosen.' % (self.arena, self.difficulty, self.numberplayer), flush = True)

	def destroyServer(self):

		print('Destroying Server...')
		GAME.DestroyServer()


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
		GAME.setPlayerName(playername)
		GAME.setColor(color)
		# TODO IMPLEMENT RGB Color picker

		print("Playername changed to: %s" % playername)
		print("Color changed to %s" % str(color))


class StatisticsMenu(Screen):
	def refreshstats(self,test):
		print("Updating screen... %s" % test)
		print("PLAYERNAME: %s" % GAME.getPlayerName())

		outputname = 'Name: %s' % (GAME.getPlayerName())
		print(outputname, flush= True)
		self.ids.nameLabel.text = outputname

		color = GAME.getColor()
		sol = "Color: %s" % str(color)
		print(sol)
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.colorLabel.text=sol
		self.ids.showcolorLabel.background_color=playercolor


class AboutMenu(Screen):
    pass

class GameStartMenu(Screen):

	def destroyserver(self):

		GAME.DestroyServer()

####################################################################
##Main Manu New version
class MainMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Search for Lobbies Menu Float version
class SearchForLobbiesMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Lobby Menu
class LobbyMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Create Match Menu Flaot version
class CreateMatchMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Connection Lost Manu Float version
class ConnectionLostMenuFloat(Screen):
	pass
####################################################################
####################################################################
##Define KV file Buttons
class BackToMenuButton(Screen):
	
	def changeScreen(self):
		screen_manager.current = 'mainmenu'
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
		start_game = GameApp()
		start_game.run()

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
		GAME.CreateServer('', 9876, self.numberplayer)
		print('Arenatype: %d, Diffculty: %d and %d Players to play have been choosen.' % (self.arena, self.difficulty, self.numberplayer), flush = True)

	def destroyServer(self):

		print('Destroying Server...')
		GAME.DestroyServer()
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