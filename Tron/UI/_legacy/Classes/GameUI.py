import sys

from kivy.app import App
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty


from ...Backend.Core.Vect2D import Vect2D
from ...Backend.Classes.Track import Track
from ...Backend.Classes.Player import Player
from ...Backend.Classes.Factory import Factory



player1 = Factory.Player('Player1', 2)
player1.getTrack().addElement(Vect2D(0,0), Vect2D(100,100))
player1.getTrack().addElement(Vect2D(100,100), Vect2D(250,140))
player1.getTrack().addElement(Vect2D(250,140), Vect2D(0,0))
linepoints = player1.getTrack().getLine()

linepoints = [0, 0, 500, 500, 0,100]
class MyWidget(Widget):
    """
    class for the lines in game
    """
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.draw_my_stuff()
        
    def draw_my_stuff(self):
        self.canvas.clear()
        with self.canvas:
            # draw a line using the default color
            self.line = Line(points = linepoints, width = 2)

class AnzeigespielerKivy(Label):
    """
    class for displaying all active players at the upper right corner
    """
    def start(self):
        return Label()


class ShowStartPoints(): 
    """
    if the game starts the countdown starts, but the players should see their starting positions
    """
    # player1 = Factory.Player("Marcell", 2)
    # StartPoint = player1.getPosition()
    
    def drawStartPoint(Widget):
        return Label        






