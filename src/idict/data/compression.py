#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the i-dict project.
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

import lz4.frame as lz4

from idict.config import GLOBAL


# TODO: different unpacking strategies: safe_unpack[text, np, pd, bin]; unpack[pickle/dill and also the safe ones]
from idict.data.serialization import serialize_json, deserialize_json, serialize_numpy


def pack(obj, ensure_determinism=True):
    r"""
    >>> from idict import setup
    >>> setup(compression_cachelimit_MB=0.000_100)
    >>> memo = GLOBAL["compression_cache"] = {}
    >>> GLOBAL["compression_cachesize"] = 0
    >>> b = b"001234567"
    >>> unpack(pack(b))
    b'001234567'
    >>> memo[id(b)]["unpacked"]
    b'001234567'
    >>> len(memo), GLOBAL["compression_cachesize"], GLOBAL["compression_cachelimit"]
    (1, 37, 100)
    >>> pack(b"asd")
    b'byte_\x04"M\x18h@\x03\x00\x00\x00\x00\x00\x00\x00\x87\x03\x00\x00\x80asd\x00\x00\x00\x00'
    >>> len(memo), GLOBAL["compression_cachesize"], GLOBAL["compression_cachelimit"]
    (2, 68, 100)
    >>> len(pack(b"123"))
    31
    >>> len(memo), GLOBAL["compression_cachesize"], GLOBAL["compression_cachelimit"]
    (3, 99, 100)
    >>> v = 12345
    >>> unpack(pack(v))
    12345
    >>> v = "12345"
    >>> unpack(pack(v))
    '12345'
    >>> v = 1/9238734
    >>> v
    1.0823993850239654e-07
    >>> unpack(pack(v))
    1.0823993850239654e-07
    >>> v = True
    >>> unpack(pack(v))
    True
    >>> v = None
    >>> unpack(pack(v))
    >>> import numpy as np
    >>> v = np.array([[1/3, 5/4], [1.3**6, "text"]])
    >>> unpack(pack(v))
    array([['0.3333333333333333', '1.25'],
           ['4.826809000000001', 'text']], dtype='<U32')    >>> unpack(pack(v))
    """
    memid = id(obj)
    memo = GLOBAL["compression_cache"]
    if memid in memo:
        if obj is memo[memid]["unpacked"]:
            return memo[memid]["packed"]
        else:
            # rare collision
            GLOBAL["compression_cachesize"] -= memo[memid]["packed"]
            del memo[memid]

    try:
        if isinstance(obj, (bytes, bytearray)):
            dump = obj
            prefix = b"byte_"
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            dump = serialize_json(obj)
            prefix = b"json_"
        elif str(type(obj)) == "<class 'numpy.ndarray'>":
            dump = serialize_numpy(obj)
            prefix = b""
        elif str(type(obj)) in ["<class 'pandas.core.frame.DataFrame'>", "<class 'pandas.core.series.Series'>"]:
            dump = pandas_serialize(obj)
        else:
            try:
                dump = pickle.dumps(obj, protocol=5)
                prefix = b"pckl_"
            except:
                if ensure_determinism:  # pragma: no cover
                    raise NondeterminismException("Cannot serialize deterministically.")
                import dill

                dump = dill.dumps(obj, protocol=5)
                prefix = b"dill_"

        blob = prefix + lz4.compress(dump, compression_level=0)
        GLOBAL["compression_cachesize"] += len(blob)
        memo[memid] = {"unpacked": obj, "packed": blob}

        # LRU
        keys = iter(list(memo.keys()))
        while len(memo) > 0 and GLOBAL["compression_cachesize"] > GLOBAL["compression_cachelimit"]:
            k = next(keys)
            v = memo.pop(k)["packed"]
            GLOBAL["compression_cachesize"] -= len(v)

        return blob
    except KeyError as e:  # pragma: no cover
        if str(e) == "'__getstate__'":  # pragma: no cover
            raise Exception("Unpickable value:", type(obj))
        else:
            raise e


def unpack(blob):
    view = memoryview(blob)
    prefix = view[:5]
    zipped = view[5:]
    bin = lz4.decompress(zipped)
    if prefix == b"byte_":
        value = bin
    elif prefix == b"json_":
        value = deserialize_json(bin)
    # if prefix == b"pckl_":
    #     return pickle.loads(lz4.decompress(blob))
    # if prefix == b"dill_":
    #     import dill
    #     return dill.loads(lz4.decompress(blob))
    else:
        raise Exception(f"Unknown prefix={bytes(prefix)}")
    return  value

class NondeterminismException(Exception):
    pass
