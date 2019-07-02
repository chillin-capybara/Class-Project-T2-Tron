from kivy.app import App
from kivy.graphics import *
from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock
from Backend.Core.Vect2D import Vect2D
from Backend.Classes.Game import Game
from Backend.Classes.GameClient import GameClient
from Backend.Classes.Arena import Arena
from Backend.Classes.HumanPlayer import HumanPlayer

from UI.Widgets.CountdownWidget import CountdownWidget
from UI.Widgets.TrackWidget import TrackWidget
from UI.Widgets.MyKeyboardListener import MyKeyboardListener
from UI.Widgets.PlayerWidget import PlayerWidget
from Backend.Classes.GameClient import GameClient

import logging

# setting display size to 500, 500
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

# Not using kv files for logic reasons, maybe temporary
Builder.load_string("""
<GameUI>:
    # Creates Button, where you are able to start the countdown
    Button:
        id: StartButton
        text: "Start"
        pos: 250, 250
        size: 100, 30
        opacity: 1 if root.countdown_is_running == False and root.game_is_running == False else 0
        on_press:
            root.countdown_is_running = True
            countdown.start()


    # initializes the countdown feature
    CountdownWidget:
        id: countdown
        opacity: 1 if root.countdown_is_running else 0
        pos: 0, 0
        size: root.size
        start_value: 2
        on_finished:
            root.do_finished()

    # kv file for the track representation
    AnchorLayout:
        size: root.size
        anchor_x: "center"
        anchor_y: "center"
        TrackWidget:
            id: trackWidget
            size: root.size
            playerList: root.playerList

    # kv file for displaying all ingame players with colors

    AnchorLayout:
        size: root.size
        anchor_x: "right"
        anchor_y: "top"
        PlayerWidget:
            id: playerWidget
            pos: 0, 0
            size: root.getPlayerWidgetSize()
            size_hint: None, None
            playerList: root.playerList
            # game: root.game
""")






## Static global defined values
UPDATES_PER_SECOND = 3
# FIELDSIZE = Arena.getSize()
FIELDSIZE = (100, 100)
TRACKSIZE = 1
HEADSIZE = 1


# GAME.setPlayerName("Its me")
# p1 = HumanPlayer()
# p1.setName("Simon")
# p1.setColor((1, 1, 0))
# p1.setPosition(10, 10)
# p1.addTrack(Vect2D(10, 10), Vect2D(20, 10))
# p1.setVelocity(0,1)

# # p1.addTrack(Vect2D(20, 10), Vect2D(20, 20))

# p2 = HumanPlayer()
# p2.setName("Lorenz")
# p2.setColor((0, 1, 1))
# p2.setPosition(30, 40)
# p2.addTrack(Vect2D(30, 40), Vect2D(45, 40))
# p2.addTrack(Vect2D(45, 40), Vect2D(45, 45))
# p2.addTrack(Vect2D(45, 45), Vect2D(100, 45))
# p2.setVelocity(1, 0)

# p3 = HumanPlayer()
# p3.setName("Marcell")
# p3.setColor((1, 0, 1))
# p3.setPosition(70, 40)
# p3.addTrack(Vect2D(70, 40), Vect2D(80, 40))
# p3.addTrack(Vect2D(80, 40), Vect2D(10, 40))
# p3.addTrack(Vect2D(10, 60), Vect2D(30, 60))
# p3.setVelocity(0, 1)
#players = [CLIENT.me]
players = []
logging.info("GameApp loaded")
# GAME.UpdatePlayers("TMP_TESTING", [p1, p2, p3])

class GameUI(Widget):
    playerList = ListProperty(players)
    # game = ObjectProperty(GAME)
    # print(GAME.getPlayers())
    
    ## Values for later use in functions
    countdown_is_running = BooleanProperty(False)
    game_is_running = BooleanProperty(False)
    playPos = ObjectProperty(Vect2D(10, 0))

    __client : GameClient = None


    def __init__(self, **kwargs):
        self.__client = kwargs['client']
        players = self.__client.match.players
        self.playerList = ListProperty(players)
        self.__client.me.setPosition(20,20)
        self.__client.me.setVelocity(1,0)

        # SET THE STUFF OF the liststs
        players[1].setPosition(20,20)
        players[1].setVelocity(1,0)


        ## creates update function for all uses, ensures synchronized update trigger
        super(GameUI, self).__init__(**kwargs)
        self.update()
        
        Clock.schedule_interval(self.update, 1 / UPDATES_PER_SECOND)
        logging.info("GameApp initialized")


    def update(self, *args):
        ## final update function, where I trigger different functuions
        # self.ids.trackWidget.update()
        self.ids.trackWidget.update()
        
        ## functions should only be started after special event is triggered
        if self.countdown_is_running == True:
            ## Despite trying to handle the information down, I was forced to create new function,
            ## which triggers certain event in subclass
            self.ids.trackWidget.setBooleanCountdown()
            self.ids.trackWidget.increaseOpacity()
        
        ## functions should only be started after special event is triggered
        if self.game_is_running == True:
            ## Despite trying to handle the information down, I was forced to create new function,
            ## which triggers certain event in subclass
            self.ids.trackWidget.setBooleanGame()     
            # p1.move(2)
            # p2.move(1)
            # p3.move(1)       




    def getPlayerWidgetSize(self):
        ## creates the hight for the widget in duty of displaying all players online
        playerCount = len(self.playerList)
        return (100, playerCount * 20)

    def do_finished(self):
        ## event handler, sets the Booleans for opacity
        def callback(_):
            # Countdown abgelaufen
            # Spiel starten ...
            self.countdown_is_running = False
            self.game_is_running = True
            
        ## after specified time callback function is called anbd game starts
        Clock.schedule_once(callback, 0)
        
    def updateUpdater(self):
        self.ids.headWidget.update_screen_size(self.size)


# Entry Point
class GameApp(App):
    __client = None
    def __init__(self, **kwargs):
        self.__client = kwargs['client']
        super().__init__()

    # creates the Application
    def build(self):
        MyKeyboardListener(client=self.__client)
        logging.info("GameApp started!")
        return GameUI(client=self.__client)

if __name__ == "__main__":
    GameApp().run()
