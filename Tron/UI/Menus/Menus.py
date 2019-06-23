# Quelle: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
#from ..mainUI import GameApp


import sys
print(sys.path)

#Builder.load_file('UI/MenusbyLT/kvfilesmenu/gameovermenu.kv')
#Builder.load_file('../kvfilesmenu/connectionlostmenu.kv')
Builder.load_file('kvfilesmenu/searchforservermenu.kv')
Builder.load_file('./kvfilesmenu/createservermenu.kv')
Builder.load_file('../../kvfilesmenu/pausemenu.kv')
Builder.load_file('../../kvfilesmenu/mainmenu.kv')
Builder.load_file('../../kvfilesmenu/statisticsmenu.kv')
Builder.load_file('../../kvfilesmenu/settingsmenu.kv')
Builder.load_file('../../kvfilesmenu/aboutmenu.kv')
Builder.load_file('../../kvfilesmenu/gamestartmenu.kv')

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
		raise NotImplementedError

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
        #call starting game function
        raise NotImplementedError

class SearchForServerMenu(Screen):

	ip = '-'
	port = 0

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

		#start_game = GameApp()
		#start_game.run()
		return self.inputIp, self.inputPort


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
			self.ids.connectiontoserverButton.text = output
		
		elif inputPort:
			output = 'Connect to the Server with IP %s and Port %s' % (self.inputIp, self.inputPort)
			self.ids.connectiontoserverButton.text = output

		else:
			pass

class CreateServerMenu(Screen):

	def startGame(self):
		"""
		Send Startsignal to server and begin countdown

		Args:
			-
		Return:
			-
		"""
		#call starting game function
		raise NotImplementedError

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
		raise NotImplementedError

	def startGame(self):
		"""
		Send Startsignal to server and begin countdown

		Args:
			-
		Return:
			-
		"""
		#call starting game function
		raise NotImplementedError

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
	def changedifficulty(self,choice):
		self.ids.difficultyendLabel.text=choice

class StatisticsMenu(Screen):
    pass

class AboutMenu(Screen):
    pass

class GameStartMenu(Screen):
    pass

screen_manager = ScreenManager()
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


class Menus(App):

	def build(self):
		Window.clearcolor = (0.5, 0.5, 1 , 1)
		return screen_manager

if __name__ == '__main__':
	Menus().run()