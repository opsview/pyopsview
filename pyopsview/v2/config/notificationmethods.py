#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyopsview.resource import OpsviewConfigResourceManager


class NotificationMethodManager(OpsviewConfigResourceManager):
    resource_uri = '/config/notificationmethod'
    schema_name = 'notificationmethod'
