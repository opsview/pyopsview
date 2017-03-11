#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class BSMComponentManager(OpsviewConfigResourceManager):
    resource_uri = '/config/bsmcomponent'
    schema_name = 'bsmcomponent'
