#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the ldict project.
#  Please respect the license - more about this in the section (*) below.
#
#  ldict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ldict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ldict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
from operator import rshift as aop
from operator import xor as cop
from random import Random
from typing import Union, Callable

from ldict.core.base import AbstractLazyDict

from .ilet import iLet


class iFunctionSpace:
    """Aglutination for future application

    >>> from ldict import ldict, empty
    >>> empty >> FunctionSpace()
    {}
    >>> fs = FunctionSpace() >> empty
    >>> fs >>= {"x": 5}
    >>> fs
    «{} × {'x': 5}»
    >>> ldict(y=7) >> fs
    {
        "y": 7,
        "x": 5
    }
    >>> fs >>= ldict(y=7)
    >>> fs
    «{} × {'x': 5} × {
        "y": 7
    }»
    >>> fs >>= lambda x,y: {"z": x*y}
    >>> fs
    «{} × {'x': 5} × {
        "y": 7
    } × λ»
    """

    def __init__(self, *args):
        self.functions = args

    def __rrshift__(self, left: Union[dict, list, Random, Callable, iLet]):
        if isinstance(left, dict):
            from idict.core.idict_ import Idict
            return reduce3(lambda a, op, b: op(a, b), (Idict(left), aop) + self.functions)
        if isinstance(left, (list, Random, Callable, iLet)):
            return iFunctionSpace(left, aop, *self.functions)
        return NotImplemented

    def __rshift__(self, other: Union[dict, list, Random, Callable, iLet, AbstractLazyDict, 'iFunctionSpace']):
        if isinstance(other, (dict, list, Random, Callable, iLet, AbstractLazyDict)):
            return iFunctionSpace(*self.functions, aop, other)
        if isinstance(other, iFunctionSpace):
            return iFunctionSpace(*self.functions, aop, *other.functions)
        return NotImplemented

    def __rxor__(self, left: Union[dict, list, Random, Callable, iLet]):
        if isinstance(left, (dict, list, Random, Callable, iLet)):
            return iFunctionSpace(left, aop, *self.functions)
        return NotImplemented

    def __xor__(self, other: Union[dict, list, Random, Callable, iLet, AbstractLazyDict, 'iFunctionSpace']):
        if isinstance(other, (dict, list, Random, Callable, iLet, AbstractLazyDict)):
            return iFunctionSpace(*self.functions, cop, other)
        if isinstance(other, iFunctionSpace):
            return iFunctionSpace(*self.functions, cop, *other.functions)
        return NotImplemented

    def __repr__(self):
        txt = []
        for f in self.functions:
            if isinstance(f, list):
                s = "^"
            elif isinstance(f, Random):
                s = "~"
            elif str(f).startswith("<function "):
                s = "λ"
            else:
                s = str(f)
            txt.append(s)
        return "«" + " × ".join(txt) + "»"


def reduce3(f, lst):
    """
    Based on https://stackoverflow.com/a/69667949/9681577
    """
    lst_iter = iter(lst)
    next_args = []
    while True:
        try:
            while len(next_args) < 3:
                next_args.append(next(lst_iter))
        except StopIteration:
            break
        next_args = [f(*next_args)]
    return next_args
