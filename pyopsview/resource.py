#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from __future__ import (unicode_literals)
import six
from pyopsview.utils import json


class OpsviewResourceManager(object):
    """Base class for Opsview resource managers"""

    # Name of the schema (e.g. host)
    schema_name = None

    def __init__(self, http_client):
        self._client = http_client
        self._schema = http_client._load_schema('config', self.schema_name)

    def _encode(self, data):
        return self._schema.encode(data)

    def _decode(self, data):
        return self._schema.decode(data)

    def _get(self, url, params=None):
        body = self._client.get(url, params=params)
        return self._decode(body['object'])

    def _list(self, url, params=None):
        # Make a copy of params so we don't start messing with the caller's
        # parameters
        opts = params.copy()

        body = self._client.get(url, params=opts)
        total_pages = int(body['summary']['totalpages'])
        first_page = int(body['summary']['page'])

        for page_number in range(first_page, total_pages + 1):
            # We've already got data from the first request
            if page_number > first_page:
                opts['page'] = page_number
                body = self._client.get(url, params=opts)

            for obj in body['list']:
                if obj:
                    yield self._decode(obj)

    def _create(self, url, body, params=None, **kwds):
        body = self._client.post(url, data=body, params=params)
        return self._decode(body['object'])

    def _create_many(self, url, body, params=None, **kwds):
        body = self._client.post(url, data=body, params=params)
        return body.get('objects_updated', body)

    def _update(self, url, body, params=None, **kwds):
        body = self._client.put(url, data=body, params=params)
        return self._decode(body['object'])

    def _update_many(self, url, body, params=None, **kwds):
        body = self._client.put(url, data=body, params=params)
        for obj in body['list']:
            if obj:
                yield self._decode(obj)

    def _delete(self, url):
        self._client.delete(url)


class OpsviewConfigResourceManager(OpsviewResourceManager):

    # URI for the resource (e.g. /config/hosts)
    resource_uri = None

    def _get_parameters(self):
        fields = self._schema.fields

        keyword_arguments = []
        required_arguments = []

        for (f_name, field) in six.iteritems(fields):
            if field['default'] is not None or not field['required']:
                keyword_arguments.append(field.get('altname', f_name))
            else:
                required_fields.append(field.get('altname', f_name))

        return (required_arguments, keyword_arguments)

    def find(self, params=None, **kwds):
        query = {'s.%s' % k: v for (k, v) in six.iteritems(kwds)}
        if params:
            opts = params.copy()
        else:
            opts = {}

        opts.update(query)

        return self.list(**query)

    def find_one(self, params=None, **kwds):
        try:
            return self.find(params=params, **kwds).next()
        except StopIteration:
            return None

    def create(self, params=None, **kwds):
        uri = self.resource_uri
        request = self._encode(kwds)
        return self._create(uri, body=request, params=params)

    def create_many(self, objects, params=None):
        uri = self.resource_uri
        request = {
            'list': [self._encode(obj) for obj in objects]
        }
        return self._create_many(uri, body=request, params=params)

    def update(self, id, params=None, **kwds):
        uri = '{}/{}'.format(self.resource_uri, id)
        request = self._encode(kwds)
        return self._update(uri, body=request, params=params)

    def delete(self, id):
        uri = '{}/{}'.format(self.resource_uri, id)
        return self._delete(uri)

    def list(self, search=None, **kwds):
        params = kwds
        if search:
            params['json_filter'] = json.dumps(search)

        return self._list(self.resource_uri, params=params)
