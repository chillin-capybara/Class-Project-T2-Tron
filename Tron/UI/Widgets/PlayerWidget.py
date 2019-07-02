from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.graphics import *
import UI.mainUI

from Backend.Classes.HumanPlayer import HumanPlayer
from Backend.Classes.Client import Client
from Backend.Classes.Game import Game
from Backend.Classes.Player import Player

Builder.load_string("""
<PlayerWidget>:
    ## BoxLayout used for increasing playercount
    BoxLayout:
        id: boxLayout1
        orientation: "vertical"
""")

class PlayerWidget(Widget):
<<<<<<< HEAD
    playerList = ListProperty()

=======
    playerList = ListProperty([])
    game = ObjectProperty()
    print(game)
>>>>>>> 5cd7da4e97c97b4d12fb51499982b74aa3456e2f
    def on_playerList(self, instance, value):
        ## function for creating the input for the BoxLayout, capable of printing the text + the color of the player
        self.ids.boxLayout1.clear_widgets()
        for player in value:
            print(self.playerList)
            self.ids.boxLayout1.add_widget(Label(
                text = player.getName(),
                color = [*player.getColor(), 1]
            ))
    
  