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
