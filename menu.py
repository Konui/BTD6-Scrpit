import PIL.Image
import cv2
import numpy as np
from pynput import keyboard

from game import Game
from common import *

auto_start_point = 1290,310
auto_start_color = 120,230,0

alert_area = 750,300, 1200,870

alert_keywords = ['ok', "升级"]

status_area = 1790,970,1880,1055
fast = cv2.imread("img/game/status_fast.png")
slow = cv2.imread("img/game/status_slow.png")
pause = cv2.imread("img/game/status_pause.png")


class Menu:
    def __init__(self, game):
        self.game = game

    def auto_start(self, enable=True):
        self.game.keyboard_tap(keyboard.Key.esc)
        self.game.sleep(self.game.sleep_interval*4)
        screenshot = self.game.screenshot()
        color = screenshot.getpixel()
        status = is_color_similar(color, auto_start_color)
        if status != enable:
            self.game.mouse_move(*auto_start_point)
            self.game.mouse_click()
        self.game.keyboard_tap(keyboard.Key.esc)

    def clear_alert(self):
        result = self.game.recognition([self.game.scale_point(alert_area)])[0]
        for text in result:
            if any(word.lower() in text.lower() for word in alert_keywords):
                print("检查到弹窗")
                self.game.mouse_move(*auto_start_point)
                self.game.mouse_click()
                return

    def status(self):
        target_p = self.game.scale_point(status_area)
        screenshot = self.game.screenshot()
        target = screenshot.crop(target_p)
        target = cv2.cvtColor(np.array(target), cv2.COLOR_RGB2BGR)
        target = self.game.resize(target)

        if match(target, fast):
            return 2
        elif match(target, slow):
            return 1
        elif match(target, pause):
            return 0
        return -1


if __name__ == "__main__":
    g = Game()
    menu = Menu(g)
    print(menu.status())