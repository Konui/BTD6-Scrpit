from tkinter import Label, Frame, Button, Tk, Toplevel, StringVar, Entry, Text, filedialog, DISABLED
from tkinter.constants import NORMAL, END
from tkinter.scrolledtext import ScrolledText

from pynput import mouse, keyboard
from game import Game
from pynput.mouse import Controller as MouseController
import time

from script import Script

status_dict = {
    0: "未运行",
    1: "运行中",
    2: "暂停中",
    3: "已结束"
}

class PositionWindow(Toplevel):
    def __init__(self, root, game):
        super().__init__(root)
        self.game = game
        self.title("坐标工具")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        # 初始化变量
        self.current_x = 0
        self.current_y = 0
        self.win_position = (0, 0)
        self.last_pos_update = 0
        self.pressed_keys = set()
        self.keyboard_timer = None

        # GUI元素
        self.position_var = StringVar(value="相对坐标: (0, 0)")
        self.position_label = Label(self, textvariable=self.position_var)
        self.position_label.pack(pady=10)
        Label(self, text="方向键控制鼠标移动", fg="green").pack()

        # 坐标输入框
        input_frame = Frame(self)
        input_frame.pack(pady=5)

        Label(input_frame, text="目标坐标:").pack(side="left")
        self.entry_x = Entry(input_frame, width=6)
        self.entry_x.pack(side="left", padx=2)
        Label(input_frame, text="x").pack(side="left")
        self.entry_y = Entry(input_frame, width=6)
        self.entry_y.pack(side="left", padx=2)

        Button(input_frame, text="移动", command=self.move_to_position).pack(side="left", padx=5)

        self.close_btn = Button(self, text="关闭", command=self.destroy)
        self.close_btn.pack(padx=5, pady=5)

        # 输入设备控制
        self.mouse = MouseController()
        self.mouse_listener = mouse.Listener(on_move=self.on_global_move)
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )

        # 启动监听和定时器
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.start_periodic_update()

    def start_periodic_update(self):
        """启动定时更新"""
        self.update_label()
        self.after(50, self.start_periodic_update)

    def on_global_move(self, x, y):
        """记录当前鼠标位置"""
        self.current_x = x
        self.current_y = y

    def update_label(self):
        """定时更新坐标显示"""
        # 每0.5秒更新一次游戏窗口位置
        if time.time() - self.last_pos_update > 0.5:
            self.win_position = self.game.position()
            self.last_pos_update = time.time()

        win_x, win_y = self.win_position
        rel_x = self.current_x - win_x
        rel_y = self.current_y - win_y
        self.position_var.set(f"相对坐标: ({rel_x}, {rel_y})")

    def handle_keyboard_movement(self):
        """处理持续按键移动"""
        dx, dy = 0, 0
        speed = 3  # 移动步长

        for key in self.pressed_keys:
            if key in (keyboard.Key.left, keyboard.KeyCode.from_vk(100)):
                dx -= speed
            elif key in (keyboard.Key.right, keyboard.KeyCode.from_vk(102)):
                dx += speed
            elif key in (keyboard.Key.up, keyboard.KeyCode.from_vk(104)):
                dy -= speed
            elif key in (keyboard.Key.down, keyboard.KeyCode.from_vk(98)):
                dy += speed

        if dx != 0 or dy != 0:
            self.mouse.move(dx, dy)

        # 保持定时运行直到按键释放
        self.keyboard_timer = self.after(10, self.handle_keyboard_movement)

    def on_key_press(self, key):
        """处理按键按下"""
        try:
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
                if not self.keyboard_timer:
                    self.handle_keyboard_movement()
        except AttributeError:
            pass

    def on_key_release(self, key):
        """处理按键释放"""
        try:
            self.pressed_keys.discard(key)
            if not self.pressed_keys and self.keyboard_timer:
                self.after_cancel(self.keyboard_timer)
                self.keyboard_timer = None
        except AttributeError:
            pass

    def move_to_position(self):
        rel_x = int(self.entry_x.get().strip())
        rel_y = int(self.entry_y.get().strip())
        self.game.mouse_move(rel_x, rel_y)


    def destroy(self):
        """销毁窗口时清理资源"""
        if self.keyboard_timer:
            self.after_cancel(self.keyboard_timer)
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        super().destroy()


