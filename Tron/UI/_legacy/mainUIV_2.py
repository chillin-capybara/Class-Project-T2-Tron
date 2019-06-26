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

from UI.Widgets.CountdownWidget import CountdownWidget
from UI.Widgets.TrackWidget import TrackWidget
from UI.Widgets.TrackWidget import MyKeyboardListener
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
            root.slowStartopacity()
            

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
            opacity:  root.slowStartopacity() if root.countdown_is_running else 1
            #(root.slowStartopacity()) if root.countdown_is_running else 0 #  1 if root.game_is_running else 0

        # linepoints: root.linepoints
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
""")



updatesPerSeconds = 50

class GameUI(Widget): 
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
    opacityValue = NumericProperty(0)
    opacityValue = 0
    
    
   
    def __init__(self, **kwargs):
        ## creates update function for all uses, ensures synchronized update trigger
        super(GameUI, self).__init__(**kwargs)
        self.update()
        Clock.schedule_interval(self.update, 1 / updatesPerSeconds)
    
    
    def update(self, *args):
        ## final update function, where I trigger different functuions
        self.ids.trackWidget.update()
        TrackWidget.updateVelocity(self)
        # self.slowStartopacity()

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
            # self.game_is_running = MyKeyboardListener._on_keyboard_down
            self.opacityValue2 = self.slowStartopacity()
            
        ## after specified time callback function is called anbd game starts
        Clock.schedule_once(callback, 0)

    def slowStartopacity(self):
        ## function for creating an increasing opacity with increasing time
        ## Fr. S.
        if self.opacityValue < 1:
            self.opacityValue += (1/updatesPerSeconds)
            print (self.opacityValue)
            return self.opacityValue
    








# Entry Point
class GameApp(App):
    # creates the Application
    def build(self):
        game = GameUI()
        MyKeyboardListener(game)
        return game

if __name__ == "__main__":
    GameApp().run()
