#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class FlowCollectorManager(OpsviewConfigResourceManager):
    resource_uri = '/config/netflow_collector'
    schema_name = 'netflowcollector'
