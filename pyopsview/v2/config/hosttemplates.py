#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class HostTemplateManager(OpsviewConfigResourceManager):
    resource_uri = '/config/hosttemplate'
    schema_name = 'hosttemplate'
