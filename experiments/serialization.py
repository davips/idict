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

import lz4.frame as lz4
import zlib
import bz2
import lzma
from pandas import DataFrame
from scipy.io.arff import loadarff

# from ldict.compression import pack
# from garoupa import ø
# ar = loadarff("airlines50k.arff")
# print(ø * pack(DataFrame(ar)))
# ar = loadarff("airlines50k.arff")
# print(ø * pack(DataFrame(ar)))
# ar = loadarff("airlines50k.arff")
# print(ø * pack(DataFrame(ar)))
# exit()

for file in ["../../airlines50k.arff"]:  # , "airlines100k.arff"]:
    print()
    print(file)

    x = [0, 0, 0, 0, 0, 0, 0]


    def df(ar):
        x[0] = DataFrame(ar)
        return x[0]


    def pick(df):
        x[1] = pickle.dumps(df, protocol=5)
        return x[1]


    def complz4(pi):
        # x[2] = lz4.compress(pi, compression_level=0)
        x[2] = lz4.compress(pi)
        return x[2]

    def compzlib(pi):
        # x[2] = zlib.compress(pi, level=0)
        x[2] = zlib.compress(pi)
        return x[2]

    def compbz2(pi):
        # x[2] = bz2.compress(pi, compresslevel=1)
        x[2] = bz2.compress(pi)
        return x[2]

    def complzma(pi):
        # x[2] = bz2.compress(pi, compresslevel=1)
        x[2] = lzma.compress(pi)
        return x[2]


    def tostr(p):
        x[3] = str(p)
        return x[3]


    def decomp(co):
        x[4] = lz4.decompress(co)
        return x[4]


    def unpick(de):
        x[5] = pickle.loads(de)
        return x[5]


    def f():
        x[6] = loadarff(file)
        return x[6]


    print("load arff", timeit(f, number=1), sep="\t")
    print("convert to pandas", timeit(lambda: df(x[6]), number=1), sep="\t")
    print("pickle", timeit(lambda: pick(x[0]), number=10), sep="\t")
    # print(">>>>>>>>>> to str", timeit(lambda: tostr(x[1]), number=1000), sep="\t")
    # print("pickle size:", len(x[0]))
    # print(">>>>>>>>>> str size:", len(x[1]))
    n=1
    print("compress lz4", timeit(lambda: complz4(x[1]), number=n), sep="\t")
    print("     final size:", len(x[2]))
    print("compress bz2", timeit(lambda: compbz2(x[1]), number=n), sep="\t")
    print("     final size:", len(x[2]))
    print("compress zlib", timeit(lambda: compzlib(x[1]), number=n), sep="\t")
    print("     final size:", len(x[2]))
    print("compress lzma", timeit(lambda: complzma(x[1]), number=n), sep="\t")
    print("     final size:", len(x[2]))

    exit()
    print(">>>>>>>>>> to str [compressed]", timeit(lambda: tostr(x[2]), number=1000), sep="\t")
    print("     final size:", len(x[0]))
    print(">>>>>>>>>> str size:", len(x[1]))
    print("uncompress lz4", timeit(lambda: decomp(x[2]), number=1), sep="\t")
    print("unpickle", timeit(lambda: unpick(x[4]), number=1), sep="\t")

"""
airlines100k
18.11314875399694
1.996661891695112
0.48285040399059653
0.28235141932964325
"""

"""
airlines200k
36.43428422510624
3.4813605742529035
0.9991299170069396
0.7922783433459699
"""
