from time import sleep
from tkinter import messagebox

import numpy as np
from pynput import keyboard
from pynput.mouse import Controller as MouseController, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController
import pygetwindow as gw
import pyautogui, cv2
import json

from ocr import OCR

positionFileLocation = "./position.json"
keybindsFileLocation = "./keybinds.json"

'''
获取游戏相关数据 执行游戏相关操作
'''
class Game:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.window_title = "BloonsTD6"
        self.width = 1920
        self.height = 1080
        self.x_offset = 12
        self.y_offset = 44
        self.window = self.__get_window()
        self.ocr = OCR()
        self.sleep_interval = 0.05

        with open(positionFileLocation) as p :
            self.regions = json.load(p)['1k']

        with open(keybindsFileLocation) as k :
            self.keybinds = json.load(k)

        self.money = None
        self.upgrade1 = None
        self.upgrade2 = None
        self.upgrade3 = None
        self.sell_money = None
        self.round = None

    def __get_window(self):
        window = gw.getWindowsWithTitle(self.window_title)
        if len(window) == 1:
            return window[0]
        else:
            print(gw.getAllTitles())
            messagebox.showwarning("警告", f"未找到【{self.window_title}】窗口")

    def position(self):
        window = self.window
        return window.left + self.x_offset, window.top + self.y_offset

    def screenshot(self):
        window = self.window
        return pyautogui.screenshot(region=(window.left + self.x_offset, window.top + self.y_offset , self.width, self.height))

    def mouse_move(self, x, y):
        # 获取最新游戏窗口位置
        win_x, win_y = self.position()

        # 计算绝对坐标并移动
        absolute_x = win_x + x
        absolute_y = win_y + y
        self.mouse.position = (absolute_x, absolute_y)
        print(f"移动鼠标: ({absolute_x}, {absolute_y})")

    def mouse_click(self):
        self.mouse.click(MouseButton.left)
        print("点击鼠标")

    def keyboard_tap(self, key):
        self.keyboard.press(key)
        self.sleep()
        self.keyboard.release(key)
        print(f"按下{key}")

    def activate_window(self):
        self.window.activate()

    def recognition(self):
        screenshot = self.screenshot()
        results = []
        for name, coords in self.regions.items():
            region_img = screenshot.crop(coords)
            results.append(self.ocr.recognition(np.array(region_img)))

        self.reset()
        self.money = self.__parse_money(results[:2])
        self.upgrade1 = self.__parse_money(results[2:4])
        self.upgrade2 = self.__parse_money(results[4:6])
        self.upgrade3 = self.__parse_money(results[6:8])
        self.sell_money = self.__parse_money(results[8:10])
        self.round = self.__parse_round(results[10:12])
        print(f"money: {self.money}, round: {self.round}, upgrade1: {self.upgrade1}, upgrade2: {self.upgrade2}, upgrade3: {self.upgrade3}, sell money: {self.sell_money}")

    def __parse_money(self, arr):
        for res in arr:
            for r in res:
                if (r.startswith("$")):
                    return int(r.replace("$", "").replace(",", ""))
        return None

    def __parse_round(self, arr):
        for res in arr:
            for r in res:
                if "/" in r:
                    return int(r.split("/")[0])

    def sleep(self, interval = None):
        if interval is None:
            interval = self.sleep_interval
        sleep(interval)

    def reset(self):
        self.money = None
        self.upgrade1 = None
        self.upgrade2 = None
        self.upgrade3 = None
        self.sell_money =None
        self.round = None

if __name__ == "__main__":
    game = Game()

    print(game.is_activate())



