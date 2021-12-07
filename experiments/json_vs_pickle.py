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
import pickle
from timeit import timeit

import dill
from pandas import DataFrame
from scipy.io.arff import loadarff

from idict.data.serialization import serialize_json, deserialize_json, serialize_numpy, deserialize_numpy

for file in ["iris.arff"]:  # , "airlines50k.arff"]:  # , "airlines100k.arff"]:
    print()
    print(file)


    def fpick(de):
        return lambda: pickle.dumps(de, protocol=5)


    def fdill(de):
        return lambda: dill.dumps(de, protocol=5)


    def fencode(de):
        return lambda: serialize_json(de)


    def fnp(de):
        return lambda: serialize_numpy(de)


    def funpick(de):
        return lambda: pickle.loads(de)


    def fundill(de):
        return lambda: dill.loads(de)


    def fdecode(de):
        return lambda: deserialize_json(de)


    def funnp(de):
        return lambda: deserialize_numpy(de)


    df = DataFrame(loadarff(file))
    np = df.to_numpy()

    for f, fun, name in [(fpick, funpick, "pick"), (fdill, fundill, "dill"), (fencode, fdecode, "json"),
                         (fnp, funnp, "np")]:
        blob = f(np)()
        print(
            name,
            "serialize", f"{timeit(f(np), number=1):.3}s",
            "size:", f"{len(blob) / 1000000:.1}MB",
            "deserialize", f"{timeit(fun(blob), number=1):.3}s",
            sep="\t"
        )
    for f, fun, name in [(fpick, funpick, "pick"), (fdill, fundill, "dill"), (fencode, fdecode, "json")]:
        blob = f(df)()
        print(
            name,
            "serialize", f"{timeit(f(df), number=1):.3}s",
            "size:", f"{len(blob) / 1000000:.1}MB",
            "deserialize", f"{timeit(fun(blob), number=1):.3}s",
            sep="\t"
        )
