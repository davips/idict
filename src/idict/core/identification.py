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


import dis
import pickle
from inspect import signature

import dill
from orjson import dumps

from garoupa import Hosh, UT40_4, Identity
from idict.data.compression import pack, NondeterminismException
from ldict.exception import NoInputException

dill_warned = False


def f2bin(f, approach):
    # Add signature.
    fields_and_params = signature(f).parameters.values()
    fields_and_params = {v.name: None if v.default is v.empty else v.default for v in fields_and_params}
    if not fields_and_params:
        raise NoInputException(f"Missing function input parameters.")
    if "_" in fields_and_params:
        return None

    if approach == "clean":
        # Remove line numbers.
        groups = [l for l in dis.Bytecode(f).dis().split("\n\n") if l]
        clean_lines = []
        for group in groups:
            lines = [segment for segment in group.split(" ") if segment][1:]
            clean_lines.append(lines)
        return dumps(clean_lines) + pickle.dumps(fields_and_params, protocol=5)
    if approach == "direct":
        c = f.__code__
        code_bin = c.co_code + str(c.co_consts).encode()
        # TODO: replace pickle for a deterministic dill if possible?
        #  it could allow a broader range of default values (numpy, models)
        return code_bin + pickle.dumps(fields_and_params, protocol=5)
    if approach == "dill":
        # TODO: one advantage of dill here is to be able to hash a custom callable instead of only functions.
        global dill_warned
        if not dill_warned:
            dill_warned = True
            print("WARNING: using 'dill' to hash functions is not determinist")
        return dill.dumps(f)


def fhosh(f, version, approach="clean"):
    """
    Create hosh with etype="ordered" using bytecode of "f" as binary content for blake3.

    For some insight on the algorithm choice inside GaROUPa, see, e.g.:
    https://news.ycombinator.com/item?id=22021984

    Usage:

    >>> print(fhosh(lambda x: {"z": x**2}, UT40_4))
    p2MGclmVa-FRxu5kFQ65RNjiK42otvusPZ9LGCi4

    >>> print(fhosh(lambda x, name=[1, 2, Ellipsis, ..., 10]: {"z": x**2}, UT40_4))
    3NPAab2SC5lsIz5ekeIQMeQU9EKRW1dYvpUsywyr

    Parameters
    ----------
    f
    version

    Returns
    -------

    """
    if hasattr(f, "hosh"):
        return f.hosh
    if (bin := f2bin(f, approach)) is None:
        f.hosh = Identity(version=version)
    else:
        f.hosh = Hosh(bin, "ordered", version=version)
    return f.hosh

# TODO: we could just use ø.hybrid * key.encode() instead of relying on this weak hash
def key2id(key, digits):
    """
    >>> key2id("y", 40)
    'y-_0000000000000000000000000000000000000'

    >>> key2id("_history", 40)
    '-h_6973746f72790000000000000000000000000'

    >>> key2id("long bad field name", 40)
    'lo_6e6720626164206669656c64206e616d65000'

    >>> key2id("long bad field name that will be truncated", 40)
    'lo_6e6720626164206669656c64206e616d65207'

    Parameters
    ----------
    key

    Returns
    -------

    """
    if key.startswith("_"):
        key = "-" + key[1:]
    prefix = key[:2].ljust(2, "-") + "_"
    rest = key[2:].encode().hex().ljust(digits - 3, "0")
    return prefix + rest[: digits - 3]


def removal_id(template, field):
    """
    >>> from garoupa import ø
    >>> removal_id(ø.delete, "myfield")
    '--------------------.............myfield'
    """
    return template[: -len(field)] + field


def blobs_hashes_hoshes(data, identity, ids, version):
    """
    >>> from idict import idict
    >>> idict(x=1, y=2, z=3, _ids={"y": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"}).show(colored=False)
    {
        "x": 1,
        "y": 2,
        "z": 3,
        "_id": "ehAAElGxN36TOvo7LdUwseCKVJyyyyyyyyyyyyyy",
        "_ids": {
            "x": "S6_787ce43265467bacea460e239d4b36762f272 (content: l8_09c7059156c4ed2aea46243e9d4b36c01f272)",
            "y": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "z": "p4_15e02e02df7f27c5cd8270aabdafb9b65d5ab (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)"
        }
    }
    """
    from idict.core.frozenidentifieddict import FrozenIdentifiedDict
    from idict.core.idict_ import Idict

    blobs = {}
    hashes = {}
    hoshes = {}
    for k, v in data.items():
        if k in ids:
            hoshes[k] = identity * ids[k]
        else:
            if isinstance(v, (Idict, FrozenIdentifiedDict)):
                hashes[k] = v.hosh
            else:
                try:
                    blobs[k] = pack(v)
                    vhosh = identity.h * blobs[k]
                except NondeterminismException:
                    vhosh = fhosh(v, version)
                hashes[k] = vhosh
            try:
                hoshes[k] = hashes[k] ** key2id(k, identity.digits)
            except KeyError as e:  # pragma: no cover
                raise Exception(
                    f"{str(e)} is not allowed in field name: {k}. It is only accepted as the first character to indicate a metafield."
                )
    return dict(blobs=blobs, hashes=hashes, hoshes=hoshes)
