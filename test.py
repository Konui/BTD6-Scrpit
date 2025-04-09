import win32api
import win32con
import win32gui

hwnd = win32gui.FindWindow(None, "BloonsTD6")
if hwnd == 0:
    raise Exception("未找到窗口")

# win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
# win32gui.SetForegroundWindow(hwnd)

# win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
# win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)
x= 250
y = 910
win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, y << 16 | x)
win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, y << 16 | x)