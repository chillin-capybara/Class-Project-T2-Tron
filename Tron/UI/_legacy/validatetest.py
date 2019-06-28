from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty
import re

KV = """

<ValidateLabel>:
    size_hint: (None, None)
    size: (280, 60)
    Label:
        id: label
        text: "Must be a float"


<MyInput>:
    foreground_color: (0,1,0,1) if root.validated else (1,0,0,1)


FloatInput:

"""


class MyInput(TextInput):
    validated = BooleanProperty(False)


class FloatInput(FloatLayout):
    bubble_showed = True

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.input = MyInput()
        self.input.bind(text=self.validate)
        self.add_widget(self.input)
        self.bubble = ValidateLabel()
        self.add_widget(self.bubble)

    def validate(self, input, value, min_value=15., max_value=25.):
        self.bubble.ids.label.text = "IP needs to look like 123.456.789.897"
        try:
            print(min_value, max_value)
            iplist = value.split(".")
            print(iplist)
            for e in iplist:
                if value == "":
                    self.bubble.ids.label.text = "IP needs to look like 123.456.789.897"
                    status = False
                elif len(e) == 3 and len(iplist) == 4:
                    print("Schleife länge 3")
                    status = True
                elif len(iplist) != 4:
                    print("Länge nicht vier")
                    status = False
                    self.bubble.ids.label.text = "Input must be an valid IP"
                else:
                    status = False
                    self.bubble.ids.label.text = "Input must be an valid IP"
            #status = float(min_value) <= float(value) <= float(max_value)
        except Exception as e:
            status = False
            self.bubble.ids.label.text = "Input must be an valid IP"

        if not status:
            if not self.bubble_showed:
                self.input.validated = False
                self.add_widget(self.bubble)
                self.bubble_showed = True
        else:
            print("bubble removed")
            self.input.validated = True
            self.remove_widget(self.bubble)
            self.bubble_showed = False


class ValidateLabel(Bubble):
    validated = False


class TestApp(App):

    def build(self):
        return Builder.load_string(KV)


TestApp().run()