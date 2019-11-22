#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class TimePeriodManager(OpsviewConfigResourceManager):
    resource_uri = '/config/timeperiod'
    schema_name = 'timeperiod'
