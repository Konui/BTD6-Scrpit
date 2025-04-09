import threading
from time import sleep
from tkinter import messagebox

from pyasn1_modules.rfc8410 import id_X448

from game import Game

def get_all_actions():
    all_subclasses = []

    for subclass in Action.__subclasses__():
        all_subclasses.append(subclass)
    return all_subclasses


class Action:
    def __init__(self, game, line):
        self.game = game
        self.line = line

    def pre_recognition(self):
        pass

    def after_recognition(self):
        pass

    def condition(self):
        pass

    def action(self):
        pass

    def parse(self, parts, script):
        pass

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
        self.game.mouse_move(self.x, self.y)
        self.game.sleep()
        self.game.mouse_click()
        self.game.sleep(0.5)

    def after_recognition(self):
        self.game.mouse_click()

    def __place(self):
        self.game.mouse_move(self.x, self.y)
        self.game.sleep()
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


class Upgrade(Action):
    def __init__(self, game, line):
        super().__init__(game, line)
        self.x = None
        self.y = None
        self.path = None

    def condition(self):
        return self.game.money > [self.game.upgrade1, self.game.upgrade2, self.game.upgrade3][self.path]

    def pre_recognition(self):
        self.game.mouse_move(self.x, self.y)
        self.game.sleep()
        self.game.mouse_click()
        self.game.sleep(0.5)

    def after_recognition(self):
        self.game.mouse_click()

    def action(self):
        self.game.mouse_move(self.x, self.y)
        self.game.sleep()
        self.game.mouse_click()
        self.game.sleep()
        self.game.keyboard_tap([',','.','/'][self.path])
        self.game.sleep()
        self.game.mouse_click()

    def parse(self, parts, script):
        self.path = int(parts[1]) - 1
        positions = parts[2].split(",")
        if len(parts) == 2:
            self.x = int(positions[0])
            self.y = int(positions[1])
        else:
            x,y = script.positions[parts[2]]
            self.x = x
            self.y = y

class Script:
    def __init__(self, game):
        self.action_dict = {action.__name__.lower(): action for action in get_all_actions()}
        self.game = game
        self.actions = []
        # 0 未开始 1 运行中 2 暂停 3 停止
        self.running = 0
        self.positions = {}

    def load(self, path=None, content=None):
        lines = []
        if path is not None:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        elif content is not None:
            lines = content.split('\n')
        else:
            raise Exception("请输入脚本路径或内容")

        for line in lines:
            line = line.strip()

            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue

            try:
                parts = line.split(" ")
                action_name = parts[0]
                action_cls = self.action_dict[action_name.lower()]
                if action_cls:
                    action = action_cls(self.game, line)
                    self.actions.append(action)
                    action.parse(parts, self)
                else:
                    messagebox.showwarning("错误", f"解析脚本错误:\n{line}")
                    raise Exception("脚本解析失败")
            except Exception as e:
                print(e)
                messagebox.showwarning("错误", f"解析脚本错误:\n{line}")
                raise Exception("脚本解析失败")

    def __process(self, action):
        if not self.game.window.isActive or self.running > 1:
            return
        print(action.line)
        action.pre_recognition()
        self.game.recognition()
        action.after_recognition()

    def execute(self):
        print("开始执行")
        print(self.actions)
        for action in self.actions:
            self.__process(action)
            while not action.condition():
                if self.running > 1:
                    return
                sleep(1)
                self.__process(action)
            action.action()
        self.stop()
        print("运行结束")

    def start(self):
        self.running = 1
        threading.Thread(target=self.execute).start()

    def stop(self):
        self.running = 3

    def pause_or_resume(self):
        if self.running == 1:
            self.running = 2
        elif self.running == 2:
            self.running = 1
        return self.running

    def reset(self):
        self.running = 0

if __name__ == '__main__':
    sleep(2)
    g = Game()
    scp = Script(g)
    scp.load("scripts/test.txt")
    scp.start()


