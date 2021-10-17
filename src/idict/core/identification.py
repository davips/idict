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
from inspect import signature

from garoupa import Hosh, UT40_4
from orjson import dumps

# def process(field, value, version):
#     """
#     Create hosh with etype=
#         "hybrid" if 'value' is not callable
#         "ordered" if 'value' is a callable without an attribute 'hosh'
#
#     Usage:
#
#     >>> hosh, blob = process("X", 123, "UT64.4")
#     >>> hosh.id
#     '000000000000000000000dHdUWpyde2pYKmMPrlf3jsgYRCHG5r0pjr5.ppXaVVi'
#     >>> blob
#     b'{"X":123}'
#     >>> f = lambda X: 123
#     >>> hasattr(f, "hosh")
#     False
#     >>> hosh, blob = process("X", f, "UT64.4")
#     >>> hosh.id
#     'fCnqZp8kieVFrP4uCsQPLmcflhA5ENCk2oRbzdjBxUxr.2mWiVrBjut5cJmaR3m2'
#     >>> blob is None
#     True
#     >>> f.hosh = hosh
#     >>> hasattr(f, "hosh")
#     True
#     >>> hosh2, blob = process("X", f, "UT64.4")
#     >>> hosh is hosh2
#     True
#
#     Parameters
#     ----------
#     field
#     value
#     version
#
#     Returns
#     -------
#
#     """
#     if callable(value):
#         h = value.hosh if hasattr(value, "hosh") else fhosh(value, version)
#         return h, None
#     obj = {field: value}
#     # TODO: separar key do hosh pra ser usada como no artigo, para localizar o blob no db. ver abaixo """
#     """
#     tabelas do BD:
#         alias(id    -> [id])        # id original (ou nested) antes de mesclar com key   ->  [hash] ou [id1, id2, ...]
#         value(id    -> blob)        # hash  ->  valor
#
#     estrutura de dados
#         {
#             id  ->  7427923r798g423t9
#             ids ->  {
#                 x   ->  798g234gf42338h32t
#                 y   ->  987hg23r86g87g32rf
#             }
#             hashes* ->  {
#                 x   ->  078g23f809h432g0h2
#                 y   ->  fdhfd49g8h34g0h923
#             }
#             x   ->  v1
#             y   ->  v2
#     }
#     *: talvez seja melhor apenas sob demanda e ficar como atributo, não field.
#     """
#     bytes = dumps(obj, option=OPT_SORT_KEYS)
#     return Hosh(bytes, "hybrid", version=version), bytes
from ldict.exception import NoInputException

from idict.compression import pack


def fhosh(f, version):
    """
    Create hosh with etype="ordered" using bytecodeof "f" as binary content.

    Usage:

    >>> print(fhosh(lambda x: {"z": x**2}, UT40_4))
    qowiXxlIUnfRg1ZyjR0trCb6-IUJBi6bgQpYHIM8

    Parameters
    ----------
    f
    version

    Returns
    -------

    """
    # Add signature.
    fargs = list(signature(f).parameters.keys())
    if not fargs:
        raise NoInputException(f"Missing function input parameters.")
    clean = [fargs]

    # Clean line numbers.
    groups = [l for l in dis.Bytecode(f).dis().split("\n\n") if l]
    for group in groups:
        lines = [segment for segment in group.split(" ") if segment][1:]
        clean.append(lines)

    return Hosh(dumps(clean), "ordered", version=version)


def key2id(key, digits):
    """
    >>> key2id("y", 40)
    'y-_0000000000000000000000000000000000000'

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
    prefix = key[:2].ljust(2, "-") + "_"
    rest = key[2:].encode().hex().ljust(digits - 3, "0")
    return prefix + rest[:digits - 3]


def removal_id(template, field):
    """
    >>> from garoupa import ø
    >>> removal_id(ø.delete, "myfield")
    '--------------------.............myfield'
    """
    return template[:-len(field)] + field


def blobs_hashes_hoshes(data, identity):
    from idict.frozenidentifieddict import FrozenIdentifiedDict
    blobs = {}
    hashes = {}
    hoshes = {}
    for k, v in data.items():
        # TODO checar se é um ?dict mutável e congelar ele
        if isinstance(v, FrozenIdentifiedDict):
            hashes[k] = v.hosh
            hoshes[k] = hashes[k] ** key2id(k, identity.digits)
        else:
            blobs[k] = pack(v)
            hashes[k] = identity.h * blobs[k]
            hoshes[k] = hashes[k] ** key2id(k, identity.digits)
    return dict(blobs=blobs, hashes=hashes, hoshes=hoshes)