from hashlib import md5
from timeit import timeit

from idict.core.identification import f2bin
from idict.function.data import arff2df, df2arff, df2np
from idict.function.evaluation import split

for approach in ["direct", "dill", "clean"]:
    t = 0
    for func in [arff2df, df2arff, df2np, split]:
        t += timeit(lambda: f2bin(func, approach), number=1000)
    print(approach, t, "ms", md5(f2bin(func, approach)).hexdigest(), sep="\t", end="\t")
    f = lambda a, b=5: {a: (x := "asd" * 5), "r": md5(x * b).hexdigest()}

    g = lambda a, b=5: {a: (x := "asd" * 5), "r": md5(x * b).hexdigest()}


    def h(a, b=5):
        return {a: (x := "asd" * 5), "r": md5(x * b).hexdigest()}


    def i(a, b=5):
        return {a: (x := "asd" * 5), "r": md5(x * b).hexdigest()}


    r = md5(f2bin(f, approach)).hexdigest() == md5(f2bin(g, approach)).hexdigest() == md5(
        f2bin(h, approach)).hexdigest() == md5(f2bin(i, approach)).hexdigest()
    print(r, sep="\t", end="\t")
    print()
