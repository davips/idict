![test](https://github.com/davips/idict/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/idict/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/idict)
<a href="https://pypi.org/project/idict">
<img src="https://img.shields.io/pypi/v/idict.svg?label=release&color=blue&style=flat-square" alt="pypi">
</a>
![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue.svg)
[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<!--- [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501845.svg)](https://doi.org/10.5281/zenodo.5501845) --->
[![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028)
[![API documentation](https://img.shields.io/badge/doc-API%20%28auto%29-a0a0a0.svg)](https://davips.github.io/idict)

# idict

A lazy `dict` with universally unique deterministic identifiers.

[Latest release](https://pypi.org/project/idict) |
[Current code](https://github.com/davips/idict) |
[API documentation](https://davips.github.io/idict)

### See also

* identification package used by `idict`: [GaROUPa](https://pypi.org/project/garoupa)
* only laziness, i.e., without the identification part: [ldict](https://pypi.org/project/ldict)

## Overview

An `idict` is an identified `dict` with `str` keys.
We consider that every value is generated by a process, starting from an `empty` `idict`. The process is a sequence of
transformation steps done through the operator `>>`, which symbolizes the ordering of the steps.
There are two types of steps:

* **value insertion** - represented by dict-like objects
* **function application** - represented by ordinary Python functions

Functions, `idict`s, and values have a deterministic UUID
(called _hosh_ - **o**perable **h**a**sh**). 
Identifiers (hoshes) for `idict`s and values are predictable through the
magic available [here](https://pypi.org/project/garoupa).
An `idict` is completely defined by its key-value pairs so that
it can be converted from/to a built-in `dict`.

Creating an `idict` is not different from creating an ordinary `dict`. Optionally it can be created through the `>>` operator
used after `empty` or `Ø` (usually AltGr+Shift+o in most keyboards).
The resulting `idict` always contains two extra entries `id` and `ids`:
![img.png](https://raw.githubusercontent.com/davips/idict/main/examples/img.png)

Function application is done in the same way. The parameter names define the input fields, while the keys in the
returned `dict` define the output fields:
![img_1.png](https://raw.githubusercontent.com/davips/idict/main/examples/img_1.png)

After evaluated, the value will not be calculated again:
![img_2.png](https://raw.githubusercontent.com/davips/idict/main/examples/img_2.png)

Functions can accept parameters:
![img_3.png](https://raw.githubusercontent.com/davips/idict/main/examples/img_3.png)


## Installation
### ...as a standalone lib
```bash
# Set up a virtualenv. 
python3 -m venv venv
source venv/bin/activate

# Install from PyPI...
pip install --upgrade pip
pip install -U idict
pip install -U idict[full]  # use the flag 'full' for extra functionality (recommended)

# ...or, install from updated source code.
pip install git+https://github.com/davips/idict
```

### ...from source
```bash
git clone https://github.com/davips/idict
cd idict
poetry install
poetry install -E full  # use the flag 'full' for extra functionality (recommended)
```

## Examples

**Overview**
<details>
<p>

```python3

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
"""
{
    "x": 5,
    "y": 7,
    "z": 10,
    "_id": "SV_4fc23c71a6bb954f6f2ed40e440cfd2b76087",
    "_ids": "GS_cb0fda15eac732cb08351e71fc359058b93bd... +1 ...gk_64fdf435fc9aa10be990397ff8fa92888792c"
}
"""
```

```python3


# Inverting color theme for a white background.
from garoupa import setup

setup(dark_theme=False)
d = idict(x=5, y=7, z=10)
print(d)


"""
{
    "x": 5,
    "y": 7,
    "z": 10,
    "_id": "SV_4fc23c71a6bb954f6f2ed40e440cfd2b76087",
    "_ids": "GS_cb0fda15eac732cb08351e71fc359058b93bd... +1 ...gk_64fdf435fc9aa10be990397ff8fa92888792c"
}
"""
```

```python3


# Function application.
# The input and output fields are detected from the function signature and returned dict.
def f(x):
    return {"y": x ** 2}


d2 = d >> f
print(d2)
"""
{
    "y": "→(x)",
    "x": 5,
    "z": 10,
    "_id": "J.WMNtqzVe2LiO8Ez4Wkgpa6zsBS.o529OTeWhNo",
    "_ids": "j6dsrYpQ-9A6BFtY5T98d-UeFJOS.o529OTeWhNo... +1 ...gk_64fdf435fc9aa10be990397ff8fa92888792c"
}
"""
```

```python3


# Anonymous function application.
d2 = d >> (lambda y: {"y": y / 5})
print(d)
"""
{
    "x": 5,
    "y": 7,
    "z": 10,
    "_id": "SV_4fc23c71a6bb954f6f2ed40e440cfd2b76087",
    "_ids": "GS_cb0fda15eac732cb08351e71fc359058b93bd... +1 ...gk_64fdf435fc9aa10be990397ff8fa92888792c"
}
"""
```

```python3


# Resulting values are evaluated lazily.
d >>= lambda y: {"y": y / 5}
print(d.y)
"""
1.4
"""
```

```python3


print(d)
"""
{
    "y": 1.4,
    "x": 5,
    "z": 10,
    "_id": "7uAa.i.4XbFyFY7OLx2TfzMQOeYZim1XGTCOzwYg",
    "_ids": "S-Vd.8e3nPaYsNmqhkiGDdvZUvVZim1XGTCOzwYg... +1 ...gk_64fdf435fc9aa10be990397ff8fa92888792c"
}
"""
```

```python3


# Parameterized function application.
# "Parameters" are distinguished from "fields" by having default values.
# When the default value is None, it means it will be explicitly defined later by 'let'.
from idict import let


def f(x, y, a=None, b=None):
    return {"z": a * x ** b, "w": y ** b}


d2 = d >> let(f, a=7, b=2)
print(d2)
"""
{
    "z": "→(a b x y)",
    "w": "→(a b x y)",
    "y": 1.4,
    "x": 5,
    "_id": "cLQzLVSJU.N2iT-5OaZWUEnnYWUHK5qjURoS6ymD",
    "_ids": "u-FenHI5ID.J6D-Hvj.WShqswXAgoL5sYPWsHSoF... +2 ...GS_cb0fda15eac732cb08351e71fc359058b93bd"
}
"""
```

```python3


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
"""
{
    "z": "→(a b ap gp x y)",
    "w": "→(a b ap gp x y)",
    "y": 1.4,
    "x": 5,
    "_id": "JNtKgf-Bz7S5z6QwqzWKKM5OLM4QR7OmcORBo47s",
    "_ids": "IYglBIPS5j1KqhPE.JPs6GD89DSHtNtvgQncZo9u... +2 ...GS_cb0fda15eac732cb08351e71fc359058b93bd"
}
"""
```

```python3

print(d2.z)
"""
175
"""
```

```python3

print(d2)
"""
{
    "z": 175,
    "w": "10.541350399999995",
    "y": 1.4,
    "x": 5,
    "_id": "JNtKgf-Bz7S5z6QwqzWKKM5OLM4QR7OmcORBo47s",
    "_ids": "IYglBIPS5j1KqhPE.JPs6GD89DSHtNtvgQncZo9u... +2 ...GS_cb0fda15eac732cb08351e71fc359058b93bd"
}
"""
```


</p>
</details>

**Identity example**
<details>
<p>

```python3
from idict import idict

a = idict(x=3)
print(a)
"""
{
    "x": 3,
    "_id": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9",
    "_ids": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9"
}
"""
```

```python3

b = idict(y=5)
print(b)
"""
{
    "y": 5,
    "_id": "EI_20378979f4669f2e318ae9742e214fd4880d7",
    "_ids": "EI_20378979f4669f2e318ae9742e214fd4880d7"
}
"""
```

```python3

print(a >> b)
"""
{
    "x": 3,
    "y": 5,
    "_id": "pl_bb7e60e68670707cdef7dfd31096db4c63c91",
    "_ids": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9 EI_20378979f4669f2e318ae9742e214fd4880d7"
}
"""
```


</p>
</details>

**Merging two idicts**
<details>
<p>

```python3
from idict import idict

a = idict(x=3)
print(a)
"""
{
    "x": 3,
    "_id": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9",
    "_ids": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9"
}
"""
```

```python3

b = idict(y=5)
print(b)
"""
{
    "y": 5,
    "_id": "EI_20378979f4669f2e318ae9742e214fd4880d7",
    "_ids": "EI_20378979f4669f2e318ae9742e214fd4880d7"
}
"""
```

```python3

print(a >> b)
"""
{
    "x": 3,
    "y": 5,
    "_id": "pl_bb7e60e68670707cdef7dfd31096db4c63c91",
    "_ids": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9 EI_20378979f4669f2e318ae9742e214fd4880d7"
}
"""
```


</p>
</details>

**Lazily applying functions to idict**
<details>
<p>

```python3
from idict import idict

a = idict(x=3)
print(a)
"""
{
    "x": 3,
    "_id": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9",
    "_ids": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9"
}
"""
```

```python3

a = a >> idict(y=5) >> {"z": 7} >> (lambda x, y, z: {"r": x ** y // z})
print(a)
"""
{
    "r": "→(x y z)",
    "x": 3,
    "y": 5,
    "z": 7,
    "_id": "kgdz8xfS7IuGtukIPe37KhAUrB2P4S3OFdPs8Gab",
    "_ids": "CXqa2zRRNd7Aj5wI8JTJ0O-7ML0P4S3OFdPs8Gab... +2 ...ZN_eccacd999c26ce18c98f9a17a6f47adcf162a"
}
"""
```

```python3

print(a.r)
"""
34
"""
```

```python3

print(a)
"""
{
    "r": 34,
    "x": 3,
    "y": 5,
    "z": 7,
    "_id": "kgdz8xfS7IuGtukIPe37KhAUrB2P4S3OFdPs8Gab",
    "_ids": "CXqa2zRRNd7Aj5wI8JTJ0O-7ML0P4S3OFdPs8Gab... +2 ...ZN_eccacd999c26ce18c98f9a17a6f47adcf162a"
}
"""
```


</p>
</details>

**Parameterized functions and sampling**
<details>
<p>

```python3
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
"""
{
    "_id": "0000000000000000000000000000000000000000",
    "_ids": {}
}
"""
```

```python3

# Putting some values. Alternatively: d = idict(x=5, y=7).
d["x"] = 5
d["y"] = 7
print(d)
"""
{
    "x": 5,
    "y": 7,
    "_id": "BB_fad4374ca911f344859dab8e4b016ba2fe65b",
    "_ids": "GS_cb0fda15eac732cb08351e71fc359058b93bd WK_6ba95267cec724067d58b3186ecbcaa4253ad"
}
"""
```

```python3

# Parameter values are uniformly sampled.
d1 = d >> simplefun
print(d1)
print(d1.z)
"""
{
    "z": "→(x y)",
    "x": 5,
    "y": 7,
    "_id": "VqfQeuBWL7Xv1FwWe6pzgqJwclRMPNZuFtrAIt6g",
    "_ids": "9KKem6QL-I8C0Yk0q3URBt-aNXHMPNZuFtrAIt6g... +1 ...WK_6ba95267cec724067d58b3186ecbcaa4253ad"
}
35
"""
```

```python3

d2 = d >> simplefun
print(d2)
print(d2.z)
"""
{
    "z": "→(x y)",
    "x": 5,
    "y": 7,
    "_id": "VqfQeuBWL7Xv1FwWe6pzgqJwclRMPNZuFtrAIt6g",
    "_ids": "9KKem6QL-I8C0Yk0q3URBt-aNXHMPNZuFtrAIt6g... +1 ...WK_6ba95267cec724067d58b3186ecbcaa4253ad"
}
35
"""
```

```python3

# Parameter values can also be manually set.
e = d >> let(fun, a=5, b=10)
print(e.z)
"""
95
"""
```

```python3

# Not all parameters need to be set.
e = d >> Random() >> let(fun, a=5)
print("e =", e.z)
"""
e = 7025.0
"""
```

```python3

# Each run will be a different sample for the missing parameters.
e = e >> Random() >> let(fun, a=5)
print("e =", e.z)
"""
e = 7025.0
"""
```

```python3

# We can define the initial state of the random sampler.
# It will be in effect from its location place onwards in the expression.
e = d >> Random(0) >> let(fun, a=5)
print(e.z)
"""
725.0
"""
```

```python3

# All runs will yield the same result,
# if starting from the same random number generator seed.
e = e >> Random(0) >> let(fun, a=[555, 777])
print("Let 'a' be a list:", e.z)
"""
Let 'a' be a list: 700003885.0
"""
```

```python3

# Reproducible different runs are achievable by using a single random number generator.
e = e >> Random(0) >> let(fun, a=[5, 25, 125, ..., 10000])
print("Let 'a' be a geometric progression:", e.z)
"""
Let 'a' be a geometric progression: 700003125.0
"""
```

```python3
rnd = Random(0)
e = d >> rnd >> let(fun, a=5)
print(e.z)
e = d >> rnd >> let(fun, a=5)  # Alternative syntax.
print(e.z)
"""
725.0
700000025.0
"""
```

```python3

# Output fields can be defined dynamically through parameter values.
# Input fields can be defined dynamically through kwargs.
copy = lambda source=None, target=None, **kwargs: {target: kwargs[source]}
d = empty >> {"x": 5}
d >>= let(copy, source="x", target="y")
print(d)
d.evaluate()
print(d)

"""
{
    "y": "→(source target x)",
    "x": 5,
    "_id": "xmcjrFNT-2nEr3vizzx-44QwV5kwDfaOqWWvzOrq",
    "_ids": "3Tv6p5fZ936EK1DUkkcYAgWPbrmwDfaOqWWvzOrq GS_cb0fda15eac732cb08351e71fc359058b93bd"
}
{
    "y": 5,
    "x": 5,
    "_id": "xmcjrFNT-2nEr3vizzx-44QwV5kwDfaOqWWvzOrq",
    "_ids": "3Tv6p5fZ936EK1DUkkcYAgWPbrmwDfaOqWWvzOrq GS_cb0fda15eac732cb08351e71fc359058b93bd"
}
"""
```


</p>
</details>

**Composition of sets of functions**
<details>
<p>

```python3
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
"""
«λ{} × λ»
"""
```

```python3

# Before a function is applied to a dict-like, the function free parameters remain unsampled.
# The result is an ordered set of composite functions.
d = {"x": 5, "y": 7} >> (Random(0) >> fun)
print(d)
"""
{
    "z": "→(c z→(a b x y))",
    "x": 5,
    "y": 7,
    "_id": "YZWooP03q0mFec8tjNwy3YuAohamevfjG3VAFXL-",
    "_ids": "5PKBLX4-dGDGHUifvK.QYVLeZTgmevfjG3VAFXL-... +1 ...WK_6ba95267cec724067d58b3186ecbcaa4253ad"
}
"""
```

```python3

print(d.z)
"""
105.0
"""
```

```python3

d = {"x": 5, "y": 7} >> (Random(0) >> fun)
print(d.z)
"""
105.0
"""
```

```python3

# Reproducible different runs by passing a stateful random number generator.
rnd = Random(0)
e = d >> rnd >> fun
print(e.z)
"""
105.0
"""
```

```python3

e = d >> rnd >> fun
print(e.z)
"""
14050.0
"""
```

```python3

# Repeating the same results.
rnd = Random(0)
e = d >> rnd >> fun
print(e.z)
"""
105.0
"""
```

```python3

e = d >> rnd >> fun
print(e.z)
"""
14050.0
"""
```


</p>
</details>

<persistence>

## Concept

An `idict` is like a common Python `dict`, with extra functionality and lazy. 
It is a mapping between string keys, called
fields, and any serializable (pickable) object.
Each `idict` has two extra entries: `id` (identifier) and `ids` (value identifiers).

A custom 40-digit unique identifier (see [GaROUPa](https://pypi.org/project/garoupa))
can be provided as an attribute for each function.
Value objects can have custom identifiers as well, if provided whithin the entry `ids`. 

Otherwise, identifiers for functions and values will be calculated through blake3 hashing of their content.
For functions, the bytecode is used as content. 
For this reason, such functions should be simple, with minimal external dependencies or
with their import statements inside the function body.
This decreases the odds of using two functions with identical local code (and, therefore, identical identifiers) 
performing different calculations.

## Grants

This work was supported by Fapesp under supervision of
Prof. André C. P. L. F. de Carvalho at CEPID-CeMEAI (Grants 2013/07375-0 – 2019/01735-0)
until 2021-03-31.
