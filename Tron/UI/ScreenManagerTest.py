from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Create all screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Create Server'
            background_color: (0.1,0.5,0.2,53)
            on_press: root.manager.current = 'create'
        Button:
            text: 'Search for Server'
            background_color: (0.1,0.3,0.7,53)
            on_press: root.manager.current = 'search'
        Button:
            text: 'Settings'
            background_color: (0.4,0.2,0.6,53)
            on_press: root.manager.current = 'settings'
        Button:
            text: 'About'
            background_color: (0.1,0.8,0.5,53)
            on_press: root.manager.current = 'about'
        Button:
            text: 'Quit'
            background_color: (1,0.0,0.0,53)
            size_hint: (1, 0.5)
            on_press: exit()

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'My settings button'
            background_color: (0.4,0.2,0.6,53)
        Button:
            text: 'Back to menu'
            background_color: (0.9,0.1,0.1,53)
            size_hint: (1, 0.25)
            on_press: root.manager.current = 'menu'

<AboutScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'A-Moll'
            background_color: (0.1,0.8,0.5,53)
        Button:
            text: 'Back to menu'
            background_color: (0.9,0.1,0.1,53)
            size_hint: (1, 0.25)
            on_press: root.manager.current = 'menu'

<CreateServerScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Creating Server'
            background_color: (0.1,0.5,0.2,53)
        Button:
            text: 'Back to menu'
            background_color: (0.9,0.1,0.1,53)
            size_hint: (1, 0.25)
            on_press: root.manager.current = 'menu'

<SearchforServerScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Searching for Server'
            background_color: (0.1,0.3,0.7,53)
        Button:
            text: 'Back to menu'
            background_color: (0.9,0.1,0.1,53)
            size_hint: (1, 0.25)
            on_press: root.manager.current = 'menu'
""")

# Declare all screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class CreateServerScreen(Screen):
    pass

class SearchforServerScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(AboutScreen(name='about'))
sm.add_widget(CreateServerScreen(name='create'))
sm.add_widget(SearchforServerScreen(name='search'))


class TestApp(App):

    def build(self):
        return sm

    def change(self, instance, *args):
        instance.background_color = (155,0,51,53)

if __name__ == '__main__':
    TestApp().run()