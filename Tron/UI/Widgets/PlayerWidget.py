from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation


from ...Backend.Classes.Client import Client
from ...Backend.Classes.Game import Game




Builder.load_string("""
<PlayerWidget>:
    AnchorLayout:
        size: root.size
        anchor_x: "center"
        anchor_y: "center"
        Label:
            # size: self.texture_size
            id: PlayerWidget0
            valign: "middle"
            halign: "center"
            color: 1, 1, 1, 1
            text_size: root.width, None
            text: 
                root.getPlayerList()[0] 
                
""")

class PlayerWidget(App, BoxLayout):
    
    playersOnline  = ListProperty([])
    playersColor = ListProperty([])
    def getPlayerList(self):
        # self.playersOnline = Game.getPlayers()
        self.playersOnline = ['Me' , 'You']
        return self.playersOnline
    def getPlayerColor(self):
        # self.playersColor = Game.getColor()
        self.playersColor = []
        self.playersOnline2 = ['Me' , 'You']
        for x in self.playersOnline2:
            self.playersColor.append(Player(x).getColor())

            if x == "":
                break

    def build(self):
        return self
    