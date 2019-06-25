from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.animation import Animation
from kivy.graphics import *

from kivy.clock import Clock
import random
import math

from Backend.Classes.HumanPlayer import HumanPlayer
from Backend.Core.Vect2D import Vect2D
from Backend.Classes.Game import Game
from Backend.Classes.Player import Player

fieldSize = (100, 100)

class TrackWidget(Widget):
    def update(self):
        self.canvas.clear()

        p1 = HumanPlayer()
        p1.setName("Simon")
        p1.setColor(0)
        p1.setPosition(20, 20)
        p1.addTrack(Vect2D(10, 10), Vect2D(20, 10))
        p1.addTrack(Vect2D(20, 10), Vect2D(20, 20))

        p2 = HumanPlayer()
        p2.setName("Ludi")
        p2.setColor(3)
        p2.setPosition(50, 50)
        p2.addTrack(Vect2D(40, 40), Vect2D(45, 40))
        p2.addTrack(Vect2D(45, 40), Vect2D(45, 45))

        players = [ p1, p2 ]

        with self.canvas:

            for player in players:
                track = player.getLine()
                allPoints = self.constructMissingPoints(track)

                colorId = player.getColor()
                Color(rgba = self.getColorFromId(colorId))

                for point in allPoints:
                    xPos = point.x * 5 - 2.5
                    yPos = point.y * 5 - 2.5
                    Rectangle(pos=(xPos, yPos), size=(5, 5))


    def getColorFromId(self, colorId):
        switcher = {
            0: (1, 0, 0, 1),
            1: (0, 1, 0, 1),
            2: (0, 0, 1, 1),
            3: (0, 1, 1, 1),
            4: (1, 1, 0, 1),
            5: (1, 0, 1, 1),
        }

        return switcher.get(colorId, (1, 1, 1, 1))

    def constructMissingPoints(self, tack):
        allPoints = []
        pointCount = len(tack)

        for i in range(0, pointCount - 1):
            startPoint = tack[i]
            endPoint = tack[i + 1]

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
        
        allPoints.append(tack[-1])
        return allPoints