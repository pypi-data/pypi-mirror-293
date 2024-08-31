#
import os
res = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")

def rfp(fp):
    if fp is None:
        return None
    bak = fp
    if not os.path.isfile(fp):
        fp = os.path.join(res, fp)
    if not os.path.isfile(fp):
        raise Exception(f"not such file: {bak}")
    return fp

pass