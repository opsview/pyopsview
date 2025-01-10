#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewStatusStateManager


class ServiceManager(OpsviewStatusStateManager):
    resource_uri = '/status/service'
    schema_name = 'service'
