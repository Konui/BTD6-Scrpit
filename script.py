import threading
from time import sleep
from tkinter import messagebox
from pynput import keyboard
from actions import *
from game import Game

def get_all_actions():
    all_subclasses = []

    for subclass in Action.__subclasses__():
        all_subclasses.append(subclass)
    return all_subclasses

class Script:
    def __init__(self, game):
        self.action_dict = {action.__name__.lower(): action for action in get_all_actions()}
        self.game = game
        self.actions = []
        # 0 未开始 1 运行中 2 暂停 3 停止
        self.running = 0
        self.positions = {}
        self.index = 0

        def on_press(key):
            if key == keyboard.Key.ctrl_l:
                print("暂停/恢复")
                self.pause_or_resume()

        keyboard.Listener(on_press=on_press).start()

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
        try:
            action.pre_recognition()
            self.game.recognition()
            action.after_recognition()
        except Exception as e:
            print(e)

    def execute(self):
        print("开始执行")
        print(self.actions)
        self.game.activate_window()
        for action in self.actions:
            action.pre_action()
            self.__process(action)
            while not action.condition():
                if self.running > 1:
                    return
                self.game.sleep(self.game.sleep_interval * 3)
                self.__process(action)
            action.action()
            action.after_action()
            self.index = self.index + 1
            self.game.sleep()
        self.stop()
        print("运行结束")

    def start(self):
        if self.running == 0 or self.running == 3:
            self.reset()
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
        self.index = 0

if __name__ == '__main__':
    g = Game()
    scp = Script(g)
    scp.load("scripts/test.txt")
    scp.start()



