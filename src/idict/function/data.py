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

"""
Functions to be used directly within an idict workflow
"""

import numpy as np
from sklearn.preprocessing import OneHotEncoder

# TODO: break down all sklearn and numpy used inside binarize,
#  so e.g. the fit-wrapper can be used for OHE; and binarize can be a composition.
from idict.macro import is_number


def nomcols(input="X", output="nomcols", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([[0, "a", 1.6], [3.2, "b", 2], [8, "c", 3]])
    >>> nomcols(X=X)
    {'nomcols': [1], '_history': Ellipsis}
    """
    X = kwargs[input]
    idxs = []
    for i, x in enumerate(X[0]):
        if not is_number(x):
            idxs.append(i)
    return {output: idxs, "_history": ...}


def binarize(input="X", idxsin="nomcols", output="Xbin", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([[0, "a", 1.6], [3.2, "b", 2], [8, "c", 3]])
    >>> binarize(X=X, nomcols=[1])
    {'Xbin': array([[1. , 0. , 0. , 0. , 1.6],
           [0. , 1. , 0. , 3.2, 2. ],
           [0. , 0. , 1. , 8. , 3. ]]), '_history': Ellipsis}
    """
    X = kwargs[input]
    cols = kwargs[idxsin]
    encoder = OneHotEncoder()
    nom = encoder.fit_transform(X[:, cols]).toarray()
    num = np.delete(X, cols, axis=1).astype(float)
    Xout = np.column_stack((nom, num))
    return {output: Xout, "_history": ...}


nomcols.metadata = {
    "id": "---------------------------------nomcols",
    "name": "nomcols",
    "description": "List column indices of nominal attributes.",
    "parameters": ...,
    "code": ...,
}
binarize.metadata = {
    "id": "--------------------------------binarize",
    "name": "binarize",
    "description": "Binarize nominal attributes so they can be handled as numeric.",
    "parameters": ...,
    "code": ...,
}
