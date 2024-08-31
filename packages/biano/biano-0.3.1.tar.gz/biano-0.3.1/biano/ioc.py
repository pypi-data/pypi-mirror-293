#coding=utf-8

from buildz.tools import *
from buildz import ioc,xf
import sys
from .tools import res, rfp
import os

def build(fp_env=None):
    mg = ioc.build()
    fps = fz.search(os.path.join(res, "ioc"), ".*\.js")
    mg.add_fps(fps)
    if fp_env is not None:
        fp_env = rfp(fp_env)
        envs = xf.loadf(fp_env)
        mg.set_envs(envs)
    return mg

pass
def run():
    fp_env = "default_env.js"
    if len(sys.argv)>1:
        fp_env = sys.argv[1]
    mg = build(fp_env)
    key = mg.get("obj.main")
    mg.get(key)

pass