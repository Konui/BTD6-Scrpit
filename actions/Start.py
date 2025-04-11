from pynput import keyboard

from actions import Action

class Start(Action):
    def __init__(self, context, line):
        super().__init__(context, line)

    def loop(self):
        self.game.keyboard_tap(keyboard.Key.space)
        self.game.keyboard_tap(keyboard.Key.space)
        return True

    def parse(self, parts):
        pass