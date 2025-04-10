class Action:
    def __init__(self, game, line):
        self.game = game
        self.line = line

    # 所有操作前
    def pre_action(self):
        pass

    # 所有操作后
    def after_action(self):
        pass

    # 识别前
    def pre_recognition(self):
        pass

    # 识别后
    def after_recognition(self):
        pass

    # 满足条件后才会执行 action
    def condition(self):
        pass

    # 具体执行action
    def action(self):
        pass

    # 解析代码行
    def parse(self, parts, script):
        pass