#coding=utf-8
from matplotlib import pyplot as plt
import numpy as np
import random
def show(ys):
    for y in ys:
        x = np.array(list(range(0, len(y))),dtype=np.float32)
        plt.plot(x,y)
    plt.show()

pass
x0 = np.arange(0,np.pi*10,0.01)
x1 = np.arange(0,np.pi*10,0.01)
y0 = np.sin(x0)
y1 = np.sin(x1+np.pi*0.3+np.pi*0.3*random.random())
y = y1*0.7+y0*0.5
show([y,y0,y1])


