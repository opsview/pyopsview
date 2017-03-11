#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class TimePeriodManager(OpsviewConfigResourceManager):
    resource_uri = '/config/timeperiod'
    schema_name = 'timeperiod'
