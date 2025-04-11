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

    def loop(self):
        self.__place()
        self.game.sleep()
        self.game.mouse_click()
        self.game.sleep()
        # 获取状态信息
        sell_money = self.game.rec_sell_money()
        self.game.mouse_click()
        return sell_money is not None

    def __place(self):
        self.game.mouse_move(self.x, self.y)
        self.game.keyboard_tap(self.key)
        self.game.sleep()
        self.game.mouse_click()

    def parse(self, parts, script):
        self.key = parts[1]
        positions = parts[2].split(",")
        self.x = int(positions[0])
        self.y = int(positions[1])
        if len(parts) > 3:
            script.positions[parts[3]] = self.x, self.y