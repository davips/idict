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
from unittest import TestCase

import pytest

from ldict import empty
from ldict.core.inspection import extract_input, extract_dictstr, extract_returnstr
from ldict.core.rshift import list2progression
from ldict.exception import NoInputException, BadOutput, InconsistentLange, \
    MultipleDicts, NoReturnException


class Test(TestCase):
    def test_input_fields(self):
        with pytest.raises(NoInputException):
            extract_input(lambda: 3)
        f = lambda **kwargs: {"x": 3}
        with pytest.raises(NoInputException):
            extract_input(f)

    def test_output_fields(self):
        def f(x):
            pass

        with pytest.raises(NoReturnException):
            extract_dictstr(extract_returnstr(f))

        def f(x):
            return {"x": 1}, {"y": 2}

        with pytest.raises(MultipleDicts):
            extract_dictstr(extract_returnstr(f))

        def f(x):
            return 0

        with pytest.raises(BadOutput):
            extract_dictstr(extract_returnstr(f))

    def test_application(self):
        with pytest.raises(BadOutput):
            _ = empty >> {"x": 2} >> (lambda x: 0)

    def test_list2progression(self):
        with pytest.raises(InconsistentLange):
            list2progression([1, 2, 5, ..., 9])
