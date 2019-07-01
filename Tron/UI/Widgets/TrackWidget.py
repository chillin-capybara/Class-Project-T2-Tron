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



class TrackWidget(Widget):
    game_is_running = BooleanProperty(False)
    countdown_is_running = BooleanProperty(False)

    speed_constant = NumericProperty(0.001)
    speed_factor = NumericProperty(1)
    counter = NumericProperty(0)
    opacityValue = NumericProperty(0)
    countergetPos = BooleanProperty(True)
    counter_constructMissingPoints = NumericProperty(0)

    allPoints_from_pointCreator = []

    def __init__(self, **kwargs):
        ## creates update function for all uses, ensures synchronized update trigger
        super(TrackWidget, self).__init__(**kwargs)
        self._player = UI.mainUI.CLIENT.me
        ## adding the me player to the players list
        players.append(self._player)
        
    
    def update(self):
        ## main update function initiallizong funcions in the trackWidget
        self.canvas.clear()
        self.updatespeed_factor()
        self.update_players()


    def update_players(self):
        fieldsize = UI.mainUI.FIELDSIZE
        tracksize = UI.mainUI.TRACKSIZE
        with self.canvas:
            self.opacity = self.opacityValue
            if self.game_is_running == False and self.countdown_is_running == True:
                ## I want to slowly increse the opacity of the Head while countdown is running
                for player in players:
                    ## Generates for every player a headWidget a class and handles down some values
                    HeadWidget(
                    game_is_running = self.game_is_running,
                    countdown_is_running = self.countdown_is_running,
                    opacityValue = self.opacityValue,
                    screen_size = self.size, 
                    player = player)
                    

            if self.game_is_running == True:
                for player in players:   
                    if player == self._player:
                        allPoints_after_calculation = self.pointCreator()
                    else:
                        print(player.getTrack())
                        allPoints_from_submission = player.getTrack()
                        allPoints_after_calculation = self.constructMissingPoints(allPoints_from_submission, player)
                
                    Color(rgba = self.getPlayerColor(player))

                    HeadWidget(screen_size = self.size, player = player)

                    for point in allPoints_after_calculation:
                        xPos2 = (self.size[0]/fieldsize[0]) * point.x
                        yPos2 = (self.size[1]/fieldsize[1]) * point.y

                        xSize = tracksize * (self.size[0]/fieldsize[0])
                        ySize = tracksize * (self.size[1]/fieldsize[1])

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

    def constructMissingPoints(self, track, player):
        ## function who creates all missing points in between
        if player == self._player and  self.counter_constructMissingPoints == 0:
            track = [player.getPosition(), player.getPosition()]
        if player == self._player:
            print ("hi")
        # allPoints = [player.getPosition()]
        allPoints = []
        pointCount = len(track)
        for i in range(0, pointCount - 1):
            startPoint = track[i]
            endPoint = track[i + 1]

            # startPoint = (10, 10)
            # endPoint = (14, 10)

            # (14 - 10) + (10 - 10) = 4
            lineLength = abs((endPoint.x - startPoint.x) + (endPoint.y - startPoint.y))
            if player == self._player and  self.counter_constructMissingPoints == 0:
                lineLength = 1
                self.counter_constructMissingPoints += 1

            deltaX = (endPoint.x - startPoint.x) / lineLength
            deltaY = (endPoint.y - startPoint.y) / lineLength

            for j in range(0, lineLength):
                xVal = round(startPoint.x + deltaX * j)
                yVal = round(startPoint.y + deltaY * j)
                allPoints.append(Vect2D(xVal, yVal))

        allPoints.append(track[-1])

        return allPoints


    
    def pointCreator(self):
        ## function for creating points in combination with the speed factor
        ## PS: Speed factor is increasing with time
        
        velocity = self._player.getVelocity()
        move = (
            velocity.x * self.speed_factor, 
            velocity.y * self.speed_factor
        )

        startPos = self._player.getPosition()
        if self.counter == 0:
            ## the function with xVal and yVal needs an initial value to start with, because of this 
            ## I need to add an if loop who appends one value at the beginning
            ## this counter is later on used for finding the last value
            self.allPoints_from_pointCreator.append(startPos)
        
        xVal = round(move[0] + self.allPoints_from_pointCreator[self.counter].x)
        yVal = round(move[1] + self.allPoints_from_pointCreator[self.counter].y)
        
        self.detect_outbound(xVal, yVal)
        self.allPoints_from_pointCreator.append(Vect2D(xVal, yVal))
        self.counter += 1

        self._player.setPosition(xVal, yVal)

        return self.allPoints_from_pointCreator


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