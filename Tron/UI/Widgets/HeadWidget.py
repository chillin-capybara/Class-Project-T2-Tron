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

from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget


class HeadWidget(Widget):
    player = ObjectProperty(None)
    screen_size = ObjectProperty(None)
    game_is_running = BooleanProperty(False)
    countdown_is_running = BooleanProperty(False)
    opacityValue = NumericProperty(1)
    

    def on_player(self, instance, value):
        #print (self.parent.parent.size)
        if value == None:
            return

        self.canvas = Canvas()
        with self.canvas:
            Color(rgba = self.getPlayerColor())
            Triangle(points = self.calculatePoints())

    def getPlayerColor(self):
        colorId = self.player.getColor()
        addOpacity = list(colorId)
        addOpacity.append(self.opacityValue)
        return tuple(addOpacity)

    def calculatePoints(self):
        ## creating all points requiered for a triangle + detecting in which direction the triangle is heading to
        fieldsize = UI.mainUI.FIELDSIZE
        velocity = self.player.getVelocity()
        playPos = self.player.getPosition()
        nowpoint = (
            playPos.x * (self.screen_size[0]/fieldsize[0]), 
            playPos.y * (self.screen_size[1]/fieldsize[1])
        )
        
        if velocity == Vect2D(1, 0):
            xPos1 = nowpoint[0] 
            yPos1 = nowpoint[1] - 5*(self.screen_size[1]/fieldsize[1])

            xPos2 = nowpoint[0]
            yPos2 = nowpoint[1] + 5*(self.screen_size[1]/fieldsize[1])

            xPos3 = nowpoint[0] + 5*(self.screen_size[0]/fieldsize[0])
            yPos3 = nowpoint[1]

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]

        if velocity == Vect2D(0, 1):
            xPos1 = nowpoint[0] - 5*(self.screen_size[0]/fieldsize[0])
            yPos1 = nowpoint[1] 

            xPos2 = nowpoint[0]
            yPos2 = nowpoint[1] + 5*(self.screen_size[1]/fieldsize[1])

            xPos3 = nowpoint[0] + 5*(self.screen_size[0]/fieldsize[0])
            yPos3 = nowpoint[1]

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]

        if velocity == Vect2D(-1, 0):
            xPos1 = nowpoint[0] - 5*(self.screen_size[0]/fieldsize[0])
            yPos1 = nowpoint[1] 

            xPos2 = nowpoint[0]
            yPos2 = nowpoint[1] + 5*(self.screen_size[1]/fieldsize[1])

            xPos3 = nowpoint[0] 
            yPos3 = nowpoint[1] - 5*(self.screen_size[0]/fieldsize[0])

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]


        if velocity == Vect2D(0, -1):
            xPos1 = nowpoint[0] - 5*(self.screen_size[0]/fieldsize[0])
            yPos1 = nowpoint[1] 

            xPos2 = nowpoint[0]
            yPos2 = nowpoint[1] - 5*(self.screen_size[1]/fieldsize[1])

            xPos3 = nowpoint[0] + 5*(self.screen_size[0]/fieldsize[0])
            yPos3 = nowpoint[1]

            return [xPos1, yPos1, xPos2, yPos2, xPos3, yPos3]

    def update_screen_size(self, screensize_from_top):
        ## todo getting value to be constant
        print (screensize_from_top)
        return screensize_from_top
         