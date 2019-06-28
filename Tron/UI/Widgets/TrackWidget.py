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



p1 = HumanPlayer()
p1.setName("Simon")
p1.setColor((1, 1, 0))
p1.setPosition(20, 20)
p1.addTrack(Vect2D(10, 10), Vect2D(20, 10))
# p1.addTrack(Vect2D(20, 10), Vect2D(20, 20))

p2 = HumanPlayer()
p2.setName("Lorenz")
p2.setColor((0, 1, 1))
p2.setPosition(50, 50)
p2.addTrack(Vect2D(30, 40), Vect2D(45, 40))
p2.addTrack(Vect2D(45, 40), Vect2D(45, 45))
p2.addTrack(Vect2D(45, 45), Vect2D(100, 45))
p2.setVelocity(1, 0)

p3 = HumanPlayer()
p3.setName("Marcell")
p3.setColor((1, 0, 1))
p3.setPosition(50, 50)
p3.addTrack(Vect2D(70, 40), Vect2D(80, 40))
p3.addTrack(Vect2D(80, 40), Vect2D(10, 40))
p3.addTrack(Vect2D(10, 60), Vect2D(30, 60))
p3.setVelocity(0, 1)

players = [p1, p2, p3]
# remoteplayers = [Game.getPlayers()]


class TrackWidget(Widget):
    game_is_running = BooleanProperty(False)
    countdown_is_running = BooleanProperty(False)

    speed_constant = NumericProperty(0.001)
    speed_factor = NumericProperty(1)
    counter = NumericProperty(0)
    opacityValue = NumericProperty(0)
    countergetPos = BooleanProperty(True)

    
    def update(self):
        self.canvas.clear()
        self.updatespeed_factor()
        self.update_players()


    def update_players(self):
        fieldsize = UI.mainUI.FIELDSIZE
        with self.canvas:
            self.opacity = self.opacityValue

            if self.game_is_running == True:
                for player in players:    
                    allPoints_from_submission = player.getLine()
                    allPoints_after_calculation = self.constructMissingPoints(allPoints_from_submission)

                    colorId = player.getColor()
                    addOpacity = list(colorId)
                    addOpacity.append(self.opacityValue)
                    colorID2 = tuple(addOpacity)
                    Color(rgb = colorID2)

                    HeadWidget(player = player)

                    for point in allPoints_after_calculation:
                        xPos2 = (self.size[0]/fieldsize[0]) * point.x
                        yPos2 = (self.size[1]/fieldsize[1]) * point.y

                        xSize = self.size[0]/fieldsize[0]
                        ySize = self.size[1]/fieldsize[1]

                        Rectangle(pos=(xPos2, yPos2), size=(xSize, ySize))


    def increaseOpacity(self):
        ## function for creating an increasing opacity with increasing time
        if self.countdown_is_running == True:
            if self.opacityValue < 1:
                self.opacityValue += 0.1 / UI.mainUI.UPDATES_PER_SECOND
                
                return self.opacityValue


    def constructMissingPoints(self, track):
        ## function who creates all missing points in between
        allPoints = [p1.getPosition()]
        pointCount = len(track)
        for i in range(0, pointCount - 1):
            startPoint = track[i]
            endPoint = track[i + 1]

            # startPoint = (10, 10)
            # endPoint = (14, 10)

            # (14 - 10) + (10 - 10) = 4
            lineLength = abs((endPoint.x - startPoint.x) + (endPoint.y - startPoint.y))

            deltaX = (endPoint.x - startPoint.x) / lineLength
            deltaY = (endPoint.y - startPoint.y) / lineLength

            for j in range(0, lineLength):
                xVal = round(startPoint.x + deltaX * j)
                yVal = round(startPoint.y + deltaY * j)
                allPoints.append(Vect2D(xVal, yVal))

        allPoints.append(track[-1])

        return allPoints


    
    def pointCreator(self, player):
        ## function for creating points in combination with the speed factor
        ## PS: Speed factor is increasing with time
        
        velocity = player.getVelocity()
        move = (
            velocity[0] * self.speed_factor, 
            velocity[1] * self.speed_factor
        )

        startPos = player.getPosition()
        if self.counter == 0:
            ## the function with xVal and yVal needs an initial value to start with, because of this 
            ## I need to add an if loop who appends one value at the beginning
            ## this counter is later on used for finding the last value
            self.allPoints.append(startPos)
        
        xVal = round(move[0] + self.allPoints[self.counter].x)
        yVal = round(move[1] + self.allPoints[self.counter].y)
        
        self.detect_outbound(xVal, yVal)
        self.allPoints.append(Vect2D(xVal, yVal))
        self.counter += 1

        return self.allPoints


    def updatespeed_factor(self):
        self.speed_factor = self.speed_factor + self.speed_constant


    def getVelocity(self):
        ## get-function for transfering veloctiy to HeadWidget
        return self.velocity

    # def getPos(self):
    #     ## get-function for transfering resent Position to HeadWidget
    #     if self.countdown_is_running == True:
    #         ## should only be started after game ist started
    #         if self.countergetPos == True:
    #             ## Problems with None-Values if the if loop is missing, loops one time through the pointCreator()
    #             self.pointCreator()
    #             self.countergetPos = False

    #         return self.allPoints[len(self.allPoints)-1]

    def detect_outbound(self, xVar, yVar):
        fieldsize = UI.mainUI.FIELDSIZE

        if xVar < 0 or xVar > fieldsize[0]:
            print ("You hit the right or left border")
        elif yVar < 0 or yVar > fieldsize[1]:
            print ("You hit the upper or lower border")