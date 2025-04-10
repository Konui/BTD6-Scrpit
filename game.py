from time import sleep
from tkinter import messagebox

import numpy as np
from pynput import keyboard
from pynput.mouse import Controller as MouseController, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController
import pygetwindow as gw
import pyautogui, cv2

from ocr import OCR

money_path_1 = 340,20,550,70
money_path_2 = 730,20,940,70

upgrade_left_1 = 250,500, 400,550
upgrade_right1 = 1470,500, 1620,550
upgrade_left_2 = 250, 650, 400,700
upgrade_right2 = 1470, 650, 1620,700
upgrade_left_3 = 250, 800, 400,855
upgrade_right3 = 1470, 800, 1620,855

sell_money_1 = 100,890, 240, 930
sell_money_2 = 1300,880, 1470, 940

round_1 = 1360,30 ,1560,70
round_2 = 950,30, 1160,70
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
        self.sleep_interval = 0.1

        self.regions = {
            "money_1": money_path_1,
            "money_2": money_path_2,
            "upgrade_left_1": upgrade_left_1,
            "upgrade_right_1": upgrade_right1,
            "upgrade_left_2": upgrade_left_2,
            "upgrade_right_2": upgrade_right2,
            "upgrade_left_3": upgrade_left_3,
            "upgrade_right_3": upgrade_right3,
            "sell_money_1": sell_money_1,
            "sell_money_2": sell_money_2,
            "round_1": round_1,
            "round_2": round_2,
        }
        self.last_screenshot = None
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
        self.last_screenshot = screenshot
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
        self.last_screenshot = None
        self.money = None
        self.upgrade1 = None
        self.upgrade2 = None
        self.upgrade3 = None
        self.sell_money =None
        self.round = None

if __name__ == "__main__":
    game = Game()

    print(game.is_activate())



