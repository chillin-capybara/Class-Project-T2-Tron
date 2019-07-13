from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation
from Backend.Core.Vect2D import Vect2D

Builder.load_string("""
<CountdownWidget>:
    # Widget for the countdown sequence
    Label:
        size_hint: ( .2, .1)
        pos_hint: {'x': .4, 'y': .45}
        color: 1, 1, 1, 1
        # counter function is implemented
        text: "Finished" if root.counter == 0 else str(round(root.counter, 1))
""")

class CountdownWidget(Widget):
    start_value = NumericProperty()
    counter = NumericProperty(-1)

    def __init__(self, **kwargs):
        # cunstructor for register the event
        super(CountdownWidget, self).__init__(**kwargs)
        self.register_event_type("on_finished") # Event registrieren

    def start(self):
        # function initializing the countdown
        Animation.cancel_all(self)
        self.counter = self.start_value
        self.anim = Animation(counter=0, duration=self.start_value)

        def finish_callback(animation, _):
            self.dispatch("on_finished")

        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    # Events
    def on_finished(self):
        pass