from pynput import keyboard

from actions import Action

class Retarget(Action):
    def __init__(self, context, line):
        super().__init__(context, line)
        self.x = None
        self.y = None
        self.count = 1

    def loop(self):
        self.game.mouse_move(self.x, self.y)
        self.game.mouse_click()
        for _ in range(self.count):
            self.game.sleep()
            self.game.keyboard_tap(keyboard.Key.tab)
        return True

    def parse(self, parts):
        self.parse_position(parts[1])

        if len(parts) > 2:
            self.count = int(parts[2])