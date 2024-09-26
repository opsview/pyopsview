#!/usr/bin/env python

from pyopsview.v2.status.service import ServiceManager


class StatusClient(object):

    def __init__(self, client):
        self.client = client
        self._init_managers()

    def _init_managers(self):
        self.service = ServiceManager(self.client)
