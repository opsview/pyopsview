#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class MonitoringServerManager(OpsviewConfigResourceManager):
    resource_uri = '/config/monitoringserver'
    schema_name = 'monitoringserver'
