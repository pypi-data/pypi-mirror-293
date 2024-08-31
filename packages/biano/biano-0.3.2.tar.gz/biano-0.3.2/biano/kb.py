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
    def set_callback(self, callback):
        self.callback = callback
    def init(self, callback=None):
        """
            callback(press_key, KB)
        """
        self.callback = callback

pass