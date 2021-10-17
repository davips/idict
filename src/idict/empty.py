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
from typing import Callable, Dict, Union

from idict.frozenidentifieddict import FrozenIdentifiedDict
# from idict.core.idict_ import Idict
from ldict.parameter.functionspace import FunctionSpace


class Empty(FrozenIdentifiedDict):
    def __init__(self):
        super().__init__()

    def __rshift__(self, other: Union[Dict, Callable, FunctionSpace], config={}):
        if callable(other):
            return FunctionSpace(other)
        # if isinstance(other, (Let, Idict)):
        #     return other
        if isinstance(other, dict):
            from idict.frozenidentifieddict import Idict
            return Idict(other)
        return NotImplemented
