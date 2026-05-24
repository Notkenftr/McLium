class UiPlugin:
    def __init__(self):
        self.name = None
        self.callback = None


class UiEvent:
    def on_input_submitted(self, callback):
        self.callback = callback
