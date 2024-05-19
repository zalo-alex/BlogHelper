import pyautogui
import win32api
import numpy as np
from PIL import ImageGrab

def get_cursor_position():
    return pyautogui.position()

def get_screen_with_cursor():
    cursor_x, cursor_y = get_cursor_position()
    monitor = win32api.MonitorFromPoint((cursor_x, cursor_y))
    info = win32api.GetMonitorInfo(monitor)
    return info["Monitor"]

def take_screenshot(screen):
    left, top, right, bottom = screen
    return ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True)

def take_screenshot_with_cursor():
    screen = get_screen_with_cursor()
    return take_screenshot(screen)