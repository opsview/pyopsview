#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class UserManager(OpsviewConfigResourceManager):
    resource_uri = '/config/contact'
    schema_name = 'contact'
