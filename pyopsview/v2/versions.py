#!/usr/bin/env python

from __future__ import unicode_literals
from pyopsview.utils import version_cmp


def from_version(version):
    def wrapper(func):
        def wrapped(self, *args, **kwds):
            if version_cmp(version, self.version) > 0:
                raise NotImplementedError(
                    '\'{}\' is not available before version {}'
                    .format(func.__name__, version)
                )

            return func(self, *args, **kwds)


def to_version(version):
    def wrapper(func):
        def wrapped(self, *args, **kwds):
            if version_cmp(version, self.version) <= 0:
                raise NotImplementedError(
                    '\'{}\' is not available as it was removed in version {}'
                    .format(func.__name__, version)
                )

            return func(self, *args, **kwds)
