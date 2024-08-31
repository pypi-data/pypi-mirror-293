#coding=utf-8

import pyaudio
import numpy as np
import math
from . import cache
from buildz import Base
fps = 4096*10*8
p = pyaudio.PyAudio()
nbyte = 2
ndtype = np.int16
nmax = (1<<(nbyte<<3))-1

nrange = nmax/2
nrange = (nmax+1)/2
def fn(n):
    """
        乐谱音符转频率
        C1: n=4 fn(4)=32.703
        C1#: n=5
        D1: n=6
    """
    return 27.5*(2**(1/12))**(n-1)

pass

mid = 50
import random
def f3(rate, n, sec = 1.0, msound = 1.0, index=0):
    """
    rate: 频率
    n: 乐谱音符（1234567）
    sec: 声波发音时间，单位秒
    msound: 全局音量大小
    """
    global fps #每秒取样数
    size = int(fps * sec)
    #data = np.zeros(size+int(size*0.5), dtype = np.float32)
    data = np.arange(0,size+int(size*0.5)*0, 1.0)
    # 频率越高，声音越小
    #sound = 1-(mid-n)*(mid-n)/(120*120)
    sound = (100-n)**2/100**2
    #if n > mid:
    #    sound = -sound
    offset = index*math.pi*0.03*random.random()*0
    x = data[:size]
    x0 = x*2*math.pi*rate/fps
    y = np.sin(x0+offset)*sound
    r = (size-x)/size
    y *= r*msound
    data[:size]=y
    data[size:]=0
    return data

pass
class F4(Base):
    def init(self, fps, n=1, r = 0.75):
        self.n = n
        self.r = r
        self.fps = fps
    def call(self, rate, n, sec = 1.0, msound = 1.0):
        """
        rate: 频率
        n: 乐谱音符（1234567）
        sec: 声波发音时间，单位秒
        msound: 全局音量大小
        """
        size = int(self.fps * sec)
        data = np.arange(0,size+int(size*0.5)*0, 1.0)
        # 频率越高，声音越小
        sound = (100-n)**2/100**2
        x = data[:size]
        x0 = x*2*math.pi*rate/fps
        dec = (size-x)/size
        dec = 0.5*dec*(dec+1)
        n = 1
        y = None
        rate = 1.0
        for i in range(self.n):
            if i==self.n-1:
                val = rate
            else:
                val = rate*self.r
            yi = np.sin(x0*n)*val*dec
            if i==0:
                y = yi
            else:
                y+=yi
            n<<=1
            dec=dec*dec
            rate *= (1-self.r)
        y *= msound*sound
        data[:size]=y
        #data[size:]=0
        return data

pass
class F5(Base):
    def init(self, fps, n=1, r = 0.75):
        self.n = n
        self.r = r
        self.fps = fps
    def call(self, rate, n, sec = 1.0, msound = 1.0):
        """
        rate: 频率
        n: 乐谱音符（1234567）
        sec: 声波发音时间，单位秒
        msound: 全局音量大小
        """
        size = int(self.fps * sec)
        data = np.arange(0,size+int(size*0.5)*0, 1.0)
        # 频率越高，声音越小
        sound = (100-n)**2/100**2
        x = data[:size]
        x0 = x*2*math.pi*rate/fps
        dec = (size-x)/size
        dec = 0.5*dec*(dec+1)
        n = 1
        y = None
        rate = 1.0
        for i in range(self.n):
            if i==self.n-1:
                val = rate
            else:
                val = rate*self.r
            val = (1.0-(i+1)/self.n)**5
            yi = np.sin(x0*n)*val*dec
            if i==0:
                y = yi
            else:
                y+=yi
            n+=1
            dec=dec*dec
            rate *= (1-self.r)
        y *= msound*sound
        data[:size]=y
        #data[size:]=0
        return data

pass
f=f3
import random
class CacheFc:
    def __init__(self,f=None,sec=1.0, n=10):
        if f is None:
            f = F4(fps, 100, 0.9)
        self.f = f
        #self.cache = {}
        self.index=0
        self.n = n
        self.caches = []
        self.sec = sec
        for i in range(n):
            self.caches.append({})
    def __call__(self, rate, n):
        i = self.index
        self.index=(self.index+1)%self.n
        cache = self.caches[0]
        if rate not in cache:
            cache[rate] = self.f(rate, n, self.sec)
        return cache[rate]

pass
def create(rate=None):
    if rate is None:
        rate = fps
    return p.open(format=p.get_format_from_width(nbyte), channels=1, rate=rate, output=True)

pass

def close(stream):
    stream.stop_stream()
    stream.close()

pass
import threading

def release():
    p.terminate()

pass


class Sound:
    def sound(self, val):
        self.stream.sound(val)
    def do_record(self, val=True):
        self.stream.do_record(val)
    def records(self):
        return self.stream.out_records()
    def mode(self, val):
        self.stream.mode(val)
    def __init__(self, fc = None, stream = None, cache_st = None):
        if fc is None:
            fc = CacheFc()
        self.fc = fc
        for i in range(15,79):
            rate = fn(i)
            self.fc(rate, i)
        self.zero = create()
        if stream is None:
            stream = create()
        self.zero = stream
        if cache_st is None:
            cache_st = cache.Stream(self.zero.write, nrange,100, int(fps*0.05), ndtype, left=1)
        self.stream = cache_st
    def start(self):
        self.stream.start()
    def play(self, n):
        if not self.stream.running:
            return
        rate = fn(n)
        data = self.fc(rate, n)
        self.stream.add(data)
    def close(self):
        import time
        self.stream.stop()
        time.sleep(1.0)
        close(self.zero)
        release()

pass