from actions import Action

class AutoStart(Action):
    def __init__(self, game, line):
        super().__init__(game, line)
        self.x = None
        self.y = None
        self.enable = True

    def condition(self):
        self.game.keyboard_tap(self.game.keybinds['exit'])
        self.game.sleep()

        sc = self.game.screenshot()
        
        return self.game.money >= need_money

    def pre_action(self):
        self.game.mouse_move(self.x, self.y)
        self.game.sleep()
        self.game.mouse_click()
        self.game.sleep()

    def after_action(self):
        self.game.mouse_move(self.x, self.y)
        self.game.sleep()
        self.game.mouse_click()

    def action(self):
        self.game.keyboard_tap([',','.','/'][self.path])

    def parse(self, parts, script):
        self.times = parts[-1]
        self.path = parts[-2]
        positions = parts[2].split(",")
        if len(positions) == 2:
            self.x = int(positions[0])
            self.y = int(positions[1])
        else:
            x,y = script.positions[parts[2]]
            self.x = x
            self.y = y
