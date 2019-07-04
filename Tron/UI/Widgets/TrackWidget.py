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

from Backend.Classes.Client import Client
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
    counter = NumericProperty(0)
    opacityValue = NumericProperty(0)
    countergetPos = BooleanProperty(True)
    counter_constructMissingPoints = NumericProperty(0)
    counter_update_players = NumericProperty(0)
    counter_update_players_remote = NumericProperty(0)
    playerList = ListProperty([])


    allPoints_from_submission = ListProperty([])
    allPoints = ListProperty([])
    allPoints_from_pointCreator = []

    def __init__(self, **kwargs):
        ## creates update function for all uses, ensures synchronized update trigger
        super(TrackWidget, self).__init__(**kwargs)
        self._player = UI.mainUI.CLIENT.me
    
    def update(self):
        self.canvas.clear()
        self.updatespeed_factor()
        self.update_players()
        


    def update_players(self):
        fieldsize = UI.mainUI.FIELDSIZE
        with self.canvas:
            self.opacity = self.opacityValue
            if self.game_is_running == False and self.countdown_is_running == True:
                ## I want to slowly increse the opacity of the Head while countdown is running
                for player in self.playerList:
                    
                    ## Generates for every player a headWidget a class and handles down some values
                    HeadWidget(
                    game_is_running = self.game_is_running,
                    countdown_is_running = self.countdown_is_running,
                    opacityValue = self.opacityValue,
                    screen_size = self.size, 
                    player = player)
                    

            if self.game_is_running == True:
                
                for player in self.playerList:   
                    self.allPoints_from_submission = player.getTrack()
                #     if player == self._player:
                #         if self.counter_update_players == 0:
                #             self.counter_update_players += 1
                #             # firstPoint = self.pointCreator_special_case()
                #             firstPoint = player.getPosition().clone()
                #             self.pointCreator(player)
                #             player.addTrack(firstPoint, player.getPosition().clone())

                #         self.pointCreator(player)
                        
                #         # if len(player.getTrack()) > 0:
                #         #     allPoints_from_submission = player.getTrack()
                            
                #         allPoints_after_calculation = self.constructMissingPoints(player)

                #     else:
                #         # if self.counter_update_players_remote < len(UI.mainUI.GAME.getPlayers()):
                #         if self.counter_update_players_remote < 3:
                #             self.counter_update_players_remote += 1
                #             # firstPoint = self.pointCreator_special_case()
                #             player.addTrack(player.getPosition().clone(), player.getPosition().clone())

                #         allPoints_after_calculation = self.constructMissingPoints_for_remote(player)
                #         print(player.getPosition())
                    
                    Color(rgba = self.getPlayerColor(player))
                    HeadWidget(screen_size = self.size, player = player)

                    for point in self.allPoints_from_submission:
                        xPos2 = (self.size[0]/fieldsize[0]) * point.x
                        yPos2 = (self.size[1]/fieldsize[1]) * point.y

                        xSize = self.size[0]/fieldsize[0]
                        ySize = self.size[1]/fieldsize[1]

                        Rectangle(pos=(xPos2, yPos2), size=(xSize, ySize))



    def constructMissingPoints_for_remote(self, player):
        ## function who creates all missing points in between
        allPoints_from_submission = player.getTrack()
        allPoints_from_submission.append(player.getPosition())
        allPoints = []
        
        pointCount = len(allPoints_from_submission)
        for i in range(0, pointCount - 1):
            startPoint = allPoints_from_submission[i]
            endPoint = allPoints_from_submission[i + 1]

            # startPoint = (10, 10)
            # endPoint = (14, 10)

            # (14 - 10) + (10 - 10) = 4
            lineLength = abs((endPoint.x - startPoint.x) + (endPoint.y - startPoint.y))
            if lineLength == 0:
                lineLength = 1
            if player == self._player and  self.counter_constructMissingPoints == 0:
                lineLength = 1
                self.counter_constructMissingPoints += 1

            deltaX = (endPoint.x - startPoint.x) / lineLength
            deltaY = (endPoint.y - startPoint.y) / lineLength

            for j in range(0, lineLength):
                xVal = round(startPoint.x + deltaX * j)
                yVal = round(startPoint.y + deltaY * j)
                allPoints.append(Vect2D(xVal, yVal))

        allPoints.append(allPoints_from_submission[-1])

        return allPoints





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

    
    def pointCreator(self, player):
        ## function for creating points in combination with the speed factor
        ## PS: Speed factor is increasing with time
        
        velocity = player.getVelocity()
        move = (
            velocity.x * self.speed_factor, 
            velocity.y * self.speed_factor
        )
        xVal = round(move[0] + player.getPosition().x)
        yVal = round(move[1] + player.getPosition().y)
        
        self.detect_outbound(xVal, yVal)
        self.counter += 1

        player.setPosition(xVal, yVal)





    def constructMissingPoints(self, player):
        ## function who creates all missing points in between
        self.allPoints.clear()
        if player != self._player:
            trackList = [player.getPosition()]
        else:
            trackList = player.getTrack()
        trackList.append(player.getPosition())
        
        pointCount = len(trackList)
        for i in range(0, pointCount - 1):
            startPoint = trackList[i]
            endPoint = trackList[i + 1]
            # startPoint = (10, 10)
            # endPoint = (14, 10)

            # (14 - 10) + (10 - 10) = 4
            lineLength = abs((endPoint.x - startPoint.x) + (endPoint.y - startPoint.y))
            
            if lineLength == 0:
                lineLength = 1
            deltaX = (endPoint.x - startPoint.x) / lineLength
            deltaY = (endPoint.y - startPoint.y) / lineLength

            for j in range(0, lineLength):
                xVal = round(startPoint.x + deltaX * j)
                yVal = round(startPoint.y + deltaY * j)
                self.allPoints.append(Vect2D(xVal, yVal))

        self.allPoints.append(trackList[-1])
        return self.allPoints





    
    def updatespeed_factor(self):
        self.speed_factor = self.speed_factor + self.speed_constant


    def setBooleanGame(self):
        self.game_is_running = True

    def setBooleanCountdown(self):
        self.countdown_is_running = True

    def detect_outbound(self, xVar, yVar):
        fieldsize = UI.mainUI.FIELDSIZE

        if xVar < 0 or xVar > fieldsize[0] or yVar < 0 or yVar > fieldsize[1]:
            print ("You hit one border")
            
