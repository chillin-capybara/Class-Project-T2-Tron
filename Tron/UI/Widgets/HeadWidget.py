from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, BooleanProperty
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
import UI.mainUI

from UI.Widgets.TrackWidget import TrackWidget

from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget


class HeadWidget(Widget):
    p1 = HumanPlayer()
    p1.setName("Simon")
    p1.setColor((1, 0, 1))
    p1.setPosition(20, 20)
    p1.addTrack(Vect2D(10, 10), Vect2D(20, 10))
    p1.addTrack(Vect2D(20, 10), Vect2D(20, 20))


    p2 = HumanPlayer()
    p2.setName("Ludi")
    p2.setColor((0, 1, 1))
    p2.setPosition(50, 50)
    p2.addTrack(Vect2D(40, 40), Vect2D(45, 40))
    p2.addTrack(Vect2D(45, 40), Vect2D(45, 45))
    p2.addTrack(Vect2D(45, 45), Vect2D(100, 45))

    players = [ p1, p2 ]
    
    opacityValue = NumericProperty(0)
    game_is_running3 = BooleanProperty(False)
    countdown_is_running3 = BooleanProperty(False)
    velocity = (0, 1)
    nowpoint = (50, 50)

    

    def update(self):
        ## function for updating the head
        self.canvas.clear()
        players2 = HeadWidget.players
        self.increaseOpacity()

        with self.canvas:
            self.opacity = self.opacityValue
            for player in players2:
                

                colorId = player.getColor()
                addOpacity = list(colorId)
                addOpacity.append(self.opacityValue)
                colorID2 = tuple(addOpacity)
                Color(rgb = colorID2)
                # Color(rgb = self.getColorFromId(colorId))
                
                
                
                
                Points = self.calculatePoints(self.velocity, self.nowpoint)
                
            
                Triangle(points = Points, color = colorId)

    

    def calculatePoints(self, velocity, nowpoint):
        ## creating all points requiered for a triangle + detecting in which direction the triangle is heading to
        fieldsize = UI.mainUI.FIELDSIZE
        nowpoint2 = (self.nowpoint[0]*(self.size[0]/fieldsize[0]), self.nowpoint[1]*(self.size[1]/fieldsize[1]))
        
        if self.velocity == (1, 0):
            xPos1 = nowpoint2[0] 
            yPos1 = nowpoint2[1] - 5*(self.size[1]/fieldsize[1])

            xPos2 = nowpoint2[0]
            yPos2 = nowpoint2[1] + 5*(self.size[1]/fieldsize[1])

            xPos3 = nowpoint2[0] + 5*(self.size[0]/fieldsize[0])
            yPos3 = nowpoint2[1]

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]

        if self.velocity == (0, 1):
            xPos1 = nowpoint2[0] - 5*(self.size[0]/fieldsize[0])
            yPos1 = nowpoint2[1] 

            xPos2 = nowpoint2[0]
            yPos2 = nowpoint2[1] + 5*(self.size[1]/fieldsize[1])

            xPos3 = nowpoint2[0] + 5*(self.size[0]/fieldsize[0])
            yPos3 = nowpoint2[1]

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]

        if self.velocity == (-1, 0):
            xPos1 = nowpoint2[0] - 5*(self.size[0]/fieldsize[0])
            yPos1 = nowpoint2[1] 

            xPos2 = nowpoint2[0]
            yPos2 = nowpoint2[1] + 5*(self.size[1]/fieldsize[1])

            xPos3 = nowpoint2[0] 
            yPos3 = nowpoint2[1] - 5*(self.size[0]/fieldsize[0])

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]


        if self.velocity == (0, -1):
            xPos1 = nowpoint2[0] - 5*(self.size[0]/fieldsize[0])
            yPos1 = nowpoint2[1] 

            xPos2 = nowpoint2[0]
            yPos2 = nowpoint2[1] - 5*(self.size[1]/fieldsize[1])

            xPos3 = nowpoint2[0] + 5*(self.size[0]/fieldsize[0])
            yPos3 = nowpoint2[1]

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]


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

        return switcher.get(colorId, (1, 1, 1))


    def increaseOpacity(self):
        ## function for creating an increasing opacity with increasing time
        if self.countdown_is_running3 == True:
            if self.opacityValue < 1:
                self.opacityValue += 0.1 / UI.mainUI.UPDATES_PER_SECOND
    
                return self.opacityValue


    
    def setVelocity(self, x):
        ## getting Velocity from TrackWidget
        self.velocity = x
        return x

    def setPosition(self, x):


        ## getting positition from TrackWidget
        if self.game_is_running3 == True:
            
            self.nowpoint = (x.x, x.y)
            print(self.nowpoint)
            return x

## set Booleans for initializing events
  
    def setBooleanGame(self):
        ## set Booleans for initializing events
        self.game_is_running3 = True

    def setBooleanCountdown(self):
        ## set Booleans for initializing events: increaseOpacity
        self.countdown_is_running3 = True
    
