#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import six

from pyopsview.resource import OpsviewResourceManager


class CollectorManager(OpsviewResourceManager):
    resource_uri = '/config/collector'
    schema_name = 'collector'

    def register(self, id, collector_name):
        uri = '{}/{}'.format(self.resource_uri, id)
        request = {"name": collector_name}
        self._update(uri, body=request)

    def update(self, id, params=None, **kwds):
        uri = '{}/{}'.format(self.resource_uri, id)
        request = self._encode(kwds)
        return self._update(uri, body=request, params=params)

    def find(self, params=None, **kwds):
        query = {'s.%s' % k: v for (k, v) in six.iteritems(kwds)}
        if params:
            opts = params.copy()
        else:
            opts = {}

        opts.update(query)

        return self.list(**opts)

    def find_one(self, params=None, **kwds):
        try:
            return next(self.find(params=params, **kwds))
        except StopIteration:
            return None

    def list(self, search=None, **kwds):
        params = kwds
        if search:
            params['json_filter'] = json.dumps(search)

        return self._list(self.resource_uri, params=params)
