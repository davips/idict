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

import operator
from functools import reduce
from typing import Dict

from garoupa import Hosh
from idict.core.frozenidentifieddict import FrozenIdentifiedDict
from idict.core.identification import fhosh, removal_id, blobs_hashes_hoshes
from idict.parameter.ilet import iLet


def application(self: FrozenIdentifiedDict, other, f, config_hosh, output=None):
    """
    >>> from idict import let
    >>> from garoupa import ø
    >>> d = FrozenIdentifiedDict(x=3)
    >>> f = lambda x: {"y": x**2}
    >>> f.metadata = {"id": "ffffffffffffffffffffffffffffffffffffffff"}
    >>> d2 = application(d, f, f, ø)
    >>> d2.show(colored=False)
    {
        "y": "→(x)",
        "x": 3,
        "_id": "hk15pNBEY5b14uMvNiMIKbSLcOlfffffffffffff",
        "_ids": {
            "y": "WOE7vLHOaw5gqWDkzk-5e-d.ujsfffffffffffff",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd (content: pD_0be33b125de54e0facc1c4d8f8f1b9aa082cd)"
        }
    }
    >>> d2.hosh / f.metadata["id"] == d.id
    True
    """
    f_hosh = f.metadata["id"] if hasattr(f, "metadata") and "id" in f.metadata else fhosh(f, self.identity.version)
    f_hosh_full = self.identity * config_hosh * f_hosh  # d' = d * ħ(config) * f
    if output:
        frozen = self.frozen >> {output: other}
        outputs = [output]
    else:
        frozen = self.frozen >> other
        outputs = frozen.returned
    uf = self.hosh * f_hosh_full
    ufu_1 = lambda: solve(self.hoshes, outputs, uf)

    # Reorder items.
    newdata, newhoshes, newblobs, newhashes, = (
        {},
        {},
        self.blobs.copy(),
        self.hashes.copy(),
    )
    noutputs = len(outputs)
    if noutputs == 1:
        k = outputs[0]
        newdata[k] = frozen.data[k]
        newhoshes[k] = ufu_1() if k in self.ids else uf * ~self.hosh
    else:
        ufu_1 = ufu_1()
        acc = self.identity
        c = 0
        for i, k in enumerate(outputs):
            newdata[k] = frozen.data[k]
            if i < noutputs - 1:
                field_hosh = ufu_1 * rho(c, self.identity.digits)
                c += 1
                acc *= field_hosh
            else:
                field_hosh = ~acc * ufu_1
            newhoshes[k] = field_hosh
            if k in newblobs:
                del newblobs[k]
            if k in newhashes:
                del newhashes[k]
    for k in self.ids:
        if k not in newdata:
            newhoshes[k] = self.hoshes[k]
            newdata[k] = frozen.data[k]

    cloned_internals = dict(blobs=newblobs, hashes=newhashes, hoshes=newhoshes, hosh=uf)
    return self.clone(newdata, _cloned=cloned_internals)


def delete(self, k):
    f_hosh = self.identity * removal_id(self.identity.delete, k)  # d' = d * "--------------------...................y"
    uf = self.hosh * f_hosh
    newdata = self.data.copy()
    newdata[k] = None
    newhoshes, newblobs, newhashes, = (
        self.hoshes.copy(),
        self.blobs.copy(),
        self.hashes.copy(),
    )
    newhoshes[k] = placeholder(k, f_hosh, self.identity, self.hoshes)
    if k in newblobs:
        del newblobs[k]
    if k in newhashes:
        del newhashes[k]
    return self.clone(newdata, _cloned=dict(blobs=newblobs, hashes=newhashes, hoshes=newhoshes, hosh=uf))


