# Quelle: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
import re
#from ..mainUI import GameApp, GameUI
from Backend.Classes.Game import Game

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
Builder.load_file('kvfilesmenu/searchforservermenufloat.kv')

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
		self.ids.colorLabel.text=sol
		self.ids.colorButton.background_color=color


class AboutMenu(Screen):
    pass

class GameStartMenu(Screen):

	def destroyserver(self):

		GAME.DestroyServer()


###################################################################
class BackToMenuButton(Screen):
	
	def changeScreen(self):
		screen_manager.current = 'mainmenu'

class IPTextInput(TextInput):
	validated = BooleanProperty(False)

class PortTextInput(TextInput):
	validated = BooleanProperty(False)

class IPInput(FloatLayout):
	bubble_showed = True
	def __init__(self, **kwargs):
		super(IPInput, self).__init__(**kwargs)
		self.input = IPTextInput()
		self.input.bind(text=self.validate)
		self.add_widget(self.input)
		self.bubble = ValidateIPLabel()
		self.add_widget(self.bubble)
	def validate(self, input, value):
		self.bubble.ids.label.text = "IP needs to look like 123.456.789.897"
		try:
			iplist = value.split(".")
			print(iplist)
			for e in iplist:
				if value == "":
					self.bubble.ids.label.text = "IP needs to look like 123.456.789.897"
					status = False
				elif len(e) == 3 and len(iplist) == 4:
					print("Schleife länge 3")
					status = True
				elif len(iplist) != 4:
					print("Länge nicht vier")
					status = False
					self.bubble.ids.label.text = "Input must be an valid IP"
				else:
					status = False
					self.bubble.ids.label.text = "Input must be an valid IP"

		except Exception as e:
			status = False
			self.bubble.ids.label.text = "Input must be an valid IP"	
		
		if value == '':
			self.input.validated = False
			self.remove_widget(self.bubble)
			self.bubble_showed = False
		
		if not status:
			if not self.bubble_showed:
				self.input.validated = False
				self.add_widget(self.bubble)
				self.bubble_showed = True
		else:
			print("bubble removed")
			self.input.validated = True
			self.remove_widget(self.bubble)
			self.bubble_showed = False

class PortInput(FloatLayout):
	bubble_showed = True
	def __init__(self, **kwargs):
		super(PortInput, self).__init__(**kwargs)
		self.input = PortTextInput()
		self.input.bind(text=self.validate)
		self.add_widget(self.input)
		self.bubble = ValidatePortLabel()
		self.add_widget(self.bubble)
	def validate(self, input, value):
		self.bubble.ids.label.text = 'IP needs to look like 123.456.789.897'
		try:
			portnumber = int(value)
			print(portnumber)
			if 1024 >= portnumber or portnumber >= 65535:
				self.bubble.ids.label.text = 'Please enter a valid port'
				status = False
				print('Wrong Port')
			else:
				status = True
				print('Right Port')
		except Exception:
			status = False
			self.bubble.ids.label.text = 'Input must be an valid port'	
		if not status:
			if not self.bubble_showed:
				self.input.validated = False
				self.add_widget(self.bubble)
				self.bubble_showed = True
		else:
			print("bubble removed")
			self.input.validated = True
			self.remove_widget(self.bubble)
			self.bubble_showed = False

class ValidateIPLabel(Bubble):
	validated = False

class ValidatePortLabel(Bubble):
	validated = False
###################################################################

class SearchForServerMenufloat(Screen):

	ip = '-'
	port = 0

	def debug(self):
		pass

	def updateIP(self, currentip):
		"""
		Sets variable arenatype to 1 or 2

		Args:
			Arenatype (int):
		Return:
			arenatype
		"""
		self.currentip = currentip

		self.serverip = int(self.currentip)
		
		print('IP %s has been choosen.' % (self.serverip), flush = True)
		return self.serverip

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

class WindowManager(ScreenManager):
	pass

screen_manager = WindowManager()
screen_manager.add_widget(SearchForServerMenufloat(name='searchforservermenufloat'))
screen_manager.add_widget(MainMenu(name='mainmenu'))
screen_manager.add_widget(GameOverMenu(name='gameovermenu'))
screen_manager.add_widget(ConnectionLostMenu(name='connectionlostmenu'))
screen_manager.add_widget(SearchForServerMenu(name='searchforservermenu'))
screen_manager.add_widget(CreateServerMenu(name='createservermenu'))
screen_manager.add_widget(PauseMenu(name='pausemenu'))
screen_manager.add_widget(StatisticsMenu(name='statisticsmenu'))
screen_manager.add_widget(SettingsMenu(name='settingsmenu'))
screen_manager.add_widget(AboutMenu(name='aboutmenu'))
screen_manager.add_widget(GameStartMenu(name='gamestartmenu'))


class MenuApp(App):

	def build(self):
		Window.clearcolor = (0.5, 0.5, 1 , 1)
		return screen_manager

if __name__ == '__main__':
	MenuApp().run()