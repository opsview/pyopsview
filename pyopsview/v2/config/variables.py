#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class VariableManager(OpsviewConfigResourceManager):
    resource_uri = '/config/attribute'
    schema_name = 'attribute'