class GUI:
    def __init__(self, game):
        self.game = game
        self.script = None

        self.root = Tk()
        self.root.title("Auto BTD6")

        self.frame = Frame(self.root)
        self.frame.pack()

        self.menu_frame = Frame(self.frame)
        self.menu_frame.pack()
        Button(self.menu_frame, text="坐标工具", command=self.open_position_window).pack(side="left")
        Button(self.menu_frame, text="选择脚本", command=self.choice_script).pack(side="left")

        self.control_frame = Frame(self.frame)
        self.control_frame.pack()

        Button(self.control_frame, text="开始", command=self.start).pack(side="left")
        Button(self.control_frame, text="暂停/继续", command=self.pause_or_resume).pack(side="left")
        Button(self.control_frame, text="终止", command=self.stop).pack(side="left")

        self.running_var = StringVar(value=f"{status_dict[0 if self.script is None else self.script.running]}")
        self.runningLabel = Label(self.frame, textvariable=self.running_var)
        self.runningLabel.pack()
        self.path_label = Label(self.frame, text="未选择脚本")
        self.path_label.pack()

        self.text_area = ScrolledText(self.frame, state=DISABLED)
        self.text_area.pack()

        # 初始化标签样式
        self.text_area.tag_config("current", background="yellow")
        self.text_area.tag_config("executed", background="#d4edda", foreground="#155724")
        self.text_area.tag_config("pending", foreground="#6c757d")

        self.content = ''

    def start(self):
        if self.script is not None:
            self.script.start()
            self.update_status()

    def update_status(self):
        if self.script.running < 3:
            self.root.after(300, self.update_status)

        self.running_var.set(f"{status_dict[0 if self.script is None else 2 if not self.game.window.isActive else self.script.running]}")

        line_num = self.script.index + 1
        self.text_area.config(state=NORMAL)
        # 设置当前行高亮
        self.text_area.tag_remove("current", "1.0", "end")
        self.text_area.tag_add("current", f"{line_num}.0", f"{line_num}.end")
        # 已执行的行改为绿色
        if line_num > 1:
            self.text_area.tag_add("executed", f"{line_num-1}.0", f"{line_num-1}.end")
            self.text_area.tag_remove("pending", f"{line_num-1}.0", f"{line_num-1}.end")
            self.text_area.see(f"{line_num}.0")  # 滚动到当前行

        self.text_area.config(state=DISABLED)
        self.root.update()

    def pause_or_resume(self):
        if self.script is not None:
            self.script.pause_or_resume()
            self.update_status()

    def stop(self):
        if self.script is not None:
            self.script.stop()
            self.update_status()

    def reset(self):
        self.text_area.setvar("")
        if self.script is not None:
            self.script.reset()
            self.update_status()

    def choice_script(self):
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.path_label.config(text=file_path)
            # 进一步操作，例如读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.script = Script(self.game)
                    self.script.load(content=content)
                    self.content = '\n'.join([a.line for a in self.script.actions])

                    self.text_area.config(state=NORMAL)
                    self.text_area.delete(1.0, END)
                    self.text_area.insert(END, self.content)

                    # 清除旧标签
                    self.text_area.tag_remove("current", "1.0", "end")
                    self.text_area.tag_remove("executed", "1.0", "end")
                    # 初始所有行设为灰色
                    for i in range(1, self.script.index + 1):
                        self.text_area.tag_add("pending", f"{i}.0", f"{i}.end")
                    self.text_area.config(state=DISABLED)
            except Exception as e:
                self.path_label.config(text=f"读取文件失败: {e}")

    def open_position_window(self):
        PositionWindow(self.root, self.game)

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    gui = GUI(Game())
    gui.mainloop()