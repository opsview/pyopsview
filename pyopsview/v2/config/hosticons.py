#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class HostIconManager(OpsviewConfigResourceManager):
    resource_uri = '/config/hosticon'
    schema_name = 'hosticon'
