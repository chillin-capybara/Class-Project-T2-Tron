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
    BoxLayout:
        id: boxLayout1
        orientation: "vertical"
""")

class PlayerWidget(Widget):
    playerList = ListProperty()

    def on_playerList(self, instance, value):
        self.ids.boxLayout1.clear_widgets()

        
        for player in value:

            # colorId = player[1]
            
            self.ids.boxLayout1.add_widget(Label(
                text = player["name"],
                color = self.getColorFromId(player["color"])
            ))
    
    def getColorFromId(self, colorId):
        switcher = {
            0: (1, 0, 0, 1),
            1: (0, 1, 0, 1),
            2: (0, 0, 1, 1),
            3: (0, 1, 1, 1),
            4: (1, 1, 0, 1),
            5: (1, 0, 1, 1),
        }

        return switcher.get(colorId, (1, 1, 1, 1))