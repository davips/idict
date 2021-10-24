#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
from functools import cached_property
from operator import rshift as aop
from operator import xor as cop
from random import Random
from typing import Union, Callable

from ldict.core.base import AbstractLazyDict
from ldict.parameter.abslet import AbstractLet
from ldict.parameter.functionspace import FunctionSpace


class iLet(AbstractLet):
    """
    Set values or sampling intervals for parameterized functions

    >>> from idict import idict, let
    >>> f = lambda x,y, a=[-1,-0.9,-0.8,...,1]: {"z": a*x + y}
    >>> f_a = let(f, a=0)
    >>> f_a
    λ{'a': 0}
    >>> d = idict(x=5,y=7)
     >>> d2 = d >> f_a
    >>> print(d2)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "id": "EeRXDcBiRneJFZEhOmpvOhPbUz-LzcpgoIkKP10B",
        "ids": {
            "z": "YdFXcXZvVdSoGcj06JWP8VlXnK1MzcpgoIkKP10B",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> d2.evaluate()
    >>> print(d2)
    {
        "z": 7,
        "x": 5,
        "y": 7,
        "id": "EeRXDcBiRneJFZEhOmpvOhPbUz-LzcpgoIkKP10B",
        "ids": {
            "z": "YdFXcXZvVdSoGcj06JWP8VlXnK1MzcpgoIkKP10B",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> from random import Random
    >>> d2 = d >> Random(0) >> let(f, a=[8,9])
    >>> print(d2)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "id": "qpPpHLgdd.4gDiRaaVAxvrVZGC.jEKWXeSzgXRsN",
        "ids": {
            "z": "adrKf2tXiNmHzyvVtf6SR2sJaN2kEKWXeSzgXRsN",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> d2.evaluate()
    >>> print(d2)
    {
        "z": 52,
        "x": 5,
        "y": 7,
        "id": "qpPpHLgdd.4gDiRaaVAxvrVZGC.jEKWXeSzgXRsN",
        "ids": {
            "z": "adrKf2tXiNmHzyvVtf6SR2sJaN2kEKWXeSzgXRsN",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> let(f, a=5) >> {"x": 5, "y": 7}
    «λ{'a': 5} × {'x': 5, 'y': 7}»
    >>> print(idict({"x": 5, "y": 7}) >> let(f, a=5))
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "id": "EZ0UWP-muXoeuN-1BPnRtJdGwOSYWVP8n81Tsn4K",
        "ids": {
            "z": "V5mOMy3Zrrywy-EMU9V9QkMp0ZVYWVP8n81Tsn4K",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> let(f, a=5) >> idict({"x": 5, "y": 7})
    «λ{'a': 5} × {
        "x": 5,
        "y": 7,
        "id": "mP_2d615fd34f97ac906e162c6fc6aedadc4d140",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }»
    >>> let(f, a=5) >> ["mycache"]
    «λ{'a': 5} × ^»
    >>> from idict.parameter.ifunctionspace import iFunctionSpace
    >>> let(f, a=5) >> iFunctionSpace()
    «λ{'a': 5}»
    >>> iFunctionSpace() >> let(f, a=5)
    «λ{'a': 5}»
    >>> (lambda x: {"z": x*8}) >> let(f, a=5)
    «λ × λ{'a': 5}»
    >>> d = {"x":3, "y": 8} >> let(f, a=5)
    >>> print(d)
    {
        "z": "→(a x y)",
        "x": 3,
        "y": 8,
        "id": "6o0JC4icwTJXeYH2CFgBvfV1fONYWVP8n81Tsn4K",
        "ids": {
            "z": "ArvV6lQlezPBNMRMNlVwPSvqONNYWVP8n81Tsn4K",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
            "y": "6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde"
        }
    }
    >>> print(d.z)
    23
    >>> d >>= Random(0) >> let(f, a=[1,2,3]) >> let(f, a=[9,8,7])
    >>> print(d)
    {
        "z": "→(a x y)",
        "x": 3,
        "y": 8,
        "id": "um3mdZK7S78uxdCOrbyGh2VQsKXXZ8.hgd0IScLe",
        "ids": {
            "z": "aj-1mwXeaJv3r3MwDTaCBFvd0KXXZ8.hgd0IScLe",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
            "y": "6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde"
        }
    }
    >>> print(d.z)
    32
    """

    def __init__(self, f, **kwargs):
        self.f = f
        self.config = {k: kwargs[k] for k in sorted(kwargs.keys())}

    @cached_property
    def asdict(self):
        return self.config

    def __repr__(self):
        return "λ" + str(self.config)

    def __rrshift__(self, left: Union[dict, list, Random, Callable, 'iLet']):
        if isinstance(left, dict) and not isinstance(left, AbstractLazyDict):
            from idict.core.idict_ import Idict
            return Idict(left) >> self
        if isinstance(left, (list, Random, Callable)):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(left, aop, self)
        return NotImplemented

    def __rshift__(self, other: Union[dict, list, Random, Callable, 'iLet', AbstractLazyDict]):
        if isinstance(other, (dict, list, Random, Callable, iLet)):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(self, aop, other)
        return NotImplemented

    def __rxor__(self, left: Union[dict, list, Random, Callable, 'iLet']):
        if isinstance(left, (dict, list, Random, Callable)) and not isinstance(left, AbstractLazyDict):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(left, cop, self)
        return NotImplemented

    def __xor__(self, other: Union[dict, list, Random, Callable, 'iLet', AbstractLazyDict]):
        if isinstance(other, (dict, list, Random, Callable, iLet)):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(self, cop, other)
        return NotImplemented
