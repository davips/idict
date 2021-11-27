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
from json import dumps
from operator import rshift as aop
from operator import xor as cop
from random import Random
from typing import Union, Callable

from ldict.core.base import AbstractLazyDict
from ldict.customjson import CustomJSONEncoder
from ldict.parameter.abslet import AbstractLet


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
    >>> d2.show(colored=False)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "_id": "uonOfBfiCPJ6QL7yu19SF9BX6OaIf7PP0vTUHwdO",
        "_ids": {
            "z": "aTcq8LzhLxCZM1OgOnGa0N7HCYdIf7PP0vTUHwdO",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8 (content: QY_49dee83e556d2448f877a44fd26f5f2fac8c8)"
        }
    }
    >>> d2.evaluate()
    >>> d2.show(colored=False)
    {
        "z": 7,
        "x": 5,
        "y": 7,
        "_id": "uonOfBfiCPJ6QL7yu19SF9BX6OaIf7PP0vTUHwdO",
        "_ids": {
            "z": "aTcq8LzhLxCZM1OgOnGa0N7HCYdIf7PP0vTUHwdO",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8 (content: QY_49dee83e556d2448f877a44fd26f5f2fac8c8)"
        }
    }
    >>> from random import Random
    >>> d2 = d >> Random(0) >> let(f, a=[8,9])
    >>> d2.show(colored=False)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "_id": "0xMtdBRZKHKRN6wjmeVZv2te5.hMrJxAMFjv1ppr",
        "_ids": {
            "z": "fH3vqqaQB3J34ma2GAqiSF.ZA9lMrJxAMFjv1ppr",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8 (content: QY_49dee83e556d2448f877a44fd26f5f2fac8c8)"
        }
    }
    >>> d2.evaluate()
    >>> d2.show(colored=False)
    {
        "z": 52,
        "x": 5,
        "y": 7,
        "_id": "0xMtdBRZKHKRN6wjmeVZv2te5.hMrJxAMFjv1ppr",
        "_ids": {
            "z": "fH3vqqaQB3J34ma2GAqiSF.ZA9lMrJxAMFjv1ppr",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8 (content: QY_49dee83e556d2448f877a44fd26f5f2fac8c8)"
        }
    }
    >>> let(f, a=5) >> {"x": 5, "y": 7}
    «λ{'a': 5} × {'x': 5, 'y': 7}»
    >>> (idict({"x": 5, "y": 7}) >> let(f, a=5)).show(colored=False)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "_id": "Q9TVKR-HVcye7.bIdDpsozCRZxSCMKqODpuKHpoM",
        "_ids": {
            "z": "butCwKlacHFJITvKwZWMag9BtIFCMKqODpuKHpoM",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8 (content: QY_49dee83e556d2448f877a44fd26f5f2fac8c8)"
        }
    }
    >>> from idict.core.appearance import decolorize
    >>> print(decolorize(str(let(f, a=5) >> idict({"x": 5, "y": 7}))))
    «λ{'a': 5} × {
        "x": 5,
        "y": 7,
        "_id": "mP_2d615fd34f97ac906e162c6fc6aedadc4d140",
        "_ids": ".T_f0bb8da3062cc75365ae0446044f7b3270977 mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
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
    >>> d.show(colored=False)
    {
        "z": "→(a x y)",
        "x": 3,
        "y": 8,
        "_id": ".weinknSzbRNQozgJ-lwxGUsk1QCMKqODpuKHpoM",
        "_ids": {
            "z": "8oEPYIznhYXapfJ-UG-rRhvRT0QCMKqODpuKHpoM",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd (content: pD_0be33b125de54e0facc1c4d8f8f1b9aa082cd)",
            "y": "6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde (content: Ar_4fd69270474feb1c2da324cc665567f611bde)"
        }
    }
    >>> print(d.z)
    23
    >>> d >>= Random(0) >> let(f, a=[1,2,3]) >> let(f, a=[9,8,7])
    >>> d.show(colored=False)
    {
        "z": "→(a x y)",
        "x": 3,
        "y": 8,
        "_id": "iyEXKNIq6t0iZRjQBBujMt73l49s9cp4PHp-q0TO",
        "_ids": {
            "z": "WNsBmRnrF.gFDFtyNh7f45KrU39s9cp4PHp-q0TO",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd (content: pD_0be33b125de54e0facc1c4d8f8f1b9aa082cd)",
            "y": "6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde (content: Ar_4fd69270474feb1c2da324cc665567f611bde)"
        }
    }
    >>> print(d.z)
    32
    """

    def __init__(self, f, **kwargs):
        from idict.core.idict_ import Idict

        super().__init__(f, Idict, config=None)
        self.config = {k: kwargs[k] for k in sorted(kwargs.keys())}

    @cached_property
    def bytes(self):
        return dumps(self.config, sort_keys=True, cls=CustomJSONEncoder).encode()

    def __repr__(self):
        return "λ" + str(self.config)

    def __rrshift__(self, left: Union[dict, list, Random, Callable, "iLet"]):
        """
        >>> from idict.parameter.ilet import iLet
        >>> ({"x":5} >> iLet(lambda x=None:{"x": x**2}, x=5)).show(colored=False)
        {
            "x": "→(x)",
            "_id": "mnXcHdQBxbXvacMuFs5dXLIyKuZR-tw5D.nfk2Sv",
            "_ids": {
                "x": "mnXcHdQBxbXvacMuFs5dXLIyKuZR-tw5D.nfk2Sv"
            }
        }
        >>> [{}] >> iLet(lambda x=None:{"x": x**2}, x=5)
        «^ × λ{'x': 5}»
        >>> from idict import Ø, idict
        >>> d = idict() >> (Ø >> iLet(lambda x=None:{"x": x**2}, x=5))
        >>> d.show(colored=False)
        {
            "x": "→(x)",
            "_id": "in2IaGHscEXIobU6WbD2JOBlpHPR-tw5D.nfk2Sv",
            "_ids": {
                "x": "in2IaGHscEXIobU6WbD2JOBlpHPR-tw5D.nfk2Sv"
            }
        }
        """
        from idict import iEmpty

        if isinstance(left, iEmpty):
            from idict.parameter.ifunctionspace import iFunctionSpace

            return iFunctionSpace(self)
        if isinstance(left, dict) and not isinstance(left, AbstractLazyDict):
            from idict.core.idict_ import Idict

            return Idict(left) >> self
        if isinstance(left, (list, Random, Callable)):
            from idict.parameter.ifunctionspace import iFunctionSpace

            return iFunctionSpace(left, aop, self)
        return NotImplemented  # pragma: no cover

    def __rshift__(self, other: Union[dict, list, Random, Callable, "iLet", AbstractLazyDict]):
        """
        >>> iLet(lambda x:{"x": x**2}, x=5) >> [1]
        «λ{'x': 5} × ^»
        """

        if isinstance(other, (dict, list, Random, Callable, iLet)):
            from idict.parameter.ifunctionspace import iFunctionSpace

            return iFunctionSpace(self, aop, other)
        return NotImplemented  # pragma: no cover

    def __rxor__(self, left: Union[dict, list, Random, Callable, "iLet"]):
        if isinstance(left, (dict, list, Random, Callable)) and not isinstance(left, AbstractLazyDict):
            from idict.parameter.ifunctionspace import iFunctionSpace

            return iFunctionSpace(left, cop, self)
        return NotImplemented  # pragma: no cover

    def __xor__(self, other: Union[dict, list, Random, Callable, "iLet", AbstractLazyDict]):
        if isinstance(other, (dict, list, Random, Callable, iLet)):
            from idict.parameter.ifunctionspace import iFunctionSpace

            return iFunctionSpace(self, cop, other)
        return NotImplemented  # pragma: no cover
