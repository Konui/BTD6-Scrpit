from actions import Action

'''
place u 120,120
'''
class Place(Action):
    def __init__(self, context, line):
        super().__init__(context, line)
        self.key = None
        self.x = None
        self.y = None

    # to do 后续如果不可用考虑匹配地板前后相似度
    def loop(self):
        # 获取状态信息
        first_money = self.game.rec_money()
        self.__place()
        self.game.sleep()
        second_money = self.game.rec_money()
        #放成功少点一下
        if first_money is None or second_money is None:
            return False
        if first_money > second_money:
            return True
        self.game.mouse_click()
        print(first_money, second_money)
        return False

    def __place(self):
        self.game.mouse_move(self.x, self.y)
        self.game.keyboard_tap(self.key)
        self.game.sleep()
        self.game.mouse_click()

    def parse(self, parts):
        self.key = parts[1]
        positions = parts[2].split(",")
        self.x = int(positions[0])
        self.y = int(positions[1])
        if len(parts) > 3:
            self.context.script.positions[parts[3]] = self.x, self.y