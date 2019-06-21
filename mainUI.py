from kivy.app import App
from kivy.graphics import *
from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from Tron.UI.Classes.GameUI import MyWidget, IncrediblyCrudeClock, AnzeigespielerKivy, ShowStartPoints


# setting display size to 500, 500
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')


class GameApp(App):
    # def build(self):
    #     ObenRechts = AnzeigespielerKivy()
    #     return ObenRechts
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        crudeclock.start()
        return crudeclock
    # def build(self):
    #     game = MyWidget()
    #     return game

if __name__ == "__main__":
    GameApp().run()
    

    