def ihandle_dict(self, dictlike):
    """
    >>> from idict.core.frozenidentifieddict import FrozenIdentifiedDict as idict
    >>> d = idict(x=5, y=7, z=8)
    >>> di = ihandle_dict(d, {"y":None})
    >>> di.show(colored=False)
    {
        "x": 5,
        "y": null,
        "z": 8,
        "_id": "dejCAhZMpV8N1ZR8s3HUnCi0-LP............y",
        "_ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "gDcc4Rgrs4C3tMZUcb1Fp9KO53R............y",
            "z": "7q_3c95f44b01eb0f9e2da3bda1665567bc21bde (content: Ar_4fd69270474feb1c2da324cc665567f611bde)"
        }
    }
    >>> di2 = ihandle_dict(di, {"w":lambda x,z: x**z})
    >>> di2.show(colored=False)
    {
        "w": "→(x z)",
        "x": 5,
        "y": null,
        "z": 8,
        "_id": "p.82XiVd66i7iZcpKpspLqJjTIqs3d9r2rr8kHNE",
        "_ids": {
            "w": "APe82rIDSl0OEtKebkaueUlhuQts3d9r2rr8kHN5",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977 (content: uV_f849a33e2d854ad065ae1a41144f7b8c50977)",
            "y": "gDcc4Rgrs4C3tMZUcb1Fp9KO53R............y",
            "z": "7q_3c95f44b01eb0f9e2da3bda1665567bc21bde (content: Ar_4fd69270474feb1c2da324cc665567f611bde)"
        }
    }
    >>> ihandle_dict(di2, {"x": 55555}).show(colored=False)
    {
        "w": "→(x z)",
        "x": 55555,
        "y": null,
        "z": 8,
        "_id": "4It--fjPyar8ZE6gaxTIDiumYwBs3d9r2rr8kHNE",
        "_ids": {
            "w": "APe82rIDSl0OEtKebkaueUlhuQts3d9r2rr8kHN5",
            "x": "T7_37f7565449f62df2f074952f6484ea6581b77 (content: m9_0be75c1d3650af70f074ab2a7484eabf61b77)",
            "y": "gDcc4Rgrs4C3tMZUcb1Fp9KO53R............y",
            "z": "7q_3c95f44b01eb0f9e2da3bda1665567bc21bde (content: Ar_4fd69270474feb1c2da324cc665567f611bde)"
        }
    }
    >>> (d := ihandle_dict(idict(), {"x": 1555})).show(colored=False)
    {
        "x": 1555,
        "_id": "wD_4afbd1e993739c6d5a0dc5b075d9990f7dd30",
        "_ids": {
            "x": "wD_4afbd1e993739c6d5a0dc5b075d9990f7dd30"
        }
    }
    >>> d >>= lambda x: {"x": x**2}
    >>> d.show(colored=False)
    {
        "x": "→(x)",
        "_id": "3B1TtaEj17qDxRNp4VoyjLmvjm.s.g4HNqVBp-Sh",
        "_ids": {
            "x": "3B1TtaEj17qDxRNp4VoyjLmvjm.s.g4HNqVBp-Sh"
        }
    }
    >>> e = idict(y=7) >> d
    >>> e.show(colored=False)
    {
        "y": 7,
        "x": "→(x)",
        "_id": "3scU-U5036J7rqqAqwPVH7GgcIYs.g4HNqVBp-Sh",
        "_ids": {
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8 (content: QY_49dee83e556d2448f877a44fd26f5f2fac8c8)",
            "x": "3B1TtaEj17qDxRNp4VoyjLmvjm.s.g4HNqVBp-Sh"
        }
    }
    """
    from idict.core.frozenidentifieddict import FrozenIdentifiedDict
    from ldict.core.base import AbstractLazyDict

    clone = self.clone(rnd=dictlike.rnd) if isinstance(dictlike, AbstractLazyDict) and dictlike.rnd else self.clone()
    for k, v in dictlike.items():
        if v is None:
            clone = delete(clone, k)
        elif k not in ["_id", "_ids"]:
            if isinstance(v, iLet):
                clone = application(clone, v, v.f, v.bytes, k)
            elif callable(v):
                clone = application(clone, v, v, self.identity, k)
            else:
                internals = blobs_hashes_hoshes({k: v}, self.identity, {})
                if k in internals["blobs"]:
                    clone.blobs[k] = internals["blobs"][k]
                if k in internals["hashes"]:
                    clone.hashes[k] = internals["hashes"][k]
                clone.hoshes[k] = internals["hoshes"][k]
                hosh = reduce(
                    operator.mul, [self.identity] + [v for k, v in clone.hoshes.items() if not k.startswith("_")]
                )
                internals = dict(blobs=clone.blobs, hashes=clone.hashes, hoshes=clone.hoshes, hosh=hosh)
                del clone.data["_id"]
                del clone.data["_ids"]
                clone = FrozenIdentifiedDict(clone.data, rnd=clone.rnd, _cloned=internals, **{k: v})
    return clone


