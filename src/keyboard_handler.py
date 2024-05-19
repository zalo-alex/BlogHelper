import time
import keyboard

from src.screenshot import take_screenshot_with_cursor
from src.notification import notify

class KeyboardHandler:
    
    HOTKEYS = {}
    MASTER = None
    
    @staticmethod
    def init(master):
        KeyboardHandler.MASTER = master
        
        
        KeyboardHandler.HOTKEYS = {
            "screenshot": {
                "hotkey": "maj+f1",
                "triggered": KeyboardHandler.on_screenshot_triggered
            },
            "text_note": {
                "hotkey": "maj+f2",
                "triggered": KeyboardHandler.on_text_note_triggered
            }
        }
        
        for name in KeyboardHandler.HOTKEYS.keys():
            KeyboardHandler.set_hotkey(name, KeyboardHandler.HOTKEYS[name]["hotkey"])
    
    @staticmethod
    def set_hotkey(name, hotkey):
        try:
            keyboard.remove_hotkey(KeyboardHandler.HOTKEYS[name]["hotkey"])
        except: pass
        KeyboardHandler.HOTKEYS[name]["hotkey"] = hotkey
        keyboard.add_hotkey(hotkey, KeyboardHandler.HOTKEYS[name]["triggered"])
    
    @staticmethod
    def on_text_note_triggered():
        print("Text note triggered!")
        KeyboardHandler.MASTER.show_page("EditTextNotePage")
    
    @staticmethod
    def on_screenshot_triggered():
        print("Screenshot triggered!")
        img = take_screenshot_with_cursor()
        filename = f"{int(time.time())}.png"
        img.save(f"output\\{filename}")
        notify(KeyboardHandler.MASTER, f"output\\{filename}")