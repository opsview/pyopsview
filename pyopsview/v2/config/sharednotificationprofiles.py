#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class SharedNotificationProfileManager(OpsviewConfigResourceManager):
    resource_uri = '/config/sharednotificationprofile'
    schema_name = 'sharednotificationprofile'
