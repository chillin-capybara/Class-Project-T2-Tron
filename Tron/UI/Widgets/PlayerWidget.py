from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation


from Backend.Classes.Client import Client
from Backend.Classes.Game import Game




Builder.load_string("""
<PlayerWidget>:
# Widget representing the Players online
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
            # trying to get a list over several lines with players...
            text: 
                root.getPlayerList()[0]  
            
""")

class PlayerWidget(App, BoxLayout):
    
    playersOnline  = ListProperty([])
    playersColor = ListProperty([])
    def getPlayerList(self):
        # function getting the players list
        # self.playersOnline = Game.getPlayers()
        self.playersOnline = ['Me' , 'You']
        return self.playersOnline
    def getPlayerColor(self):
        # function getting the players color by checking each entry in playersOnline List and creating 
        # a new list which first entry is the color of the first player in the playersOnline List
        # self.playersColor = Game.getColor()
        self.playersColor = []
        self.playersOnline2 = ['Me' , 'You']
        for x in self.playersOnline2:
            self.playersColor.append(x.getColor())

            if x == "":
                break

    def build(self):
        return self
    