#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class BSMComponentManager(OpsviewConfigResourceManager):
    resource_uri = '/config/bsmcomponent'
    schema_name = 'bsmcomponent'
