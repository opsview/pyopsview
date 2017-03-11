#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class UserManager(OpsviewConfigResourceManager):
    resource_uri = '/config/contact'
    schema_name = 'contact'
