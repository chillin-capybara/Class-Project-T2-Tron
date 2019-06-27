from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.animation import Animation
from kivy.graphics import *
from kivy.vector import Vector

from kivy.clock import Clock
import random
import math

from Backend.Classes.HumanPlayer import HumanPlayer
from Backend.Core.Vect2D import Vect2D
from Backend.Classes.Game import Game
from Backend.Classes.Player import Player

from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget


class HeadWidget(Widget):
    p1 = HumanPlayer()
    p1.setName("Simon")
    p1.setColor((1, 1, 1))
    p1.setPosition(20, 20)
    p1.addTrack(Vect2D(10, 10), Vect2D(20, 10))
    p1.addTrack(Vect2D(20, 10), Vect2D(20, 20))

    p2 = HumanPlayer()
    p2.setName("Ludi")
    p2.setColor((1, 1, 1))
    p2.setPosition(50, 50)
    p2.addTrack(Vect2D(40, 40), Vect2D(45, 40))
    p2.addTrack(Vect2D(45, 40), Vect2D(45, 45))
    p2.addTrack(Vect2D(45, 45), Vect2D(100, 45))

    players = [ p1, p2 ]

    

    def update(self):
        ## function for updating the track
        fieldsize = (100, 100)
        self.canvas.clear()
        players2 = HeadWidget.players
        

        with self.canvas:

            for player in players2:
                track = player.getPosition()
                veloctiy = player.getVelocity()

                colorId = player.getColor()
                Color(rgb = self.getColorFromId(colorId))

            
                xPos = track.x
                yPos = track.y
                xPos2 = (self.size[0]/fieldsize[0]) * xPos
                yPos2 = (self.size[1]/fieldsize[1]) * yPos

                # Rectangle(pos=(xPos2, yPos2), size = ((self.size[0]/fieldsize[0])*5, (self.size[1]/fieldsize[1])*5) )

        # with self.canvas:
        #     for player in players2:
        #         startpos = player.getPosition()
        #         xPos = startpos[0]
        #         yPos = startpos[1]
        #         Triangle(size_hint=(0.5, 0.5))



    def getColorFromId(self, colorId):
        ## remove
        switcher = {
            0: (1, 0, 0),
            1: (0, 1, 0),
            2: (0, 0, 1),
            3: (0, 1, 1),
            4: (1, 1, 0),
            5: (1, 0, 1),
        }

        return switcher.get(colorId, (1, 1, 1, 1))

  
   

    
