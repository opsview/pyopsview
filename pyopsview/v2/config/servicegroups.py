#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class ServiceGroupManager(OpsviewConfigResourceManager):
    resource_uri = '/config/servicegroup'
    schema_name = 'servicegroup'
