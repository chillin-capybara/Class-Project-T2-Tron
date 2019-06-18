from kivy.app import App
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from Player import Player
from Track import Track
from ..Core.Vect2D import Vect2D
from Factory import Factory

player1 = Factory.Player("Marcell", 2)
player1.getTrack().addElement(Vect2D(0,0), Vect2D(100,100))
player1.getTrack().addElement(Vect2D(100,100), Vect2D(250,140))
player1.getTrack().addElement(Vect2D(250,140), Vect2D(0,0))
linepoints = player1.getTrack().getLine()
class MyWidget(Widget):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.draw_my_stuff()
        
    def draw_my_stuff(self):
        self.canvas.clear()
        with self.canvas:
            # draw a line using the default color
            self.line = Line(points = linepoints, width = 2)
class TrackApp(App):
    def build(self):
        game = MyWidget()
        return game

TrackApp().run()