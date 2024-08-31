#coding=utf-8
from matplotlib import pyplot as plt
import numpy as np
import random

def smooth(datas, ws):
    if ws is None:
        return datas
    ys = [ws[i]*datas[i:datas.size-ws.size+1+i] for i in range(ws.size)]
    rst = ys[0]
    for _y in ys[1:]:
        rst+=_y
    return rst

pass
def show(ys):
    for y in ys:
        x = np.array(list(range(0, len(y))),dtype=np.float32)
        plt.plot(x,y)
    plt.show()

pass
mx = np.pi*10
x0 = np.arange(0,np.pi*10,0.001)
x1 = np.arange(0,np.pi*10,0.001)
y0 = np.sin(x0)
y1 = np.sin(x1+np.pi*0.3+np.pi*0.3*random.random())
y0 *= (mx-x0)/mx
y1*=(mx-x1)/mx
print(x0.size)
zeros = np.zeros(1000)
y1 = np.hstack([zeros,zeros,y1,zeros])
y0 = np.hstack([zeros,y0, zeros,zeros])
y = y1*0.7+y0*0.5
y=y1+y0
print(y.size)
ws = [1.0]*500
ws = np.array(ws)/sum(ws)
#y=smooth(y, ws)
print(y.size)
#show([y,y0])#,y1,y0])
r = x0/mx
r=1-r
r=r**20
#show([r])

r = 0.9
n = 10
rate = 1.0
rst = []
for i in range(n):
    if i==n-1:
        val = rate
    else:
        val = rate*r
    rst.append(val)
    rate *= (1-r)

pass
rst = np.array(rst)
show([rst])


