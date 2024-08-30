#coding=utf-8

from . import sound1 as sound
sd = sound.sd
from buildz import Base, xf
import time, sys, os
import threading as th
res = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")

keys = "1,%1,2,%2,3,4,%4,5,%5,6,%6,7".split(",")
k2n = {k:i for k,i in zip(keys, range(len(keys)))}
base = 40

def v2n(v):
    if v is None:
        return None
    add = 0
    if type(v)==int:
        v = str(v)
    while v[:1]=="*":
        add-=1
        v = v[1:]
    while v[-1:]=="*":
        add+=1
        v = v[:-1]
    if v not in k2n:
        return None
    return k2n[v]+add*12

pass


def rfp(fp):
    bak = fp
    if not os.path.isfile(fp):
        fp = os.path.join(res, fp)
    if not os.path.isfile(fp):
        raise Exception(f"not such file: {bak}")
    return fp

pass
class Play(Base):
    def init(self, sec = 1.0, base = 40):
        self.sec = sec
        self.base = base
        self.lk = th.Lock()
    def single(self, dt, sec, rst, base=0):
        if type(dt)!=list:
            n = v2n(dt)
            if n is not None:
                n += self.base
            rst.append([n, base])
            return 
            #return [n, sec]
        sec /= len(dt)
        for v in dt:
            self.single(v, sec, rst, base)
            base+=sec
        return
    def product(self, data):
        if type(data) in [bytes, str]:
            data = xf.loadf(data)
        rst = []
        for dt in data:
            tmp = []
            self.single(dt, 1.0, tmp)
            rst.append(tmp)
        return rst
    def products(self, datas):
        dts = [self.product(data) for data in datas]
        ls = [len(dt) for dt in dts]
        rst = []
        for i in range(max(ls)):
            tmp = []
            for dt in dts:
                if len(dt)>i:
                    tmp+=dt[i]
            tmp.sort(key = lambda x:x[1])
            rst.append(tmp)
        return rst
    def plays(self, datas):
        if type(datas)!=list:
            datas = [datas]
        rst = self.products(datas)
        for dt in rst:
            prev = 0
            for v,b in dt:
                sec = (b-prev)*self.sec
                if sec>0:
                    time.sleep(sec)
                if v is not None and v>0:
                    sd.play(v)
                prev = b
            left = (1.0-prev)*self.sec
            if left>0:
                time.sleep(left)
    def call(self, fp):
        fp = rfp(fp)
        conf = xf.loadf(fp)
        sec = conf['sec']
        fps = conf['fps']
        sec = xf.g(conf, sec=1.0)
        base = xf.g(conf, base=40)
        sound = xf.g(conf, sound=0.5)
        sd.sound(sound)
        self.sec = sec
        self.base = base
        fps = [rfp(fp) for fp in fps]
        self.plays(fps)

pass

def test():
    fp = "datas/conf.js"
    if len(sys.argv)>1:
        fp = sys.argv[1]
    Play()(fp)

pass
if __name__=="__main__":
    test()

pass