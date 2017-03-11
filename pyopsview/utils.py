#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from __future__ import (unicode_literals)
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
    return json.loads(unicode(_get_schema(_type, name)))


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
        raise ValueError('Cannot normalize version: %s' % version)


def version_cmp(version_a, version_b):
    """Compares two versions"""
    a = normalize_version(version_a)
    b = normalize_version(version_b)

    i_a = a[0] * 100 + a[1] * 10 + a[0] * 1
    i_b = b[0] * 100 + b[1] * 10 + b[0] * 1

    return i_a - i_b


if __name__ == '__main__':
    from pyopsview import OpsviewClient

    client = OpsviewClient(endpoint='http://ov-uat5.opsview.com',
                           username='admin',
                           password='initial')

    for host in client.config.hosts.list():
        print host['name']
