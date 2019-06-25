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


class TrackWidget(Widget):
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
        players2 = TrackWidget.players
        

        with self.canvas:

            for player in players2:
                track = player.getLine()
                allPoints = self.constructMissingPoints(track)

                colorId = player.getColor()
                Color(rgb = self.getColorFromId(colorId))

                for point in allPoints:
                    xPos = point.x
                    yPos = point.y
                    xPos2 = (self.size[0]/fieldsize[0]) * xPos
                    yPos2 = (self.size[1]/fieldsize[1]) * yPos

                    Rectangle(pos=(xPos2, yPos2), size = ((self.size[0]/fieldsize[0]), (self.size[1]/fieldsize[1])) )

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

    def constructMissingPoints(self, track):
        ## function who creates all missing points in between
        allPoints = []

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

    def LineCreator(self):
        ## test function
        players3 = TrackWidget.players
        print('Hi')
        players3[0].addTrack(Vect2D(20,20), Vect2D(0, 20))

    
    velocity = [] # (x, y)
    speed_constant = 0.01
    speed_factor = 1

    def set_velocity(self, x , y):
        velocity = [x, y]
        print(velocity)
    def updateVelocity(self):
        pass

    

class MyKeyboardListener(Widget):
    ## keyboard listener, listen to keyboard inputs

    def __init__(self, game, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)

        self._game = game
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
            TrackWidget.LineCreator(self)
            

        if keycode[1] == 'w':
            # TrackWidget.set_velocity(0, 1)
            pass

        if keycode[1] == 'd':
            self._game.set_velocity(1, 0)

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
    
  