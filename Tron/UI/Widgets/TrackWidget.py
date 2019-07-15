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
from UI.Widgets.HeadWidget import HeadWidget
import UI.mainUI


from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget



class TrackWidget(Widget):
    game_is_running = BooleanProperty(False)
    countdown_is_running = BooleanProperty(False)
    speed_constant = NumericProperty(0.001)
    speed_factor = NumericProperty(1)
    opacityValue = NumericProperty(0)
    fieldsize = ListProperty([])
    client = ObjectProperty(object())

    def update(self):
        self.canvas.clear()
        self.updatespeed_factor()
        self.update_players()
    
    def __init__(self, *args, **kwargs):
        self.game_is_running = False
        self.countdown_is_running = False
        self.speed_factor = 1
        self.opacityValue = 0
        self.fieldsize = []
        self.client = ObjectProperty(object())
        super().__init__(*args, **kwargs)
    
    def reset_init(self):
        self.game_is_running = False
        self.countdown_is_running = False
        self.speed_factor = 1
        self.opacityValue = 0
        self.fieldsize = []


    def update_players(self):
        with self.canvas:
            self.opacity = self.opacityValue
            # if self.game_is_running == False and self.countdown_is_running == True:
            #     ## I want to slowly increse the opacity of the Head while countdown is running
            #     for player in self.client.match.players:
                    
            #         ## Generates for every player a headWidget a class and handles down some values
            #         HeadWidget(
            #         game_is_running = self.game_is_running,
            #         countdown_is_running = self.countdown_is_running,
            #         fieldsize = self.fieldsize,
            #         opacityValue = self.opacityValue,
            #         screen_size = self.size, 
            #         player = player)
                    

            if self.game_is_running == True:
                for player in self.client.match.players:   
                    allPoints_from_submission = player.getTrack()
                    
                    Color(rgba = self.getPlayerColor(player))
                    HeadWidget(
                    screen_size = self.size, 
                    fieldsize = self.fieldsize,
                    player = player)

                    for point in allPoints_from_submission:
                        xPos2 = (self.size[0]/self.fieldsize[0]) * point.x
                        yPos2 = (self.size[1]/self.fieldsize[1]) * point.y

                        xSize = self.size[0]/self.fieldsize[0]
                        ySize = self.size[1]/self.fieldsize[1]

                        Rectangle(pos=(xPos2, yPos2), size=(xSize, ySize))

    def increaseOpacity(self):
        ## function for creating an increasing opacity with increasing time
        if self.countdown_is_running == True:
            if self.opacityValue < 1:
                self.opacityValue += 0.5 / UI.mainUI.UPDATES_PER_SECOND
                
                return self.opacityValue

    def getPlayerColor(self, player):
        ## function for adding the opacity Value to the rgb -> rgba
        colorId = player.getColor()
        addOpacity = list(colorId)
        addOpacity.append(self.opacityValue)
        return tuple(addOpacity)

    def getFieldsize(self, fieldsizeX, fieldsizeY):
        self.fieldsize = (fieldsizeX, fieldsizeY)
    
    def updatespeed_factor(self):
        self.speed_factor = self.speed_factor + self.speed_constant


    def setBooleanGame(self):
        self.game_is_running = True

    def setBooleanCountdown(self):
        self.countdown_is_running = True

    def setBooleanGame_Ended(self):
        self.game_is_running = False

    def detect_outbound(self, xVar, yVar):

        if xVar < 0 or xVar > self.fieldsize[0] or yVar < 0 or yVar > self.fieldsize[1]:
            print ("You hit one border")
            
    def game_ended(self):
        self.game_is_running = False
        self.opacityValue = 0
        self.clear_widgets()
        #self.client = ObjectProperty()
        self.exit()
        