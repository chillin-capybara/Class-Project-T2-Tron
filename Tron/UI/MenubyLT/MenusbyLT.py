# Quelle: https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Create both screens. Please note the root.manager.current: this is how
#you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

Builder.load_file('gameovermenu.kv')
Builder.load_file('connectionlostmenu.kv')
Builder.load_file('searchforservermenu.kv')
Builder.load_file('createservermenu.kv')
Builder.load_file('pausemenu.kv')

#following will come later in the implementation with Oliver
#Builder.load_file('mainmenu.kv')
#Builder.load_file('statisticsmenu.kv')
#Builder.load_file('settingsmenu.kv')
#Builder.load_file('aboutmenu.kv')

#following will come later in the implementation with Ludwig
#Builder.load_file('gamestartmenu')
'''
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'settings'
        Button:
            text: 'Quit'
            on_press: exit() #in future close client and server

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
""")
'''

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
        #    displaytext = 'Please wait for other Players'
        #elif enemies_left == True:
        #    displaytext = 'I am sorry. The other Players left'
        #else:
        #    displatext = 'Server askes you to grab a coffee and wait...'
            
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
        #call starting game function
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

    def getserverOnline(self):
        """
		Get the server which are online

		Args:
			server_ip (list): Time the player was in the game
		Return:
			String
		"""
        #if...
        raise NotImplementedError
    
    def connecttoServer(self, ticketBox):
        """
		Connects to Server

		Args:
			-
		Return:
			-
		"""
        #connect to choosen server
        raise NotImplementedError

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

class StatisticsMenu(Screen):
    pass

class SettingsMenu(Screen):
    pass

class AboutMenu(Screen):
    pass

class GameStartMenu(Screen):
    pass

screen_manager = ScreenManager()
screen_manager.add_widget(GameOverMenu(name='gameovermenu'))
screen_manager.add_widget(ConnectionLostMenu(name='connectionlostmenu'))
screen_manager.add_widget(SearchForServerMenu(name='searchforservermenu'))
screen_manager.add_widget(CreateServerMenu(name='createservermenu'))
screen_manager.add_widget(PauseMenu(name='pausemenu'))
screen_manager.add_widget(MainMenu(name='mainmenu'))
screen_manager.add_widget(StatisticsMenu(name='statisticsmenu'))
screen_manager.add_widget(SettingsMenu(name='settingsmenu'))
screen_manager.add_widget(AboutMenu(name='aboutmenu'))
screen_manager.add_widget(GameStartMenu(name='gamestartmenu'))


class MenusbyLT(App):

    def build(self):
        Window.clearcolor = (1, 1, 1 , 1)
        return screen_manager

if __name__ == '__main__':
    MenusbyLT().run()