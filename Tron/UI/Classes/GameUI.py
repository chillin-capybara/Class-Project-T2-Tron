import sys

from kivy.app import App
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty

from Tron.Backend.Classes.Player import Player
from Tron.Backend.Classes.Factory import Factory
# from ...Backend.Core.Vect2D import Vect2D
# from ...Backend.Classes.Track import Track
# from ...Backend.Classes.Player import Player
# from ...Backend.Classes.Factory import Factory



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



class IncrediblyCrudeClock(Label):
    """
    a class for a countdown starting at 5, this is used for the reason that all players can start to look at the game
    """
    a = NumericProperty(5)  # seconds
    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)


