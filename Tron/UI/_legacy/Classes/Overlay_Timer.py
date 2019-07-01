from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
# from Tron.Backend.Classes.Player import Player
# from Tron.Backend.Classes.Factory import Factory


# player1 = Factory.Player("Marcell", 2)
# startPoint = player1.getPosition()
# print(startPoint)
class ShowStartPoints(): 
    # player1 = Factory.Player("Marcell", 2)
    # StartPoint = player1.getPosition()
    
    def drawStartPoint(Widget):
        return Label        



class IncrediblyCrudeClock(Label):
    a = NumericProperty(5)  # seconds

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        crudeclock.start()
        return crudeclock

if __name__ == "__main__":
    TimeApp().run()