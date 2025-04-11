import traceback

from menu import *

class Action:
    def __init__(self, context, line):
        self.context = context
        self.game = context.game
        self.menu = context.menu
        self.line = line

        self.x = None
        self.y = None

    # 所有操作前
    def pre_action(self):
        pass

    # 所有操作后
    def post_action(self):
        pass

    # 满足条件后才会执行 action
    def cond_loop(self):
        if not self.game.window.isActive:
            return True
        self.menu.clear_alert()
        try:
            return not self.loop()
        except:
            traceback.print_exc()

    # 返回True跳出循环
    def loop(self):
        pass

    # 解析代码行
    def parse(self, parts):
        pass

    def parse_position(self, position):
        positions = position.split(",")
        if len(positions) == 2:
            self.x = int(positions[0])
            self.y = int(positions[1])
        else:
            x,y = self.context.script.positions[position]
            self.x = x
            self.y = y