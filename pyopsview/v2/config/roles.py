#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class RoleManager(OpsviewConfigResourceManager):
    resource_uri = '/config/role'
    schema_name = 'role'
