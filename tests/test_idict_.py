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
from unittest import TestCase

import pytest
from idict import empty, idict
from idict.core.appearance import decolorize
from idict.data.compression import unpack, pack
from ldict.exception import DependenceException, NoInputException, WrongKeyType, ReadOnlyLdict


class TestLdict(TestCase):
    def test_identity(self):
        a = empty >> {"x": 1, "y": 2}
        b = a >> empty
        self.assertEqual(a, b)
        self.assertFalse(a == {"a": 3})
        self.assertNotEqual(a, {"a": 3})
        d = {
            "_id": "mH_70118e827bbcd88303202a006d34eb63e4fbd",
            "_ids": {"x": "S6_787ce43265467bacea460e239d4b36762f272", "y": "wA_8d94995016666dd618d91cdccfe8a5fcb5c4b"},
            "x": 1,
            "y": 2,
        }
        self.assertEqual(a.asdict, d)

    def test_illdefined_function(self):
        with pytest.raises(DependenceException):
            empty >> {"x": 5} >> (lambda y: {"x": 5})
        with pytest.raises(NoInputException):
            empty >> {"x": 5} >> (lambda: {"x": 5})

    def test_setitem_value(self):
        d = idict()
        d["x"] = 3
        d["y"] = 4
        d["z"] = 5
        self.assertEqual(
            """{
    "x": 3,
    "y": 4,
    "z": 5,
    "_id": "ol_e5c16dd16f412466a532f45ddb120cb746448",
    "_ids": {
        "x": "n4_51866e4dc164a1c5cd82c0babdafb9a65d5ab (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
        "y": "I-_f967564db1ccce58af55d7fb75e2841e9c01d (content: a0_019baa6057e1ce58af55e7fb75e2841e9c01d)",
        "z": "ji_e6b7ae77dbae16c5384a72b1b88fbd4d3cd8f (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)"
    }
}""",
            decolorize(d.all),
        )

    def test_setitem_function(self):
        d = idict()
        d["x"] = 3
        d["y"] = 5
        d >>= lambda x, y: {"z": x * y}

        self.assertEqual(
            """{
    "z": "→(x y)",
    "x": 3,
    "y": 5,
    "_id": "pLhQxcF.Yn8MyR0ND1666ZBx5-nadBnjS7VNt6Mg",
    "_ids": {
        "z": "LMgQzXnuVppb3md.0Q6E7oIkqjiadBnjS7VNt6Mg",
        "x": "n4_51866e4dc164a1c5cd82c0babdafb9a65d5ab (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
        "y": "ii_6ee7b815d7ae16c5384a72b1b88fbd4d3cd8f (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)"
    }
}""",
            decolorize(d.all),
        )
        self.assertEqual(d.z, 15)

    def test_setitem_overwrite_value(self):
        d = idict()
        d["x"] = 3
        d["y"] = 5
        d >>= lambda x, y: {"z": x * y}
        d.evaluate()
        de = {
            "z": "→(x y)",
            "x": 3,
            "y": 5,
            "_id": "pLhQxcF.Yn8MyR0ND1666ZBx5-nadBnjS7VNt6Mg",
            "_ids": {
                "z": "LMgQzXnuVppb3md.0Q6E7oIkqjiadBnjS7VNt6Mg",
                "x": "n4_51866e4dc164a1c5cd82c0babdafb9a65d5ab (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
                "y": "ii_6ee7b815d7ae16c5384a72b1b88fbd4d3cd8f (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)",
            },
        }
        self.assertEqual(d, de)

        # Overwrite same value.
        d["y"] = 5
        self.assertEqual(d, de)

        # Repeate same overwrite.
        d["y"] = 5
        self.assertEqual(d, de)

        # Overwrite other value.
        d["y"] = 6
        self.assertNotEqual(d, de)

    def test_rshift(self):
        d = idict()
        d["x"] = 3
        d["y"] = 5
        d >>= lambda x, y: {"z": x * y}
        self.assertEqual(
            """{
    "z": "→(x y)",
    "x": 3,
    "y": 5,
    "_id": "pLhQxcF.Yn8MyR0ND1666ZBx5-nadBnjS7VNt6Mg",
    "_ids": {
        "z": "LMgQzXnuVppb3md.0Q6E7oIkqjiadBnjS7VNt6Mg",
        "x": "n4_51866e4dc164a1c5cd82c0babdafb9a65d5ab (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
        "y": "ii_6ee7b815d7ae16c5384a72b1b88fbd4d3cd8f (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)"
    }
}""",
            str(decolorize(d.all)),
        )
        self.assertEqual(15, d.z)
        # with pytest.raises(OverwriteException):
        #     d >>= {"z": 5}

    def test_overwrite(self):
        a = idict(x=3)
        self.assertEqual(a, a >> {"x": 3})  # overwrite
        a >>= {"y": 4}
        b = idict(y=4, x=3)
        self.assertEqual(a, b)  # new value
        self.assertEqual(a, a >> {"x": 3})  # should differ for idict/cdict
        # with pytest.raises(OverwriteException):

    def test_setitem_overwrite_function(self):
        d = idict()
        d["x"] = 1
        d["y"] = 2
        d["z"] = 3

        # Apply some function.
        old = d
        d >>= lambda x, y, z: {"z": x + y * z}  # 7
        self.assertNotEqual(old, d)
        self.assertEqual(
            d,
            {
                "_id": "fO.GZwQORND3xRsNGdQPzNnw6DCCresH0ccu3pl7",
                "_ids": {
                    "x": "S6_787ce43265467bacea460e239d4b36762f272",
                    "y": "wA_8d94995016666dd618d91cdccfe8a5fcb5c4b",
                    "z": "uuK12VIIPD7MTRotl-f4iPyMoNHCresH0ccu3pl7",
                },
                "x": 1,
                "y": 2,
                "z": 7,
            },
        )

        # Reapply same function.
        old = d
        d >>= lambda x, y, z: {"z": x + y * z}  # 15
        self.assertNotEqual(old, d)

        # Reapply same function.
        old = d
        d >>= lambda x, y, z: {"z": x + y * z}  # 31
        self.assertNotEqual(old, d)
        self.assertEqual(
            d,
            {
                "_id": "vEtxmz.hlCHyxdGZO-836Fe6wkHdmHk22sAqab0m",
                "_ids": {
                    "x": "S6_787ce43265467bacea460e239d4b36762f272",
                    "y": "wA_8d94995016666dd618d91cdccfe8a5fcb5c4b",
                    "z": "qiyFKALstbn0GaCFtLAjQGpmOuMdmHk22sAqab0m",
                },
                "x": 1,
                "y": 2,
                "z": 31,
            },
        )

        def f(x):
            return {"z": x + 2}

        a = empty >> {"x": 1, "y": 2} >> f
        b = a >> (lambda x: {"z": x ** 2})
        self.assertNotEqual(a, b)

    def test_getitem(self):
        d = empty >> {"x": 0}
        with pytest.raises(WrongKeyType):
            _ = d[1]
        with pytest.raises(KeyError):
            _ = d["1"]

    def test_delitem(self):
        d = empty >> {"x": 0}
        with pytest.raises(WrongKeyType):
            del d[1]
        with pytest.raises(KeyError):
            del d["1"]
        with pytest.raises(ReadOnlyLdict):
            d["d"] = d
            del d.d["x"]

    def test_setitem(self):
        d = empty >> {"x": 0}
        with pytest.raises(WrongKeyType):
            d[1] = 1

        d = empty >> {"d": d}
        # with pytest.raises(ReadOnlyLdict):
        #     d["d"]["x"] = 5

        # T = namedtuple("T", "hosh")

    def test_compression(self):
        self.assertTrue(callable(unpack(pack(lambda a: 5, nondeterministic_fallback=True))))
