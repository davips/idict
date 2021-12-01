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

import dill as d
from hashlib import md5
print(md5(d.dumps(lambda x: {"y": x+2})).hexdigest())
# output: 'f063cdd725f0e6f5a1d211925a1024b1'
print(md5(d.dumps(lambda x: {"y": x+2})).hexdigest())
# output: 'ea85fa41e85f0c78c54bbe0e00e55798'
