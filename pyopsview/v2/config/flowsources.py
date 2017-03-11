#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class FlowSourceManager(OpsviewConfigResourceManager):
    resource_uri = '/config/netflow_source'
    schema_name = 'netflowsource'
