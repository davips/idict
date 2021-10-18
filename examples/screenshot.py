# Overview

# Creation by direct instantiation.
from idict import idict

d = idict(x=5, y=7, z=10)

# Creation from scratch.
# The expression 'v >> a >> b' means "Value 'v' will be processed by step 'a' then 'b'".
# A step can be a value insertion or a function application.
from idict import empty

d = empty >> {"x": 5} >> {"y": 7, "z": 10}

# Empty alias ('Ø') usage.
from idict import Ø

d = Ø >> {"x": 5} >> {"y": 7, "z": 10}
print(d)
# ...


# Inverting color theme for a white background.
from garoupa import setup

setup(dark_theme=False)
d = idict(x=5, y=7, z=10)
print(d)


# ...


# Function application.
# The input and output fields are detected from the function signature and returned dict.
def f(x):
    return {"y": x ** 2}


d2 = d >> f
print(d2)
# ...


# Anonymous function application.
d2 = d >> (lambda y: {"y": y / 5})
print(d)
# ...


# Resulting values are evaluated lazily.
d >>= lambda y: {"y": y / 5}
print(d.y)
# ...


print(d)
# ...


# Parameterized function application.
# "Parameters" are distinguished from "fields" by having default values.
# When the default value is None, it means it will be explicitly defined later by 'let'.
from idict import let


def f(x, y, a=None, b=None):
    return {"z": a * x ** b, "w": y ** b}


d2 = d >> let(f, a=7, b=2)
print(d2)
# ...


# Parameterized function application with sampling.
# The default value is one of the following ranges, 
#     list, arithmetic progression, geometric progression.
# Each parameter value will be sampled later.
# A random number generator must be given.
from idict import let
from random import Random


def f(x, y, a=None, b=[1, 2, 3], ap=[1, 2, 3, ..., 10], gp=[1, 2, 4, ..., 16]):
    return {"z": a * x ** b, "w": y ** ap * gp}


d2 = d >> Random(0) >> let(f, a=7)
print(d2)
# ...

print(d2.z)
# ...

print(d2)
# ...
