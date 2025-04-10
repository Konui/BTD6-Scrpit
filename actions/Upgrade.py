from actions import Action

class Upgrade(Action):
    def __init__(self, game, line):
        super().__init__(game, line)
        self.x = None
        self.y = None
        self.path = None

    def condition(self):
        need_money = [self.game.upgrade1, self.game.upgrade2, self.game.upgrade3][self.path]
        if need_money is None or self.game.money is None:
            return False
        return self.game.money >= need_money

    def pre_action(self):
        self.game.sleep()
        self.game.mouse_move(self.x, self.y)
        self.game.mouse_click()
        self.game.sleep()

    def after_action(self):
        self.game.mouse_move(self.x, self.y)
        self.game.mouse_click()
        self.game.sleep()

    def action(self):
        self.game.keyboard_tap([',','.','/'][self.path])

    def parse(self, parts, script):
        self.path = int(parts[1]) - 1
        positions = parts[2].split(",")
        if len(positions) == 2:
            self.x = int(positions[0])
            self.y = int(positions[1])
        else:
            x,y = script.positions[parts[2]]
            self.x = x
            self.y = y
