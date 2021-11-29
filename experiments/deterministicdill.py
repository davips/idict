import pickletools as pt
from hashlib import md5
from io import StringIO

import dill as d


def h(f):
    s = StringIO()
    pt.dis(d.dumps(f, protocol=5), out=s)
    by = ((s.getvalue())) #.encode()
    print(by)
    # m = md5(by).hexdigest()
    # s.close()
    return 0

asd= "passlib"
print(h(lambda x: {"sy": x + 2}))
print(h(lambda x: {"sy": x + 21}))
print(h(lambda x: {"y": x + 2}))
print(h(lambda x: {"y": x + 2}))
#  muda apenas o número da linha, por isso não é determinístico
