#coding=utf-8

import pynput
from buildz.tz import getch
from buildz import xf, Base, fz
from biano import sound1 as sound
import sys,os
from .tools import rfp
import time
# try:
#     from .pynkb import KB
# except:
#     #一般不会报错到这里
#     from .bzkb import KB

# pass
class ConfPress(Base):
    def init(self, conf, sd, kb=None):
        self.mlefts = conf['left']
        self.mrights = conf['right']
        self.lr2base = {'left':0, 'right':1}
        self.maps = {}
        self.k2base = {}
        self.bases = [40,40]
        self.moves = [0,0]
        self.records = []
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
        #self.vsound = xf.g(conf, sound=1.0)
        self.quit = xf.g(conf, quit = "esc")
        self.save_records = xf.g(conf, save_records = False)
        self.sd = sd
        #self.sd.sound(self.vsound)
        if kb is None:
            if self.skb == 'full':
                from .pynkb import KB
                self.kb = KB(self.press)
            elif self.skb == 'current':
                from .bzkb import KB
                self.kb = KB(self.press)
            else:
                raise Exception(f"unsupport kb mode: {self.skb}")
        else:
            self.kb = kb
    def deal(self, c):
        if c in self.maps:
            kbase = self.k2base[c]
            vc = self.maps[c] + self.bases[kbase]+self.moves[kbase]
            if vc <= 0:
                return
            if vc >= 89:
                return
            if self.save_records:
                self.records.append([vc, time.time()])
            self.sd.play(vc)
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
            self.sd.mode(mode)
    def is_quit(self, key, c, kb):
        if self.quit == "esc":
            return kb.is_esc(key)
        return self.quit==c
    def press(self, key, kb):
        c = kb.char(key)
        if c is not None:
            self.deal(c)
        if self.is_quit(key, c, kb):
            kb.stop()
            self.sd.close()
            self.try_save()
    def try_save(self):
        if not self.save_records or len(self.records)==0:
            return
        date = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        fp = f"record_{date}.js"
        rds = self.records
        base = rds[0][1]
        rds = [[v, b-base] for v,b in rds]
        rs = xf.dumps(rds)
        fz.write(rs, fp, 'w')
        print(f"记录已经保存至'{fp}'，可以运行\n    python -m biano.replay \"{fp}\"\n重放")
    def run(self):
        self.sd.start()
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
        #print(f"修改模式: 按键: {ncs}")
        print(f"按'{self.quit}'退出")
        print(f"press to sound: left: {lks} right: {rks}")
        print(f"change tone: press {nbs}")
        print(f"change left/right tone offset: press {nofs}")
        #print(f"change mode: press {ncs}")
        print(f"press '{self.quit}' to exit")
        #KB(self.press).run()
        self.kb.run()

pass
def build(fps, sd, kb=None):
    fps = [rfp(fp) for fp in fps if fp is not None]
    conf = None
    for fp in fps:
        _conf = xf.loadf(fp)
        if conf is None:
            conf = _conf
        else:
            xf.fill(_conf, conf, 1)
    return ConfPress(conf, sd, kb)

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