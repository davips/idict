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
from idict.data.compression import unpack, pack
from ldict.core.appearance import decolorize
from ldict.exception import DependenceException, NoInputException, WrongKeyType, ReadOnlyLdict


class TestLdict(TestCase):
    def test_identity(self):
        a = empty >> {"x": 1, "y": 2}
        b = a >> empty
        self.assertEqual(a, b)
        self.assertFalse(a == {"a": 3})
        self.assertNotEqual(a, {"a": 3})
        d = {
            "_id": "5G_358b45f49c547174eb4bd687079b30cbbe724",
            "_ids": {"x": "fH_5142f0a4338a1da2ca3159e2d1011981ac890", "y": "S-_074b5a806933d64f111a93af359a278402f83"},
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
    "_id": "uN_ffd1a1a656d34bc1e3c450b6334481cf39273",
    "_ids": {
        "x": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9 (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
        "y": "2p_1f3a332e3920c543b89549b3ea84065bf8355 (content: a0_019baa6057e1ce58af55e7fb75e2841e9c01d)",
        "z": "HL_e332871b8bae94409da13193665aeefc55354 (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)"
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
    "_id": "wnN2sFeynlPdlFUyqmhIrXDz56QMPNZuFtrAIt6g",
    "_ids": {
        "z": "BxpUP79x3yGOGt8jpOWYnwAYPLKMPNZuFtrAIt6g",
        "x": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9 (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
        "y": "EI_20378979f4669f2e318ae9742e214fd4880d7 (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)"
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
            "_id": "wnN2sFeynlPdlFUyqmhIrXDz56QMPNZuFtrAIt6g",
            "_ids": {
                "z": "BxpUP79x3yGOGt8jpOWYnwAYPLKMPNZuFtrAIt6g",
                "x": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9 (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
                "y": "EI_20378979f4669f2e318ae9742e214fd4880d7 (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)",
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
    "_id": "wnN2sFeynlPdlFUyqmhIrXDz56QMPNZuFtrAIt6g",
    "_ids": {
        "z": "BxpUP79x3yGOGt8jpOWYnwAYPLKMPNZuFtrAIt6g",
        "x": "ME_bd0a8d9d8158cdbb9d7d4c7af1659ca1dabc9 (content: S5_331b7e710abd1443cd82d6b5cdafb9f04d5ab)",
        "y": "EI_20378979f4669f2e318ae9742e214fd4880d7 (content: Mj_3bcd9aefb5020343384ae8ccb88fbd872cd8f)"
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
                "_id": "SmicWca2i6bdY-.RVGjl1UmC1DEYp2E8pA4Gubx6",
                "_ids": {
                    "x": "fH_5142f0a4338a1da2ca3159e2d1011981ac890",
                    "y": "S-_074b5a806933d64f111a93af359a278402f83",
                    "z": "r2NUGYeVL5ztMXEY1L1VqAXfPYzYp2E8pA4Gubx6",
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
                "_id": "m3hxUQZSMBBhQK.RRKMlgxwfa-Gyf7UpbFd-ryzj",
                "_ids": {
                    "x": "fH_5142f0a4338a1da2ca3159e2d1011981ac890",
                    "y": "S-_074b5a806933d64f111a93af359a278402f83",
                    "z": "iV2sljdf9X6023.369RkVIx5SsMyf7UpbFd-ryzj",
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
        self.assertTrue(callable(unpack(pack(lambda a: 5, ensure_determinism=False))))
