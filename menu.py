from pynput import keyboard

from game import Game
from common import *

auto_start_point = 1290,310
auto_start_color = 120,230,0

alert_area = 750,300, 1200,870

alert_keywords = ['ok', "升级"]

class Menu:
    def __init__(self, game):
        self.game = game

    def auto_start(self, enable=True):
        self.game.keyboard_tap(keyboard.Key.esc)
        self.game.sleep(self.game.sleep_interval*4)
        screenshot = self.game.screenshot()
        color = screenshot.getpixel(auto_start_point)
        status = is_color_similar(color, auto_start_color)
        if status != enable:
            self.game.mouse_move(*auto_start_point)
            self.game.mouse_click()
        self.game.keyboard_tap(keyboard.Key.esc)

    def clear_alert(self):
        result = self.game.recognition([alert_area])[0]
        for text in result:
            if any(word.lower() in text.lower() for word in alert_keywords):
                print("检查到弹窗")
                self.game.mouse_move(*auto_start_point)
                self.game.mouse_click()
                return

if __name__ == "__main__":
    g = Game()
    menu = Menu(g)
    menu.clear_alert()