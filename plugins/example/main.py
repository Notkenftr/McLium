from mclium.api.plugin import UiPlugin

class App(UiPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Example"
        self.callback = self.callback_func()

    def callback_func(self):
        print("ok")
