#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class HashTagManager(OpsviewConfigResourceManager):
    resource_uri = '/config/keyword'
    schema_name = 'keyword'
