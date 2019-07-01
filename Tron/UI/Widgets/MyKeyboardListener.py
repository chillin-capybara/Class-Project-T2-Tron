from kivy.uix.widget import Widget
from kivy.core.window import Window
import UI.mainUI
from Backend.Core.Vect2D import Vect2D


class MyKeyboardListener(Widget):
    ## keyboard listener, listen to keyboard inputs

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)

        self._game = UI.mainUI.CLIENT
        print (UI.mainUI.CLIENT.me.getName)
        self._player = self._game.me
        print(self._player)
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
        
        # enterPause Menu
        if keycode[1] == 'p':
            print("not Implemented Yet Pause Menu")
            keyboard.release()

        if keycode[1] == 'a':
            self.press_a_key()

        if keycode[1] == 'd':
            self.press_d_key()
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def press_d_key(self):
        ## is triggered by keyboard listener, if I have a velocity vector in a certain direction, I need to change that velocity
        ## with d we go clockwise
        if self._player.getVelocity().x == 1 and self._player.getVelocity().y == 0:
            self._player.setVelocity(0, -1)
            
            return

        if self._player.getVelocity().x == 0 and self._player.getVelocity().y == 1:
            self._player.setVelocity(1, 0)
            return

        if self._player.getVelocity().x == -1 and self._player.getVelocity().y == 0:
            self._player.setVelocity(0, 1)
            return


        if self._player.getVelocity().x == 0 and self._player.getVelocity().y == -1:
            self._player.setVelocity(-1, 0)
            return
    

    def press_a_key(self):
        ## is triggered by keyboard listener, if I have a velocity vector in a certain direction, I need to change that velocity
        ## with a we go counter-clockwise
        if self._player.getVelocity().x == 1 and self._player.getVelocity().y == 0:
            self._player.setVelocity(0, 1)
            return

        if self._player.getVelocity().x == 0 and self._player.getVelocity().y == 1:
            self._player.setVelocity(-1, 0)
            return
            
        if self._player.getVelocity().x == -1 and self._player.getVelocity().y == 0:
            self._player.setVelocity(0, -1)
            return

        if self._player.getVelocity().x == 0 and self._player.getVelocity().y == -1:
            self._player.setVelocity(1, 0)
            return