def placeholder(key, f_hosh, identity, hoshes: Dict[str, Hosh]):
    it = iter(hoshes.items())
    while (pair := next(it))[0] != key:
        pass
    # noinspection PyTypeChecker
    oldfield_hosh: Hosh = pair[1]
    right = identity
    for k, v in it:
        right *= v
    field_hosh = oldfield_hosh * right * f_hosh * ~right
    return field_hosh


def solve(hoshes, output, uf: Hosh):
    """
    >>> from idict.core.frozenidentifieddict import FrozenIdentifiedDict as idict
    >>> a = idict(x=3)
    >>> a.show(colored=False)
    {
        "x": 3,
        "_id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "_ids": {
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
        }
    }
    >>> a >>= (lambda x: {"x": x+2})
    >>> a.show(colored=False)
    {
        "x": "→(x)",
        "_id": "j9i-.G4WwbjZsi8V.dLkkb5hhPDYDDRQkGiQ6qJ8",
        "_ids": {
            "x": "j9i-.G4WwbjZsi8V.dLkkb5hhPDYDDRQkGiQ6qJ8"
        }
    }
    >>> a = idict(x=3, y=5) >> (lambda x: {"x": x+2})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["y"]
    True
    >>> a = idict(w=2, x=3) >> (lambda x: {"x": x+2})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["w"]
    True
    >>> a = idict(w=2, x=3, z=1, y=4) >> (lambda x: {"x": x+2})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["w"] * a.hoshes["z"] * a.hoshes["y"]
    True
    >>> a = idict(w=2, x=3, z=1, y=4) >> (lambda w,x,y: {"x": x+2, "a": w*x*y})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["a"] * a.hoshes["w"] * a.hoshes["z"] * a.hoshes["y"]
    True
    >>> a = idict(w=2, x=3, z=1, y=4) >> (lambda w,x,y: {"x": x+2, "y": w*x*y})
    >>> a.hosh == a.hoshes["x"] * a.hoshes["y"] * a.hoshes["w"] * a.hoshes["z"]
    True
    >>> a.show(colored=False)
    {
        "x": "→(w x y)",
        "y": "→(w x y)",
        "w": 2,
        "z": 1,
        "_id": "4k236R0oT.PI6-c2KLgmahWdNOzzkEFdqK4B1zjh",
        "_ids": {
            "x": "RonX9OcL1opfeXE9CJXL1LtpNBqgmEFdqG4B1zji",
            "y": "ofEb.nRSYsUsgAnnyp4KYFovZaUOV6000sv....-",
            "w": "ng_5dad44381c5ac2a4c1bfe594d68a486791c45 (content: Th_59bbaaedafd83522c1bf0c9fd68a48b181c45)",
            "z": "vY_6b073e90b397af73e43c1e6c4777abeeadb9f (content: YZ_9a7dbd0368c59cf0e43c74875777ab299db9f)"
        }
    }
    """
    previous = uf.ø
    for k, v in hoshes.items():
        if k not in output:
            previous *= v
    return uf * ~previous


def rho(c, digits):
    return digits // 2 * "-" + str(c).rjust(digits // 2, ".")
