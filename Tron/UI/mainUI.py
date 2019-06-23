from kivy.app import App
from kivy.graphics import *
from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from Backend.Core.Vect2D import Vect2D

from UI.Widgets.CountdownWidget import CountdownWidget
from UI.Widgets.TrackWidget import TrackWidget


# setting display size to 500, 500
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

Builder.load_string("""
<GameUI>: 
    Button:
        text: "Start"
        pos: 0, 0
        size: 100, 30
        opacity: 1 if root.countdown_is_running == False and root.game_is_running == False else 0
        on_press:  
            root.countdown_is_running = True
            countdown.start()

    CountdownWidget:
        id: countdown
        opacity: 1 if root.countdown_is_running else 0
        pos: 0, 0
        size: root.size
        start_value: 2
        on_finished: 
            root.do_finished()         
            trackWidget.startTrack()

    TrackWidget:
        id: trackWidget
        size: root.size
        opacity: 1 if root.game_is_running else 0
""")


class GameUI(Widget):
    countdown_is_running = BooleanProperty(False)
    game_is_running = BooleanProperty(False)
    playPos = ObjectProperty(Vect2D(10, 0))

    def do_finished(self):
        def callback(_):
            # Countdown abgelaufen
            # Spiel starten ...
            self.countdown_is_running = False
            self.game_is_running = True


        Clock.schedule_once(callback, 2)



# Entry Point
class GameApp(App):
    def build(self):
        return GameUI()

if __name__ == "__main__":
    GameApp().run()