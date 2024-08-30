#
import sys
from buildz import pyz
pyz.add(__file__)
from biano import confkeys as keys
def run():
    keys.run()
if __name__=="__main__":
    run()

pass
"""
import rtest
sound=rtest.keys.sound
sd = rtest.keys.sound.sd
sd.do_record()
rtest.run()

rst = sd.records()
y=rst
from matplotlib import pyplot as plt
import numpy as np
def show(y):
    x = np.array(list(range(0, len(y))),dtype=np.float32)
    x = x*(1/sound.fps)
    plt.plot(x,y)
    plt.show()

pass
show(y[::10000])

"""