#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class ClusterManager(OpsviewConfigResourceManager):
    resource_uri = '/config/monitoringcluster'
    schema_name = 'monitoringcluster'
