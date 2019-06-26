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
import UI.mainUI

from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget


## Fr.S
# updatesPerSeconds = parent.updatesPerSeconds
# updatesPerSeconds = 50

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

class TrackWidget(Widget):
    opacityValue = NumericProperty(0)
    speed_constant = NumericProperty(0.01)
    speed_factor = NumericProperty(1)

    def __init__(self, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)

        self.velocity = (0, 1)

    def update(self):
        ## function for updating the track
        fieldsize = (100, 100)
        self.canvas.clear()
        self.increaseOpacity()
        self.updatespeed_factor()

        with self.canvas:
            self.opacity = self.opacityValue

            for player in players:
                track = player.getLine()
                allPoints2 = self.constructMissingPoints(track)

                colorId = player.getColor()
                Color(rgba = self.getColorFromId(colorId))

                for point in allPoints2:
                    xPos = point.x
                    yPos = point.y

                    xPos2 = (self.size[0]/fieldsize[0]) * xPos
                    yPos2 = (self.size[1]/fieldsize[1]) * yPos

                    xSize = self.size[0]/fieldsize[0]
                    ySize = self.size[1]/fieldsize[1]

                    Rectangle(pos=(xPos2, yPos2), size=(xSize, ySize))

        # with self.canvas:
        #     for player in players2:
        #         startpos = player.getPosition()
        #         xPos = startpos[0]
        #         yPos = startpos[1]
        #         Triangle(size_hint=(0.5, 0.5))



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
        ## Fr. S.
        if self.parent.parent.countdown_is_running or self.parent.parent.game_is_running:
            if self.opacityValue < 1:
                self.opacityValue += 0.01 / UI.mainUI.UPDATES_PER_SECOND
                print (self.opacityValue)
                return self.opacityValue

    def constructMissingPoints(self, track):
        ## function who creates all missing points in between
        allPoints2 = []

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
                allPoints2.append(Vect2D(xVal, yVal))

        allPoints2.append(track[-1])

        return allPoints2

    def LineCreator2(self):
        ## test function
        players3 = TrackWidget.players
        print('Hi')
        players3[0].addTrack(Vect2D(20,20), Vect2D(0, 20))

    
     # (x, y)
    
    def press_d_key(self):
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

        


    # def press_d_key(self, x = velocity[0], y = velocity[1]):
    #     print ("d")
    #     if self.velocity[0] == 1 and self.veloctiy[1] == 0:
    #         pass
    #         # self.velocity = (0, -1)
    #     if self.velocity[0] == 0 and self.veloctiy[1] == 1:
    #         pass
    #         # self.velocity = (1, 0)
    #     if self.velocity[0] == -1 and self.veloctiy[1] == 0:
    #         pass
    #         # self.velocity = (0, 1)
    #     if self.velocity[0] == 0 and self.veloctiy[1] == -1:
    #         pass
    #         # self.velocity = (-1, 0)
    #     # return self.velocity


    def updatespeed_factor(self):
        self.speed_factor = self.speed_factor + self.speed_constant
    
    # def createStartPoint(self):
    #     allPoints = []
    #     velocity = [1, 0]
    #     pointx = velocity[0] + p1.getPosition()[0]
    #     pointy = velocity[1] + p1.getPosition()[0]
    #     allPoints.append(Vect2D(pointx, pointy))
    #     print (allPoints)
    #     pass




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
    
