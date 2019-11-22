#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pkg_resources

try:
    import simplejson as json
except ImportError:
    import json


def _get_schema(schema_type, schema_name):
    if not schema_name.endswith('.json'):
        schema_name += '.json'

    return pkg_resources.resource_string(
        __name__, '/'.join(['schemas', schema_type, schema_name])
    )


def read_schema(_type, name):
    """Returns the deserialized representation of a schema, specified using the
    name of the schema"""
    return json.loads(_get_schema(_type, name))


def normalize_version(version):
    version_lst = version.split('.')
    if len(version_lst) >= 3:
        return (
            int(version_lst[0]),
            int(version_lst[1]),
            int(version_lst[2]),
        )
    elif len(version_lst) == 2:
        return (
            int(version_lst[0]),
            int(version_lst[1]),
            0,
        )
    elif len(version_lst) == 1:
        return (
            int(version_lst[0]),
            0,
            0,
        )
    else:
        raise ValueError('Cannot normalize version: %r' % version)


def version_cmp(version_a, version_b):
    """Compares two versions"""
    a = normalize_version(version_a)
    b = normalize_version(version_b)

    i_a = a[0] * 100 + a[1] * 10 + a[2]
    i_b = b[0] * 100 + b[1] * 10 + b[2]

    return i_a - i_b
