#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the i-dict project.
#  Please respect the license - more about this in the section (*) below.
#
#  i-dict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  i-dict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with i-dict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#
from idict import let
from idict.function.wrapper import call


def dfhead(input="df", output="head", **kwargs):
    """
    >>> from idict import idict
    >>> d = idict.fromtoy(output_format="df")
    >>> d >>= dfhead()
    >>> d.head
       attr1  attr2  class
    0    5.1    6.4      0
    1    1.1    2.5      1
    2    6.1    3.6      0
    3    1.1    3.5      1
    4    3.1    2.5      0
    """
    return let(call, input=input, method="head", output=output)
