#coding=utf-8
from buildz import pyz, WBase
class KB(WBase):
    def stop(self):
        pass
    def char(self, key):
        return None
    def is_esc(self, key):
        return True
    def run(self):
        pass
    def init(self, callback):
        """
            callback(press_key, KB)
        """
        self.callback = callback

pass