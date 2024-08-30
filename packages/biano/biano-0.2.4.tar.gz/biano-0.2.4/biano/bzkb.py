#coding=utf-8

from buildz import pyz, WBase
from buildz.tz import getch
from . import kb
class KB(kb.KB):
    def _open(self):
        getch.open()
    def _close(self):
        getch.close()
    def stop(self):
        self.running = False
    def char(self, key):
        return chr(key)
    def is_esc(self, key):
        return key==27
    def run(self):
        self.running=True
        with self.open():
            while self.running:
                v = getch()
                self.callback(v, self)
    def init(self, callback):
        self.callback = callback
        self.running = False

pass