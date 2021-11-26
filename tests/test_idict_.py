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
from ldict.exception import DependenceException, NoInputException, WrongKeyType, ReadOnlyLdict

from idict import empty, idict
from idict.core.appearance import decolorize

class TestLdict(TestCase):
    def test_identity(self):
        a = empty >> {"x": 1, "y": 2}
        b = a >> empty
        self.assertEqual(a, b)
        self.assertFalse(a == {"a": 3})
        self.assertNotEqual(a, {"a": 3})
        d = {
            "_id": "Tc_fb3057e399a385aaa6ebade51ef1f31c5f7e4",
            "_ids": {"x": "tY_a0e4015c066c1a73e43c6e7c4777abdeadb9f", "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45"},
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
    "_id": "Pd_7f559308b2f3bf28c9dfd54cf6ba43b636504",
    "_ids": {
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd (no key: pD_0be33b125de54e0facc1c4d8f8f1b9aa082cd)",
        "y": "SL_6e8b071c1bc6504ea76f407e1a791e887d9ce (no key: kN_8e281576102a3dbba76fb6892a791ec26d9ce)",
        "z": "1U_fdd682399a475d5365aeb336044f7b4270977 (no key: uV_f849a33e2d854ad065ae1a41144f7b8c50977)"
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
    "_id": "dq32pdZalIcM-fc5ZX1PZjUhNSpadBnjS7VNt6Mg",
    "_ids": {
        "z": "m3S-qN-WiH188lwxKIguTF.2YniadBnjS7VNt6Mg",
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd (no key: pD_0be33b125de54e0facc1c4d8f8f1b9aa082cd)",
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977 (no key: uV_f849a33e2d854ad065ae1a41144f7b8c50977)"
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
            "_id": "dq32pdZalIcM-fc5ZX1PZjUhNSpadBnjS7VNt6Mg",
            "_ids": {
                "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
                "y": "0U_e2a86ff72e226d5365aea336044f7b4270977",
                "z": "m3S-qN-WiH188lwxKIguTF.2YniadBnjS7VNt6Mg",
            },
            "x": 3,
            "y": 5,
            "z": 15,
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
    "_id": "dq32pdZalIcM-fc5ZX1PZjUhNSpadBnjS7VNt6Mg",
    "_ids": {
        "z": "m3S-qN-WiH188lwxKIguTF.2YniadBnjS7VNt6Mg",
        "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd (no key: pD_0be33b125de54e0facc1c4d8f8f1b9aa082cd)",
        "y": "0U_e2a86ff72e226d5365aea336044f7b4270977 (no key: uV_f849a33e2d854ad065ae1a41144f7b8c50977)"
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
                "_id": "NU4YLiIschNCZX9.tuBycZ6n4BOCresH0ccu3pl7",
                "_ids": {
                    "x": "tY_a0e4015c066c1a73e43c6e7c4777abdeadb9f",
                    "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45",
                    "z": "2CwHWARvJhPEk2cDYuPicC7tfnLCresH0ccu3pl7",
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
                "_id": "q-F.7ZpdwiDTmX16eHsfJRN7DIJdmHk22sAqab0m",
                "_ids": {
                    "x": "tY_a0e4015c066c1a73e43c6e7c4777abdeadb9f",
                    "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45",
                    "z": "SwpdBZEt4A2Po04KIHG.IuOdOuGdmHk22sAqab0m",
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
