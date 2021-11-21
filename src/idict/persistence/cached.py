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
from garoupa import ø40
from ldict.lazyval import LazyVal


def cached(d, cache):
    """
    Store each value (fid: value) and an extra value containing the fids (did: {"_ids": fids}).
    When the dict is a singleton, we have to use id² as dict id to workaround the ambiguity did=fid.
    """
    if len(d.ids) == 1:
        did2 = (d.hosh * d.hosh).id
        if did2 in cache:
            return cache[did2]
    else:
        did2 = None

    def closure(outputf, fid, fids, data, output_fields, id):
        def func(**kwargs):
            # Try loading.
            if fid in cache:
                return cache[fid]
            if did2 and did2 in cache:
                return cache[did2]

            # Process and save (all fields, to avoid a parcial ldict being stored).
            result = k = None
            for k, v in fids.items():
                # TODO (minor): all lazies are evaluated, but show() still shows deps as lazy.
                #    Fortunately the dep is evaluated only once.
                if isinstance(data[k], LazyVal):
                    data[k] = data[k](**kwargs)
                cache[v] = data[k]
                if k == outputf:
                    result = data[k]
            if result is None:
                if k is None:
                    raise Exception(f"No ids")
                raise Exception(f"{k=} not in output fields: {output_fields}. ids: {fids.items()}")
            did = did2 or id
            if did not in cache:
                cache[did] = {"_ids": fids}

            # Return requested value.
            return result

        return func

    data = d.data.copy()
    lazies = False
    output_fields = []
    for field, v in list(data.items()):
        if isinstance(v, LazyVal):
            if field.startswith("_"):
                raise Exception("Cannot have a lazy value in a metafield.", field)
            output_fields.append(field)
            lazies = True
            id = d.hashes[field].id if field in d.hashes else d.hoshes[field].id
            deps = {"^": None}
            deps.update(v.deps)
            lazy = LazyVal(field, closure(field, id, d.ids, d.data, output_fields, d.id), deps, None)
            data[field] = lazy

    # Eager saving when there are no lazies.
    if not lazies:
        for k, id in d.ids.items():
            if id not in cache:
                cache[id] = data[k]
        did = did2 or id
        if did not in cache:
            cache[did] = {"_ids": d.ids}

    return d.clone(data)


def build(id, cache, identity=ø40):
    """
    >>> from idict import idict
    >>> cache = {}
    >>> d = idict(x=5) >> (lambda x: {"y": x**2}) >> [cache]
    >>> d
    {
        "y": "→(^ x)",
        "x": 5,
        "_id": "6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4",
        "_ids": "RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4 .T_f0bb8da3062cc75365ae0446044f7b3270977"
    }
    >>> d.y
    25
    >>> cache
    {'RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4': 25, '.T_f0bb8da3062cc75365ae0446044f7b3270977': 5, '6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4': {'_ids': {'y': 'RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4', 'x': '.T_f0bb8da3062cc75365ae0446044f7b3270977'}}}
    >>> d2 = idict.fromid(d.id, cache)
    >>> d2
    {
        "y": 25,
        "x": 5,
        "_id": "6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4",
        "_ids": "RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4 .T_f0bb8da3062cc75365ae0446044f7b3270977"
    }
    >>> d == d2
    True
    """
    ids = cache[id]["_ids"]
    dic = {}
    for k, v in ids.items():
        dic[k] = cache[v]
    from idict import idict
    return idict(dic, _id=id, _ids=ids, identity=identity)
