#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class ServiceCheckManager(OpsviewConfigResourceManager):
    resource_uri = '/config/servicecheck'
    schema_name = 'servicecheck'
