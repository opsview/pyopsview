#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class HostGroupManager(OpsviewConfigResourceManager):
    resource_uri = '/config/hostgroup'
    schema_name = 'hostgroup'
