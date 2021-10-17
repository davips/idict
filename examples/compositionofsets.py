# Composition of sets of functions
from random import Random

from idict import Ø


# A multistep process can be defined without applying its functions


def g(x, y, a=[1, 2, 3, ..., 10], b=[0.00001, 0.0001, 0.001, ..., 100000]):
    return {"z": a * x + b * y}


def h(z, c=[1, 2, 3]):
    return {"z": c * z}


# In the 'idict' framework 'data is function',
# so the alias Ø represents the 'empty data object' and the 'reflexive function' at the same time.
# In other words: 'inserting nothing' has the same effect as 'doing nothing'.
fun = Ø >> g >> h  # 'empty' or 'Ø' enable the cartesian product of the subsequent sets of functions within the expression.
print(fun)
# ...

# Before a function is applied to a dict-like, the function free parameters remain unsampled.
# The result is an ordered set of composite functions.
d = {"x": 5, "y": 7} >> (Random(0) >> fun)
print(d)
# ...

print(d.z)
# ...

d = {"x": 5, "y": 7} >> (Random(0) >> fun)
print(d.z)
# ...

# Reproducible different runs by passing a stateful random number generator.
rnd = Random(0)
e = d >> rnd >> fun
print(e.z)
# ...

e = d >> rnd >> fun
print(e.z)
# ...

# Repeating the same results.
rnd = Random(0)
e = d >> rnd >> fun
print(e.z)
# ...

e = d >> rnd >> fun
print(e.z)
# ...
