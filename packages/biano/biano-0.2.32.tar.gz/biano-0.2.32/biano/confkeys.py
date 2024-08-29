#coding=utf-8

import pynput
from buildz.tz import getch
from buildz import xf, Base
from biano import sound1 as sound
import sys,os
# try:
#     from .pynkb import KB
# except:
#     #一般不会报错到这里
#     from .bzkb import KB

# pass
class ConfPress(Base):
    def init(self, conf):
        self.mlefts = conf['left']
        self.mrights = conf['right']
        self.lr2base = {'left':0, 'right':1}
        self.maps = {}
        self.k2base = {}
        self.bases = [40,40]
        self.moves = [0,0]
        for k in self.mlefts:
            self.k2base[k] = 0
            self.maps[k] = self.mlefts[k]
        for k in self.mrights:
            self.k2base[k] = 1
            self.maps[k] = self.mrights[k]
        self.mbases = conf['bases']
        self.moffsets = conf['offsets']
        self.mcombines = conf['combines']
        self.inits = conf['inits']
        self.skb = conf['kb']
        if self.skb == 'full':
            from .pynkb import KB
            self.kb = KB(self.press)
        elif self.skb == 'current':
            from .bzkb import KB
            self.kb = KB(self.press)
        else:
            raise Exception(f"unsupport kb mode: {self.skb}")
    def deal(self, c):
        if c in self.maps:
            kbase = self.k2base[c]
            vc = self.maps[c] + self.bases[kbase]+self.moves[kbase]
            if vc <= 0:
                return
            if vc >= 89:
                return
            sound.sd.play(vc)
        elif c in self.moffsets:
            _map = self.moffsets[c]
            for k in _map:
                self.moves[self.lr2base[k]] = _map[k]
            #print(f"moves: {self.moves}")
        elif c in self.mbases:
            _map = self.mbases[c]
            for k in _map:
                self.bases[self.lr2base[k]] = _map[k]
            #print(f"bases: {self.bases}")
        elif c in self.mcombines:
            mode = self.mcombines[c]
            sound.sd.mode(mode)
    def press(self, key, kb):
        c = kb.char(key)
        if c is not None:
            self.deal(c)
        if kb.is_esc(key):
            kb.stop()
            sound.sd.close()
            sound.release()
    def run(self):
        for c in self.inits:
            self.deal(c)
        lks = list(self.mlefts.keys())
        lks = "".join(lks)
        rks = list(self.mrights.keys())
        rks = "".join(rks)
        nbs = ",".join(list(self.mbases.keys()))
        nofs = ", ".join(list(self.moffsets.keys()))
        ncs = []
        for k,v in self.mcombines.items():
            ncs.append(f"'{k}': '{v}'")
        ncs = ", ".join(ncs)
        print(f"按键: 左手: {lks} 右手: {rks}")
        print(f"修改音调: 按键: {nbs}")
        print(f"修改左右音调偏移: 按键: {nofs}")
        print(f"修改模式: 按键: {ncs}")
        print("按esc退出")
        print(f"press to sound: left: {lks} right: {rks}")
        print(f"change tone: press {nbs}")
        print(f"change left/right tone offset: press {nofs}")
        print(f"change mode: press {ncs}")
        print("press esc to exit")
        #KB(self.press).run()
        self.kb.run()

pass
def run():
    res = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
    dfp = os.path.join(res, "conf.js")
    fp = None
    if len(sys.argv)>1:
        fp = sys.argv[1]
    conf = xf.loadf(dfp)
    if fp is not None:
        bak = fp
        if not os.path.isfile(fp):
            fp = os.path.join(res, fp)
        if not os.path.isfile(fp):
            raise Exception(f"config file not found: {bak}")
        nconf = xf.loadf(fp)
        xf.fill(conf, nconf, 0)
        conf = nconf
    ConfPress(conf).run()
    return

pass
if __name__=="__main__":
    run()

pass
"""
python keys.py
"""