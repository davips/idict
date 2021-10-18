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

* laziness+identity ([ldict](https://pypi.org/project/ldict))
* laziness+identity+persistence ([cdict](https://pypi.org/project/cdict))

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

# ...or, install from updated source code.
pip install git+https://github.com/davips/idict
```

### ...from source
```bash
git clone https://github.com/davips/idict
cd idict
poetry install
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
    "id": "H8_d2866809b46b74333b8a1e77c2897466edc1b",
    "ids": {
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
        "z": "ll_4dd7bf5575f1c410dc6458230cda99c380bda"
    }
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
    "id": "H8_d2866809b46b74333b8a1e77c2897466edc1b",
    "ids": {
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
        "z": "ll_4dd7bf5575f1c410dc6458230cda99c380bda"
    }
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
    "id": "d6tEK5U0qq3sv0aCdSADNL3DiohLRgUAfdP7HEp4",
    "ids": {
        "y": "S8kpf19fdmWw65QIdKajRI2i03eLRgUAfdP7HEp4",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "z": "ll_4dd7bf5575f1c410dc6458230cda99c380bda"
    }
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
    "id": "H8_d2866809b46b74333b8a1e77c2897466edc1b",
    "ids": {
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
        "z": "ll_4dd7bf5575f1c410dc6458230cda99c380bda"
    }
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
    "id": "OfV9fKxwEnz.wbUBTPj8HiLDPnT04cq1Fa6MPeo7",
    "ids": {
        "y": "LZHU.q4GvU4Y3YhITHVPLfKix2Q04cq1Fa6MPeo7",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "z": "ll_4dd7bf5575f1c410dc6458230cda99c380bda"
    }
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
    "id": "0NVUmzD6.hrqvbHxGYHCrI8ZGKBXCQn7RgvPiD1z",
    "ids": {
        "z": "wlfii3B.l6NcROr6syPY3h-YOeRWyEZ5c6p3voFs",
        "w": "ofEb.nRSYsUsgAnnyp4KYFovZaUOV6000sv....-",
        "y": "LZHU.q4GvU4Y3YhITHVPLfKix2Q04cq1Fa6MPeo7",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
    }
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
    "id": "sKzmHJm6wbwwLKYCewWyeMBQ8dAItpDRQXLcK1wt",
    "ids": {
        "z": "6hnZUsoJDO0UABeIu.OOWVu6p7vHpddQbNFsWO7n",
        "w": "ofEb.nRSYsUsgAnnyp4KYFovZaUOV6000sv....-",
        "y": "LZHU.q4GvU4Y3YhITHVPLfKix2Q04cq1Fa6MPeo7",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
    }
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
    "id": "sKzmHJm6wbwwLKYCewWyeMBQ8dAItpDRQXLcK1wt",
    "ids": {
        "z": "6hnZUsoJDO0UABeIu.OOWVu6p7vHpddQbNFsWO7n",
        "w": "ofEb.nRSYsUsgAnnyp4KYFovZaUOV6000sv....-",
        "y": "LZHU.q4GvU4Y3YhITHVPLfKix2Q04cq1Fa6MPeo7",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
    }
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
    "id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
    "ids": {
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
    }
}
"""
```

```python3

b = idict(y=5)
print(b)
"""
{
    "y": 5,
    "id": "0U_e2a86ff72e226d5365aea336044f7b4270977",
    "ids": {
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
    }
}
"""
```

```python3

print(a >> b)
"""
{
    "x": 3,
    "y": 5,
    "id": "Xt_a63010fa2b5b4c671270fbe8ec313568a8b35",
    "ids": {
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
    }
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
    "id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
    "ids": {
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
    }
}
"""
```

```python3

b = idict(y=5)
print(b)
"""
{
    "y": 5,
    "id": "0U_e2a86ff72e226d5365aea336044f7b4270977",
    "ids": {
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
    }
}
"""
```

```python3

print(a >> b)
"""
{
    "x": 3,
    "y": 5,
    "id": "Xt_a63010fa2b5b4c671270fbe8ec313568a8b35",
    "ids": {
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
    }
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
    "id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
    "ids": {
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
    }
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
    "id": "H8DftZZ4nH6d67WSvYYxh-KsdBqp9MQBdvkLxU2o",
    "ids": {
        "r": "n57RGOgdv03kK4IqBkIf6oFrvgAp9MQBdvkLxU2o",
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977",
        "z": "nX_da0e3a184cdeb1caf8778e34d26f5fd4cc8c8"
    }
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
    "id": "H8DftZZ4nH6d67WSvYYxh-KsdBqp9MQBdvkLxU2o",
    "ids": {
        "r": "n57RGOgdv03kK4IqBkIf6oFrvgAp9MQBdvkLxU2o",
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977",
        "z": "nX_da0e3a184cdeb1caf8778e34d26f5fd4cc8c8"
    }
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


# Creating an empty ldict. Alternatively: d = ldict().
d = Ø >> {}
d.show(colored=False)
"""
{
    "id": "0000000000000000000000000000000000000000",
    "ids": {}
}
"""
```

```python3

# Putting some values. Alternatively: d = ldict(x=5, y=7).
d["x"] = 5
d["y"] = 7
d.show(colored=False)
"""
{
    "x": 5,
    "y": 7,
    "id": "mP_2d615fd34f97ac906e162c6fc6aedadc4d140",
    "ids": {
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
    }
}
"""
```

```python3

# Parameter values are uniformly sampled.
d1 = d >> simplefun
d1.show(colored=False)
print(d1.z)
"""
{
    "z": "→(x y)",
    "x": 5,
    "y": 7,
    "id": "ZAasLu0lIEqhJyS1s8ML8WGeTnradBnjS7VNt6Mg",
    "ids": {
        "z": "iE6rHiYYwfwOBqa4Luh4XCd-myeadBnjS7VNt6Mg",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
    }
}
35
"""
```

```python3

d2 = d >> simplefun
d2.show(colored=False)
print(d2.z)
"""
{
    "z": "→(x y)",
    "x": 5,
    "y": 7,
    "id": "ZAasLu0lIEqhJyS1s8ML8WGeTnradBnjS7VNt6Mg",
    "ids": {
        "z": "iE6rHiYYwfwOBqa4Luh4XCd-myeadBnjS7VNt6Mg",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
    }
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
e = d >> let(simplefun, a=5)
print(e.z)
"""
35
"""
```

```python3

# Each run will be a different sample for the missing parameters.
e = e >> let(simplefun, a=5)
print(e.z)
"""
35
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
«<function g at 0x7f193a229dc0> × <function h at 0x7f193a237af0>»
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
    "id": "fxUC9sbaX2rNuWEutGTJHWKMV5Af0h9G8FLRPWeq",
    "ids": {
        "z": "o5r8PbsxYejqtbjdN0p22yhwpgDf0h9G8FLRPWeq",
        "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
    }
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

<!--- ## Persistence
Extra dependencies can be installed to support saving data to disk or to a server in the network. 

**[still an ongoing work...]**

`poetry install -E full`
--->

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
