from actions import Action

'''
place u 120,120
'''
class Place(Action):
    def __init__(self, game, line):
        super().__init__(game, line)
        self.key = None
        self.x = None
        self.y = None

    def condition(self):
        return self.game.sell_money is not None

    def pre_recognition(self):
        self.__place()
        self.game.sleep()
        self.game.mouse_click()
        self.game.sleep(0.5)

    def after_recognition(self):
        self.game.mouse_click()

    def __place(self):
        self.game.mouse_move(self.x, self.y)
        self.game.keyboard_tap(self.key)
        self.game.sleep()
        self.game.mouse_click()

    def action(self):
        pass

    def parse(self, parts, script):
        self.key = parts[1]
        positions = parts[2].split(",")
        self.x = int(positions[0])
        self.y = int(positions[1])
        if len(parts) > 3:
            script.positions[parts[3]] = self.x, self.y