#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class TenancyManager(OpsviewConfigResourceManager):
    resource_uri = '/config/tenancy'
    schema_name = 'tenancy'
