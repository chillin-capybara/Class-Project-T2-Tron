# from Tron.Backend.Classes.Player import Player
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
 
# player1 = Player.getName()
class AnzeigespielerKivy(Label):
    def start(self):
        return Label(text="Welcome to LikeGeeks!", background_color=(155,0,51,53))

    
class OrApp(App):
    def build(self):
        ObenRechts = AnzeigespielerKivy()
        ObenRechts.start()
        return ObenRechts

if __name__ == "__main__":
    OrApp().run()
