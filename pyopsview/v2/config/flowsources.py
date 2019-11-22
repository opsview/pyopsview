#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class FlowSourceManager(OpsviewConfigResourceManager):
    resource_uri = '/config/netflow_source'
    schema_name = 'netflowsource'
