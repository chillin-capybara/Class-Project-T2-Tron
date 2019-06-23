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
from Tron.Backend.Core.Vect2D import Vect2D

from Tron.UI.Widgets.CountdownWidget import CountdownWidget
from Tron.UI.Widgets.TrackWidget import TrackWidget
from Tron.UI.Widgets.PlayerWidget import PlayerWidget


# setting display size to 500, 500
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

# Not using kv files for logic reasons, maybe temporary
Builder.load_string("""
<GameUI>: 
    # Creates Button, where you are able to start the countdown
    Button:
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
            trackWidget.startTrack()

    # kv file for the track representation
    TrackWidget:
        id: trackWidget
        size: root.size
        opacity: 1 if root.game_is_running else 0
    # kv file for displaying all ingame players with colors
    PlayerWidget:
        id: playerWidget0
        size: root.getplayerWidgetSize()[0], root.getplayerWidgetSize()[1]
        opacity: 1
        pos: 60, 400
""")


class GameUI(Widget): 
    countdown_is_running = BooleanProperty(False)
    game_is_running = BooleanProperty(False)
    playPos = ObjectProperty(Vect2D(10, 0))
    playerWidgetSize = ListProperty([]) 
    labelHeight = NumericProperty()
    def getplayerWidgetSize(self):
        # creates the hight for the widget in duty of displaying all players online
        self.playerWidgetSize = [500 , 200]
        # self.labelHeight = 3.0
        # len(Game.getPlayers())
        # self.playerWidgetSize = [int(labelHeight*100) , 100]
        return self.playerWidgetSize

    def do_finished(self):
        # event handler, sets the Booleans for opacity
        def callback(_):
            # Countdown abgelaufen
            # Spiel starten ...
            self.countdown_is_running = False
            self.game_is_running = True

        # after specified time callback function is called anbd game starts
        Clock.schedule_once(callback, 0.5)



# Entry Point
class GameApp(App):
    # creates the Application
    def build(self):
        return GameUI()

if __name__ == "__main__":
    GameApp().run()
