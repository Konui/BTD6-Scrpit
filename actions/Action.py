from menu import *

class Action:
    def __init__(self, context, line):
        self.context = context
        self.game = context.game
        self.menu = context.menu
        self.line = line

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
        return not self.loop()

    # 返回True跳出循环
    def loop(self):
        pass

    # 解析代码行
    def parse(self, parts, script):
        pass