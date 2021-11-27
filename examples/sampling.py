# Parameterized functions and sampling
from random import Random

from idict import Ø, let


# A function provide input fields and, optionally, parameters.
# For instance:
# 'a' is sampled from an arithmetic progression
# 'b' is sampled from a geometric progression
# Here, the syntax for default parameter values is borrowed with a new meaning.
def fun(x, y, a=[-100, -99, -98, ..., 100], b=[0.0001, 0.001, 0.01, ..., 100000000]):
    return {"z": a * x + b * y}


def simplefun(x, y):
    return {"z": x * y}


# Creating an empty idict. Alternatively: d = idict().
d = Ø >> {}
d.show(colored=False)
# ...

# Putting some values. Alternatively: d = idict(x=5, y=7).
d["x"] = 5
d["y"] = 7
print(d)
# ...

# Parameter values are uniformly sampled.
d1 = d >> simplefun
print(d1)
print(d1.z)
# ...

d2 = d >> simplefun
print(d2)
print(d2.z)
# ...

# Parameter values can also be manually set.
e = d >> let(fun, a=5, b=10)
print(e.z)
# ...

# Not all parameters need to be set.
e = d >> Random() >> let(fun, a=5)
print("e =", e.z)
# ...

# Each run will be a different sample for the missing parameters.
e = e >> Random() >> let(fun, a=5)
print("e =", e.z)
# ...

# We can define the initial state of the random sampler.
# It will be in effect from its location place onwards in the expression.
e = d >> Random(0) >> let(fun, a=5)
print(e.z)
# ...

# All runs will yield the same result,
# if starting from the same random number generator seed.
e = e >> Random(0) >> let(fun, a=[555, 777])
print("Let 'a' be a list:", e.z)
# ...

# Reproducible different runs are achievable by using a single random number generator.
e = e >> Random(0) >> let(fun, a=[5, 25, 125, ..., 10000])
print("Let 'a' be a geometric progression:", e.z)
# ...
rnd = Random(0)
e = d >> rnd >> let(fun, a=5)
print(e.z)
e = d >> rnd >> let(fun, a=5)  # Alternative syntax.
print(e.z)
# ...

# Output fields can be defined dynamically through parameter values.
# Input fields can be defined dynamically through kwargs.
copy = lambda source=None, target=None, **kwargs: {target: kwargs[source]}
d = empty >> {"x": 5}
d >>= let(copy, source="x", target="y")
print(d)
d.evaluate()
print(d)
