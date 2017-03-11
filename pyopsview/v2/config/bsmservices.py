#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class BSMServiceManager(OpsviewConfigResourceManager):
    resource_uri = '/config/bsmservice'
    schema_name = 'bsmservice'
