#coding=utf-8

from . import sound1 as sound
#sd = sound.sd
from buildz import Base, xf, pyz, fz
import time, sys, os
import threading as th
from . import ioc
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

from .tools import rfp
class Play(Base):
    def init(self, sd, sec = 1.0, base = 40):
        self.sd = sd
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
        self.run(rst)
    def run(self, rst):
        for dt in rst:
            prev = 0
            for v,b in dt:
                sec = (b-prev)*self.sec
                if sec>0:
                    time.sleep(sec)
                if v is not None and v>0:
                    self.sd.play(v)
                prev = b
            left = (1.0-prev)*self.sec
            if left>0:
                time.sleep(left)
    def replay(self, fp):
        self.sd.start()
        fp = rfp(fp)
        rds = xf.loadf(fp)
        self.simple(rds)
    def simple(self, dt):
        base = 0.0
        for v,b in dt:
            sec = (b-base)
            if sec>0:
                time.sleep(sec)
            if v is not None and v>0:
                self.sd.play(v)
            base = b
        time.sleep(1.0)
    def call(self, fp):
        self.sd.start()
        fp = rfp(fp)
        conf = xf.loadf(fp)
        sec = conf['sec']
        fps = conf['fps']
        sec = xf.g(conf, sec=1.0)
        base = xf.g(conf, base=40)
        sound = xf.g(conf, sound=0.5)
        self.sd.sound(sound)
        self.sec = sec
        self.base = base
        fps = [rfp(fp) for fp in fps]
        self.plays(fps)

pass

def test():
    mg = ioc.build("default_env.js")
    fp = "datas/conf.js"
    if len(sys.argv)>1:
        fp = sys.argv[1]
    mg.set_env("play.confs", fp)
    mg.get("play")

pass
pyz.bylocals(locals(), test)