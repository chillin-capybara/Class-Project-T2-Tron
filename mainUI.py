from Tron.UI.Classes.Line import MyWidget

class TrackApp(App):
    def build(self):
        game = MyWidget()
        return game

if __name__ == "__main__":
    TrackApp().run()