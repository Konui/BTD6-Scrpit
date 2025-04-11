from actions import Action
import copy

class Upgrade(Action):
    def __init__(self, context, line):
        super().__init__(context, line)
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

    def parse(self, parts):
        self.parse_position(parts[1])

        self.path = int(parts[2]) - 1
        if len(parts) > 3:
            for _ in range(1, int(parts[3])):
                self.context.script.actions.append(copy.copy(self))
