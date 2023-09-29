import win32gui
import win32con
import win32api
import time


def HindWindows(hwnd):
    win32gui.ShowWindow(hwnd, 0)


def ShowWindows(hwnd):
    win32gui.ShowWindow(hwnd, 5)
    
def doTop(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def reset(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                          win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def doDown(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,
                          win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def doDisabled(hwnd):
    c, a, s = getold(hwnd)
    exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT  # 能改顏色，能穿透
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exStyle)
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), a, win32con.LWA_ALPHA)


def doAbled(hwnd):
    c, a, s = getold(hwnd)
    exStyle = win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exStyle)
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), a, win32con.LWA_ALPHA)


def setAlpha(hwnd, alpha):
    exStyle = win32con.WS_EX_LAYERED
    exStyle |= win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exStyle)
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)


def getold(hwnd):
    try:
        return win32gui.GetLayeredWindowAttributes(hwnd)
    except:
        return (0, 255, 2)


def movewindows(hwnd, x, y):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    new_left = x
    new_top = y
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_left,
                          new_top, width, height, win32con.SWP_SHOWWINDOW)


def big(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

def flashing(hwnd,t):
    win32gui.FlashWindow(hwnd,t)
if __name__ == '__main__':
    x = 2622632
    # doDisabled(x)
    # doAbled(x)
    # HindWindows(x)
    # ShowWindows(x)
    # doTop(x)
    # doDown(x)
    # print(win32con.WS_EX_LAYERED)
