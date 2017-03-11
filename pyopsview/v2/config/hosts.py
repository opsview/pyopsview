#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class HostManager(OpsviewConfigResourceManager):
    resource_uri = '/config/host'
    schema_name = 'host'
