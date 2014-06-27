#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Read and write to a dict-like cache.

Implements The Basic Sequence and Mapping Protocol
Please see http://stackoverflow.com/a/2438926

"""

from collections import MutableMapping


class IMCache(MutableMapping):

    """Read and write to a dict-like cache."""

    MAXLEN = 1000

    def __init__(self, maxlen=MAXLEN, *a, **k):
        self.maxlen = maxlen
        self.d = dict(*a, **k)
        while len(self) > maxlen:
            self.popitem()

    def __iter__(self):
        return iter(self.d)

    def __len__(self):
        return len(self.d)

    def __getitem__(self, k):
        return self.d[k]

    def __delitem__(self, k):
        del self.d[k]

    def __setitem__(self, k, v):
        if k not in self and len(self) == self.maxlen:
            self.popitem()
        self.d[k] = v