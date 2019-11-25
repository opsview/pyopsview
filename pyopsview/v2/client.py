#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import requests

from pyopsview import exceptions as exc
from pyopsview import schema
from pyopsview.utils import json
from pyopsview.v2.config import ConfigClient


class Client(object):

    default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
    }

    def __init__(self, endpoint, username=None, password=None, token=None,
                 strict=False, **request_kwds):

        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'

        if not endpoint.endswith('/rest/'):
            endpoint = endpoint + 'rest/'

        self.base_url = endpoint

        if not (username and (token or password)):
            raise exc.OpsviewClientException(
                'Must specify username and either token or password'
            )

        self._version = None
        self.token = token
        self._request_kwds = request_kwds
        self._username = username
        self._password = password
        self._session = requests.session()
        self._session.headers = Client.default_headers
        self._authenticate()
        self._load_schema = self._get_schema_loader(strict)
        self._init_clients()

    def _init_clients(self):
        self.config = ConfigClient(self)

    @property
    def version(self):
        if self._version is None:
            self._version = self.info()['opsview_version']
        return self._version

    def _get_schema_loader(self, strict=False):
        """Gets a closure for schema.load_schema with the correct/current
        Opsview version
        """
        return functools.partial(schema.load_schema, version=self.version,
                                 strict=strict)

    def _authenticate(self):
        self._session.headers.pop('X-Opsview-Username', None)
        self._session.headers.pop('X-Opsview-Token', None)

        if self._username and self._password:
            payload = {
                'username': self._username,
                'password': self._password,
            }

            response = self._request('POST', 'login', data=payload)
            self.token = response['token']

        self._session.headers['X-Opsview-Username'] = self._username
        self._session.headers['X-Opsview-Token'] = self.token

    def _url(self, path):
        if path[0] == '/':
            path = path[1:]

        return self.base_url + path

    def _request(self, method, path, data=None, params=None, expected=[200]):
        if data is not None:
            data = json.dumps(data)

        response = self._session.request(url=self._url(path), method=method,
                                         data=data, params=params,
                                         **self._request_kwds)
        # Force the response to be decoded as utf-8
        response.encoding = 'utf-8'
        if response.status_code not in expected:
            raise exc.OpsviewClientException(response.text)

        return json.loads(response.text)

    def get(self, url, **kwds):
        return self._request('GET', url, **kwds)

    def post(self, url, **kwds):
        return self._request('POST', url, **kwds)

    def put(self, url, **kwds):
        return self._request('PUT', url, **kwds)

    def delete(self, url, **kwds):
        return self._request('DELETE', url, **kwds)

    def reload(self, asynchronous=False, **kwargs):
        # async is now a reserved keyword from Python 3.7 but still
        # check for it in kwargs for older code.
        if asynchronous or kwargs.get("async", False):
            params = {'asynchronous': 1}
        else:
            params = {}
        return self.post('/reload', params=params)

    def reload_status(self):
        return self.get('/reload')

    def info(self):
        return self.get('/info')

    def server_info(self):
        return self.get('/serverinfo')

    def user_info(self):
        return self.get('/user')
