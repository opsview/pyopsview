#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class HostManager(OpsviewConfigResourceManager):
    resource_uri = '/config/host'
    schema_name = 'host'
