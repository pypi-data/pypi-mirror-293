#coding=utf-8

from . import ioc
import sys
from buildz import pyz
def test():
    mg = ioc.build("default_env.js")
    if len(sys.argv)>1:
        fp = sys.argv[1]
        mg.set_env("file.records", fp)
    mg.get("replay")

pass

pyz.bylocals(locals(), test)