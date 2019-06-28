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





p3 = HumanPlayer()
p3.setName("Marcell")
p3.setColor((1, 0, 1))
p3.setPosition(50, 50)
p3.addTrack(Vect2D(70, 40), Vect2D(80, 40))
p3.addTrack(Vect2D(80, 40), Vect2D(10, 40))
p3.addTrack(Vect2D(10, 60), Vect2D(30, 60))

players = [p1]
remoteplayers = [p1, p2, p3]
# remoteplayers = [Game.getPlayers()]

class TrackWidget(Widget):
    opacityValue = NumericProperty(0)
    speed_constant = NumericProperty(0.001)
    speed_factor = NumericProperty(1)
    game_is_running2 = BooleanProperty(False)
    countdown_is_running2 = BooleanProperty(False)
    # remoteplayers = ListProperty([Game.getPlayers()])

    remoteplayers.remove(p1)


    allPoints = []
    

    counter = NumericProperty(0)
    countergetPos = BooleanProperty(True)
    

    def __init__(self, **kwargs):
        ## Fr. S. was das genau bewirkt
        super(TrackWidget, self).__init__(**kwargs)

        self.velocity = (0, 1)



    # def update_remote_player(self):
    #     fieldsize = UI.mainUI.FIELDSIZE
    #     self.canvas.clear()
    #     with self.canvas:
    #         self.opacity = self.opacityValue

    #         if self.game_is_running2 == True:
    #             for player in remoteplayers:    
    #                 # allPoints_from_submission = player.getTrack()
    #                 colorId = player.getColor()
    #                 Color(rgba = self.getColorFromId(colorId))
                    
                    
    #                 for point in allPoints_from_submission:
                    

    #                     xPos2 = (self.size[0]/fieldsize[0]) * point.x
    #                     yPos2 = (self.size[1]/fieldsize[1]) * point.y

    #                     xSize = self.size[0]/fieldsize[0]
    #                     ySize = self.size[1]/fieldsize[1]

    #                     Rectangle(pos=(xPos2, yPos2), size=(xSize, ySize))

    def update_human_player(self):
        ## function for updating the track
        fieldsize = UI.mainUI.FIELDSIZE
        self.canvas.clear()
        self.updatespeed_factor()
        
        

        with self.canvas:
            self.opacity = self.opacityValue

            # for player in players:
            # track = player.getLine()
            if self.game_is_running2 == True:
                allPoints = self.pointCreator()
                allPoints2 = self.constructMissingPoints(allPoints)
                ## I want all points to be submitted, also the intermediate points
                self.addTrack_to_sub(allPoints2)
                colorId = p1.getColor()
                Color(rgba = self.getColorFromId(colorId))
                
                
                for point in allPoints2:
                

                    xPos2 = (self.size[0]/fieldsize[0]) * point.x
                    yPos2 = (self.size[1]/fieldsize[1]) * point.y

                    xSize = self.size[0]/fieldsize[0]
                    ySize = self.size[1]/fieldsize[1]

                    Rectangle(pos=(xPos2, yPos2), size=(xSize, ySize))





    def getColorFromId(self, colorId):
        ## remove
        switcher = {
            0: (1, 0, 0, self.opacityValue),
            1: (0, 1, 0, self.opacityValue),
            2: (0, 0, 1, self.opacityValue),
            3: (0, 1, 1, self.opacityValue),
            4: (1, 1, 0, self.opacityValue),
            5: (1, 0, 1, self.opacityValue),
        }

        return switcher.get(colorId, (1, 1, 1, 1))


    def increaseOpacity(self):
        ## function for creating an increasing opacity with increasing time
        if self.countdown_is_running2 == True:
            if self.opacityValue < 1:
                self.opacityValue += 0.1 / UI.mainUI.UPDATES_PER_SECOND
                
                return self.opacityValue



    def constructMissingPoints(self, track):
        ## function who creates all missing points in between
        allPoints3 = [p1.getPosition()]
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
                allPoints3.append(Vect2D(xVal, yVal))

        allPoints3.append(track[-1])

        return allPoints3


    
    
    
    def pointCreator(self):
        ## function for creating points in combination with the speed factor
        ## PS: Speed factor is increasing with time
        
        move = (self.velocity[0] * self.speed_factor, self.velocity[1]*self.speed_factor)

        for player in players:
            startPos = player.getPosition()
            if self.counter == 0:
                ## the function with xVal and yVal needs an initial value to start with, because of this 
                ## I need to add an if loop who appends one value at the beginning
                ## this counter is later on used for finding the last value
                self.allPoints.append(startPos)
            
            xVal = round(move[0] + self.allPoints[self.counter].x)
            yVal = round(move[1] + self.allPoints[self.counter].y)
            
            self.allPoints.append(Vect2D(xVal, yVal))
        self.counter += 1
              
        


        return self.allPoints

    def setBooleanGame(self):
        ## set Booleans for initializing events
        self.game_is_running2 = True

    def setBooleanCountdown(self):
        ## set Booleans for initializing events: increaseOpacity
        self.countdown_is_running2 = True
        self.increaseOpacity()

        

    def press_d_key(self):
        ## is triggered by keyboard listener, if I have a velocity vector in a certain direction, I need to change that velocity
        ## with d we go clockwise
        if self.velocity == (1, 0):
            self.velocity = (0, -1)
            
            return

        if self.velocity == (0, 1):
            self.velocity = (1, 0)
            return

        if self.velocity == (-1, 0):
            self.velocity = (0, 1)
            return


        if self.velocity == (0, -1):
            self.velocity = (-1, 0)
            return
    

    def press_a_key(self):
        ## is triggered by keyboard listener, if I have a velocity vector in a certain direction, I need to change that velocity
        ## with a we go counter-clockwise
        if self.velocity == (1, 0):
            self.velocity = (0, 1)
            return

        if self.velocity == (0, 1):
            self.velocity = (-1, 0)
            return
            
        if self.velocity == (-1, 0):
            self.velocity = (0, -1)
            return

        if self.velocity == (0, -1):
            self.velocity = (1, 0)
            return

        



    def updatespeed_factor(self):
        ## function for increasing speed_factor over time, is updated by standard update function of TrackWidget class
        self.speed_factor = self.speed_factor + self.speed_constant


    def getVelocity(self):
        ## get-function for transfering veloctiy to HeadWidget
        return self.velocity

    def getPos(self):
        ## get-function for transfering resent Position to HeadWidget
        if self.game_is_running2 == True:
            ## should only be started after game ist started
            if self.countergetPos == True:
                ## Problems with None-Values if the if loop is missing, loops one time through the pointCreator()
                self.pointCreator()
                self.countergetPos = False

            return self.allPoints[len(self.allPoints)-1]

    def addTrack_to_sub(self, points):
        if self.game_is_running2 == True:
            p1.addTrack((points[len(points)-2]),(points[len(points)-1]))
            # print(p1.getTrack())

        
    
    






class MyKeyboardListener(Widget):
    ## keyboard listener, listen to keyboard inputs

    def __init__(self, game, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)

        self._game = game
        self._track = game.ids.trackWidget
        self._keyboard = Window.request_keyboard( self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)
        
        # enterPause Menu
        if keycode[1] == 'p':
            print("not Implemented Yet Pause Menu")
            keyboard.release()

        if keycode[1] == 'a':
            self._track.press_a_key()

        if keycode[1] == 'd':
            self._track.press_d_key()
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
    
