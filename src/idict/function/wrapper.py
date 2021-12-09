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

def xywrapper(function=None, config={}, Xin="X", yin="y", Xout="X", yout="y", version=0, **kwargs):
    r"""
    >>> from sklearn.utils import resample
    >>> X=[[1,2,3], [4,5,6], [11,12,13]]
    >>> y=[7,8,9]
    >>> xywrapper(resample, config={"n_samples":2, "random_state":0}, X=X, y=y)
    {'X': [[1, 2, 3], [4, 5, 6]], 'y': [7, 8], '_history': Ellipsis}
    """
    result = function(kwargs[Xin], kwargs[yin], **config)
    return {Xout: result[0], yout: result[1], "_history": ...}


xywrapper.metadata = {
    "id": "idict-----------------wrapper--xywrapper",
    "name": "xywrapper",
    "description": "Wrapper for Xy-based funcions.",
    "parameters": ...,
    "code": ...,
}
