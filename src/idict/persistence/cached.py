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
    def closure(id, ids, data, output_field):

        def func(**kwargs):
            # Try loading.
            if id in cache:
                return cache[id]

            # Process and save (all fields, to avoid a parcial ldict being stored).
            result = None
            for field, fid in ids.items():
                if isinstance(data[field], LazyVal):
                    data[field] = data[field]()
                cache[ids[field]] = data[field]
                if field == output_field:
                    result = data[field]
            if result is None:
                raise Exception(f"{output_field=} not in fields: {ids.items}")

            # Return requested value.
            return result

        return func

    clone = d.clone()
    for field, v in list(clone.data.items())[2:]:
        if isinstance(v, LazyVal):
            id = d.hashes[field].id if field in d.hashes else d.hoshes[field].id
            deps = {"^": None}
            deps.update(v.deps)
            clone.data[field] = LazyVal(field, closure(id, d.ids, d.data, field), deps)
    return clone
