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


from UI.Widgets.CountdownWidget import CountdownWidget
from UI.Widgets.TrackWidget import TrackWidget
from UI.Widgets.MyKeyboardListener import MyKeyboardListener
from UI.Widgets.PlayerWidget import PlayerWidget


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
            
    Button:
        id: Pause Button
        text: "Pause"
        pos: 500, 500
        size: 100, 30
        opacity: 1 if root.game_is_running else 0
        on_press:
            root.game_is_running = False


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

    # kv file for displaying all ingame players with colors

    AnchorLayout:
        size: root.size
        anchor_x: "right"
        anchor_y: "top"
        PlayerWidget:
            id: playerWidget0
            pos: 0, 0
            size: root.getPlayerWidgetSize()
            size_hint: None, None
            playerList: root.playerList

    AnchorLayout:
        size: root.size
        anchor_x: "center"
        anchor_y: "center"
        HeadWidget:
            id: headWidget
            size: root.size
""")


## Static global defined values
UPDATES_PER_SECOND = 5
FIELDSIZE = (100, 100)
HEADSIZE = 1
TRACKSIZE = 1

print("GAME CREATED...", flush=True)
# Define global GAME object
CLIENT = GameClient()
CLIENT.me.setName("Peter")
CLIENT.me.setColor((1, 1, 0))
CLIENT.me.setVelocity(1, 0)
CLIENT.me.setPosition(20, 20)
# ANFANGSPOS = CLIENT.me.getPosition()

class GameUI(Widget):

    # playerList = ListProperty(CLIENT.getPlayers())
    
    playerList = ListProperty([
        {
            "name": "Simon",
            "color": (1, 0, 0, 1)
        },
        {
            "name": "Ludi",
            "color": (0, 1, 0, 1)

        },
        {
            "name": "Dani",
            "color": (0, 0, 1, 1)

        }
    ])

    ## Values for later use in functions
    countdown_is_running = BooleanProperty(False)
    game_is_running = BooleanProperty(False)
    playPos = ObjectProperty(Vect2D(10, 0))


    def __init__(self, **kwargs):
        ## creates update function for all uses, ensures synchronized update trigger
        super(GameUI, self).__init__(**kwargs)
        self.update()
        Clock.schedule_interval(self.update, 1 / UPDATES_PER_SECOND)



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
    # creates the Application
    def build(self):
        MyKeyboardListener()
        return GameUI()

if __name__ == "__main__":
    GameApp().run()
