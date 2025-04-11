from actions import Action
import copy

class Upgrade(Action):
    def __init__(self, game, line):
        super().__init__(game, line)
        self.x = None
        self.y = None
        self.path = None

    def loop(self):
        money, upgrade_money = self.game.rec_upgrade_path(self.path)
        print(money, upgrade_money)
        if upgrade_money is None or money is None:
            return False
        elif money >= upgrade_money:
            self.game.keyboard_tap([',', '.', '/'][self.path])
            return True
        return False

    def pre_action(self):
        self.game.mouse_move(self.x, self.y)
        self.game.mouse_click()
        # 等待窗口动画
        self.game.sleep()

    def post_action(self):
        self.game.mouse_move(self.x, self.y)
        self.game.mouse_click()
        # 等待窗口动画
        self.game.sleep()

    def parse(self, parts, script):
        positions = parts[1].split(",")
        if len(positions) == 2:
            self.x = int(positions[0])
            self.y = int(positions[1])
        else:
            x,y = script.positions[parts[1]]
            self.x = x
            self.y = y

        self.path = int(parts[2]) - 1
        if len(parts) > 3:
            for _ in range(1, int(parts[3])):
                script.actions.append(copy.copy(self))
