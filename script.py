from time import sleep
from tkinter import messagebox
from pynput import keyboard
from actions import *
from game import Game
from job import JobTemplate, JobStatus


def get_all_actions():
    all_subclasses = []

    for subclass in Action.__subclasses__():
        all_subclasses.append(subclass)
    return all_subclasses

class Script(JobTemplate):
    def __init__(self, game):
        super().__init__()
        self.action_dict = {action.__name__.lower(): action for action in get_all_actions()}
        self.game = game
        self.actions = []
        self.positions = {}
        self.index = 0

        def on_press(key):
            if key == keyboard.Key.ctrl_l:
                print("暂停/恢复")
                self.pause_or_resume()

        listener = keyboard.Listener(on_press=on_press)
        listener.daemon=True
        listener.start()

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
        if not self.game.window.isActive or self._status != JobStatus.RUNNING:
            return
        print(action.line)
        try:
            action.pre_recognition()
            self.game.recognition()
            action.after_recognition()
        except Exception as e:
            print(e)

    def _run_task(self):
        print("开始执行")
        print(self.actions)
        for action in self.actions:
            if self._stop_event.is_set():
                break
            elif self._status == JobStatus.PAUSED:
                self._pause_event.wait()

            action.pre_action()
            self.__process(action)
            while not action.condition():
                if self._stop_event.is_set():
                    break
                elif self._status == JobStatus.PAUSED:
                    self._pause_event.wait()
                self.game.sleep(self.game.sleep_interval * 3)
                self.__process(action)
            action.action()
            action.after_action()
            self.index = self.index + 1
            self.game.sleep()
        self.stop()


    def reset(self):
        super().reset()
        self.index = 0

if __name__ == '__main__':
    g = Game()
    scp = Script(g)
    scp.load("scripts/test.txt")
    scp.start()

    sleep(5)
    scp.pause_or_resume()
    sleep(5)
    scp.pause_or_resume()

    scp.join()

    print(scp.status)



