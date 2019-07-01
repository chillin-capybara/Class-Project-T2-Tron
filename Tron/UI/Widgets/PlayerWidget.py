from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.graphics import *


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
    # self._game = UI.mainUI.GAME
    # player
    playerList = ListProperty()

    def on_playerList(self, instance, value):
        ## function for creating the input for the BoxLayout, capable of printing the text + the color of the player
        self.ids.boxLayout1.clear_widgets()
        for player in value:
            self.ids.boxLayout1.add_widget(Label(
                text = player["name"],
                color = player["color"]
            ))
    
  