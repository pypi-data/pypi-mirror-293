#coding=utf-8

from pynput.keyboard import Listener, Key
from . import kb
class KB(kb.KB):
    def char(self, key):
        if hasattr(key, "char"):
            return key.char
        return None
    def is_esc(self, key):
        return key == Key.esc
    def stop(self):
        self.lst.stop()
    def init(self, callback):
        super().init(callback)
        self.pressed = set()
    def press(self, key):
        if hasattr(key, "char"):
            c = key.char
            if c in self.pressed:
                return
            self.pressed.add(c)
        self.callback(key, self)
    def release(self, key):
        if hasattr(key, "char"):
            c = key.char
            if c in self.pressed:
                self.pressed.remove(c)
    def run(self):
        with Listener(on_press=self.press, on_release=self.release) as lst:
            self.lst = lst
            lst.join()

pass