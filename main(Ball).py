# imports for ball-class
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock

# imports for key input
import kivy
kivy.require('1.0.8')

from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.widget import Widget


# Classes for key input
class MyKeyboardListener(Widget):

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
        
        # Direction up
        if keycode[1] == 'w':
            self._game.set_velocity(0, 1)

        if keycode[1] == 'a':
            self._game.set_velocity(-1, 0)

        if keycode[1] == 's':
            self._game.set_velocity(0, -1)

        if keycode[1] == 'd':
            self._game.set_velocity(1, 0)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True




# Classes for representing the ball + Movement of the ball
class PongBall(Widget):
    def move(self, move_distance):
        self.pos = move_distance + self.pos


class BallGame(Widget):
    balls = []
    velocity = (1, 0) # (x, y)
    speed_constant = 0.01
    speed_factor = 1

    length_counter = 0
    length_threshhold = 10

    def __init__(self, **kwargs):
        super(BallGame, self).__init__(**kwargs)

        # add second and more balls
        with self.canvas:
            for i in range(10):
                ball = PongBall()
                self.balls.append(ball)

    def set_velocity(self, x = velocity[0], y = velocity[1]):
        self.velocity = (x, y)


    # 
    def update(self, dt):
        self.length_counter += 1
        if self.length_counter >= self.length_threshhold:
            self.length_counter = 0

            # with self.canvas:
            #     ball = PongBall()
            #     last_ball_ps = self.balls[-1].pos
            #     self.balls.append(ball)

        old_pos = self.balls[0].pos
        self.speed_factor = self.speed_factor + self.speed_constant
        self.balls[0].pos = (
            old_pos[0] + self.velocity[0] * self.speed_factor * 10,
            old_pos[1] + self.velocity[1] * self.speed_factor * 10
        )

        if len(self.balls) > 1:
            for i in range(len(self.balls)):
                tmp_pos = self.balls[i].pos 
                self.balls[i].pos = old_pos
                old_pos = tmp_pos


class BallApp(App):
    def build(self):
        game = BallGame()
        Clock.schedule_interval(game.update, 0.05)
        MyKeyboardListener(game)
        return game

        print ("Hello")
        print("bye")


if __name__ == '__main__':
    BallApp().run()