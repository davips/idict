#  Copyright (c) 2022. Davi Pereira dos Santos
#  This file is part of the i-dict project.
#  Please respect the license - more about this in the section (*) below.
#
#  i-dict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  i-dict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with i-dict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#

import shelve
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import partial
from threading import Thread
from time import sleep

from temporenc import packb, unpackb

from idict.persistence.shelchemy import sopen


def ping(ctx, item, timeout, stop):
    with ctx() as dic:
        while not stop[0]:
            dic[item] = packb(datetime.now())
            t = timeout / 2
            if t is None or t == 0:
                break
            while not stop[0] and t > 0:
                sleep(min(0.2, t))
                t -= 0.2


def locker(iterable, dict__url__ctxmgr=None, timeout=None, logstep=1):
    """
    Generator that skips items from 'iterable' already processed before or still being processed

    Item processing is restarted if 'timeout' expires.
    'dict_shelf' is a dict-like or a shelve-like object to store each item status
        when 'None', 'shelve.open("/tmp/locker.db")' will be used
    'logstep' is the frequency of printed messages, 'None' means 'no logs'.
    'timeout'=None keeps the job status as 'started' forever (or until it finishes)

    >>> from time import sleep
    >>> names = ["a","b","c","d","e"]
    >>> storage = {}
    >>> for name in locker(names, dict__url__ctxmgr=storage, timeout=10):
    ...    print(f"Processing {name}")
    ...    sleep(0.1)
    ...    print(f"{name} processed!")
    'a' is new, started
    Processing a
    a processed!
    'a' done
    'b' is new, started
    Processing b
    b processed!
    'b' done
    'c' is new, started
    Processing c
    c processed!
    'c' done
    'd' is new, started
    Processing d
    d processed!
    'd' done
    'e' is new, started
    Processing e
    e processed!
    'e' done
    >>> storage
    {'a': b'd', 'b': b'd', 'c': b'd', 'd': b'd', 'e': b'd'}
    >>> for name in locker(names, dict__url__ctxmgr=storage, timeout=10):
    ...    print(f"Processing {name}")
    ...    sleep(0.1)
    ...    print(f"{name} processed!")
    'a' already done, skipping
    'b' already done, skipping
    'c' already done, skipping
    'd' already done, skipping
    'e' already done, skipping
    """
    if dict__url__ctxmgr is None:
        ctx = partial(shelve.open, "/tmp/locker.db")
    elif isinstance(dict__url__ctxmgr, str):
        ctx = partial(sopen, dict__url__ctxmgr, autopack=False)
    elif isinstance(dict__url__ctxmgr, dict) and hasattr(dict__url__ctxmgr, "__contains__"):
        @contextmanager
        def ctx():
            yield dict__url__ctxmgr
    else:
        ctx = dict__url__ctxmgr

    for c, item in enumerate(iterable):
        with ctx() as dic:
            if item in dic:
                val = dic[item]
                if val == b'd':
                    status, action = 'already done', "skipping"
                elif timeout is not None and datetime.now() > unpackb(val).datetime() + timedelta(seconds=timeout):
                    status, action = "expired", "restarted"
                else:
                    status, action = 'already started', "skipping"
            else:
                status, action = "is new", "started"

        if logstep is not None and c % logstep == 0:
            print(f"'{item}' {status}, {action}")
        if action != "skipping":
            stop = [False]
            t = Thread(target=ping, args=(ctx, item, timeout, stop), daemon=True)
            t.start()
            yield item
            stop[0] = True
            t.join()
            with ctx() as dic:
                dic[item] = b'd'
            if logstep is not None and c % logstep == 0:
                print(f"'{item}' done")
