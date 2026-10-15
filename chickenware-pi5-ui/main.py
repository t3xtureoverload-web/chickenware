from kivy.config import Config
from ffpyplayer.player import MediaPlayer
Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "720")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty


player = MediaPlayer(
    "tcp://10.42.0.1:8888",
    ff_opts={
        "vf": ["setpts=N/15"],
        "framedrop": True,
    },
    lib_opts={
        "fflags": "nobuffer",
        "flags": "low_delay",
    },
)


class Panel(Widget):
    gatestate = NumericProperty(0)


#eventually add a middle value for 'opening' or 'closing' in orange to prevent spamming. this should be confirmable with a servo.
    def toggle_gate(self, button):
        if self.gatestate == 0:
            button.text = "OPENED"
            button.background_color = (1, 0, 0, 1)
            self.gatestate = 1
        else:
            button.text = "CLOSED"
            button.background_color = (0, 1, 0, 1)
            self.gatestate = 0

class PanelApp(App):
    def build(self):
        return Panel()


if __name__ == '__main__':
    PanelApp().run()