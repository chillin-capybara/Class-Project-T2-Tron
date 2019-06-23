from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.animation import Animation
from kivy.graphics import Triangle, Rectangle, Ellipse, Line

from kivy.clock import Clock
import random

from ...Backend.Core.Vect2D import Vect2D



class TrackWidget(Widget):
    updatesPerSecond = 10
    fieldSize = (100, 100)

    def startTrack(self):
        self.canvas.clear()

        with self.canvas.before:
            Line(width=1, rectangle=(self.x + 1, self.y + 1, self.width - 2, self.height - 2))

        Clock.schedule_interval(self.update, 0.5 / self.updatesPerSecond)


    def update(self, *args):
        linepoints = []
        
        # for i in range(random.randint(1, 50)):
        #     linepoints.append(Vect2D(random.randint(1, 99), random.randint(1, 99)))
        
        for i in range(50):
            linepoints.append(Vect2D(1+i, 10+i))
        for t in range(1):
            print (len(linepoints))
            if linepoints[2*t] != linepoints[2*t+2] and linepoints[2*t+1] != linepoints[2*t+3]:
                break
        


        self.canvas.clear()
        with self.canvas:
            for point in linepoints:
                x = (point.x - 1) * 5
                y = (point.y - 1) * 5
                Rectangle(pos=(x, y), size=(5, 5))


    # Events
    def on_finished(self):
        pass