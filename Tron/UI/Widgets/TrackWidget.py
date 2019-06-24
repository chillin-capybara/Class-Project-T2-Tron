from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.animation import Animation
from kivy.graphics import Triangle, Rectangle, Ellipse, Line

from kivy.clock import Clock
import random

from Backend.Core.Vect2D import Vect2D



class TrackWidget(Widget):
    # function for creating the single rectangles, creating the typical snake feeling
    updatesPerSecond = 10
    fieldSize = (100, 100)

    def startTrack(self):
        # function responsible for the drawing part
        self.canvas.clear()

        with self.canvas.before:
            Line(width=1, rectangle=(self.x + 1, self.y + 1, self.width - 2, self.height - 2))

        # runs the update function every periode
        Clock.schedule_interval(self.update, 0.5 / self.updatesPerSecond)


    def update(self, *args):
        # function for updating the linepoints and draw new
        linepoints = []
        
        # for i in range(random.randint(1, 50)):
        #     linepoints.append(Vect2D(random.randint(1, 99), random.randint(1, 99)))
        for i in range(50):
            linepoints.append(Vect2D(1+i, 10+i))
            self.straightlinechecker(linepoints)


        self.canvas.clear()
        with self.canvas:
            for point in linepoints:
                x = (point.x - 1) * 5
                y = (point.y - 1) * 5
                Rectangle(pos=(x, y), size=(5, 5))

    def straightlinechecker(self, *args):
        # function for checking if two points in list are straight line 
        # linepoints = [] # Fr.S. wenn auskommentiert kommt nichts mehr bei raus (nimmt Liste nicht von draußem)
        
        for t in range(len(self.linepoints)-3):
            print (len(self.linepoints))
            if self.linepoints[2*t] == self.linepoints[2*t+2]:
                self.constructvertilane()
            elif self.linepoints[2*t+1] == self.linepoints[2*t+3]:
                self.constructhorilane()
            else:
                break

    def constructvertilane(self, *args):
        # function for getting all points between two side points
        # Fr.S. wie bekomme ich den straightpoints wieder raus
        linepoints = [0, 10, 0, 100]
        straightpoints = []
        for i in range(linepoints[1], linepoints[3]):
            straightpoints.append(linepoints[0])
            straightpoints.append(linepoints[1]+i)
            
   
   
    def constructhorilane(self, *args):
        # function for getting all points between two side points
        linepoints = [0, 30, 100, 30]
        straightpoints = []
        for i in range(linepoints[0], linepoints[2]):
            straightpoints.append(linepoints[0]+i)
            straightpoints.append(linepoints[1])
            

    # Events
    def on_finished(self):
        pass