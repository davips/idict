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
from ldict.lazyval import LazyVal


def cached(d, cache):
    """
    >>> from idict import idict
    >>> f = lambda x,y: {"z":x+y}
    >>> d = idict(x=5, y=7)
    >>> d2 = d >> f
    >>> d2.show(colored=False)
    {
        "z": "→(x y)",
        "x": 5,
        "y": 7,
        "id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> c = {}
    >>> d3 = cached(d2, c)
    >>> d3.show(colored=False)
    {
        "z": "→(^ x y)",
        "x": 5,
        "y": 7,
        "id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> c
    {}
    >>> d3.z
    12
    >>> c
    {'0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv': 12, '.T_f0bb8da3062cc75365ae0446044f7b3270977': 5, 'mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8': 7}
    >>> d3.show(colored=False)
    {
        "z": 12,
        "x": 5,
        "y": 7,
        "id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    """

    def closure(id, ids, data, output_field):

        def func(**kwargs):
            # Try loading.
            if id in cache:
                return cache[id]

            # Process and save (all fields, to avoid a parcial ldict being stored).
            result = None
            for k, fid in ids.items():
                if isinstance(data[k], LazyVal):
                    data[k] = data[k](**kwargs)
                cache[ids[k]] = data[k]
                if k == output_field:
                    result = {k: data[k]}
            if result is None:
                raise Exception(f"{output_field=} not in fields: {ids.items}")

            # Return requested value.
            return result

        return func

    data = d.data.copy()
    lazies = []
    for field, v in list(data.items())[:-2]:
        if isinstance(v, LazyVal):
            id = d.hashes[field].id if field in d.hashes else d.hoshes[field].id
            deps = {"^": None}
            deps.update(v.deps)
            lazy = LazyVal(field, closure(id, d.ids, d.data, field), deps, lazies)
            data[field] = lazy
            lazies.append(lazy)
    return d.clone(data)
