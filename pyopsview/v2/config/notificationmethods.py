#!/usr/bin/env python
from __future__ import unicode_literals
from pyopsview.resource import OpsviewConfigResourceManager


class NotificationMethodManager(OpsviewConfigResourceManager):
    resource_uri = '/config/notificationmethod'
    schema_name = 'notificationmethod'
