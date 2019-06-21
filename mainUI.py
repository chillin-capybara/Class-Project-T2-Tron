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
from Tron.Backend.Core.Vect2D import Vect2D

from Tron.UI.Widgets.CountdownWidget import CountdownWidget


# setting display size to 500, 500
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

Builder.load_string("""
<GameUI>: 
    Button:
        text: "Start"
        pos: 0, 0
        size: 100, 30
        on_press:  
            root.is_running = True
            countdown.start()

    CountdownWidget:
        id: countdown
        opacity: 1 if root.is_running else 0
        pos: 0, 0
        size: root.size
        start_value: 2
        on_finished: root.do_finished()           
""")


class GameUI(Widget): 
    is_running = BooleanProperty(False)
    playPos = ObjectProperty(Vect2D(10, 0))

    def do_finished(self):
        def callback(_):
            self.is_running = False
            # Countdown abgelaufen
            # Spiel starten ...

        Clock.schedule_once(callback, 2)



# Entry Point
class GameApp(App):
    def build(self):
        return GameUI()

if __name__ == "__main__":
    GameApp().run()