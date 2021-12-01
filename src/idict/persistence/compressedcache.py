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
import time
from abc import abstractmethod

from idict.persistence.cache import Cache


from threading import Thread


def alive(n):
    """Based on https://www.geeksforgeeks.org/start-and-stop-a-thread-in-python/"""
    while n > 0:
        print('contando', n)
        n -= 1
        time.sleep(5)


class CompressedCache(Cache):  # pragma: no cover
    def setblob(self, id, blob):
        # noinspection PyArgumentList
        # REMINDER: Cannot declare __setitem__ as abstract in this class since SQLA access it from its parent.
        self.__setitem__(id, blob, packit=False)

    # # see cached
    # def getwithblob(self, id):
    #     # TODO: adaptar __Getitem do SQLA
    #     # noinspection PyArgumentList
    #     # REMINDER: Cannot declare __setitem__ as abstract in this class since SQLA access it from its parent.
    #     return self.__getitem__(id, return_blob=True)

    def lock(self, id, state):
        # TODO: what it better? launch thread at cached or here(each dict-like lock-capable would have to implement)
        pass
        # t = Thread(target=alive, args=(10,))
        # t.start()

    def unlock(self):
        pass

    @abstractmethod
    def copy(self):
        raise NotImplementedError
