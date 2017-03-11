#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class HostCheckCommandManager(OpsviewConfigResourceManager):
    resource_uri = '/config/hostcheckcommand'
    schema_name = 'hostcheckcommand'
