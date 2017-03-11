#!/usr/bin/env python

from pyopsview.v2.config.bsmcomponents import BSMComponentManager
from pyopsview.v2.config.bsmservices import BSMServiceManager
from pyopsview.v2.config.flowcollectors import FlowCollectorManager
from pyopsview.v2.config.flowsources import FlowSourceManager
from pyopsview.v2.config.hashtags import HashTagManager
from pyopsview.v2.config.hostcheckcommands import HostCheckCommandManager
from pyopsview.v2.config.hostgroups import HostGroupManager
from pyopsview.v2.config.hosticons import HostIconManager
from pyopsview.v2.config.hosts import HostManager
from pyopsview.v2.config.hosttemplates import HostTemplateManager
from pyopsview.v2.config.monitoringservers import MonitoringServerManager
from pyopsview.v2.config.notificationmethods import NotificationMethodManager
from pyopsview.v2.config.roles import RoleManager
from pyopsview.v2.config.servicechecks import ServiceCheckManager
from pyopsview.v2.config.servicegroups import ServiceGroupManager
from pyopsview.v2.config.sharednotificationprofiles import \
    SharedNotificationProfileManager

from pyopsview.v2.config.tenancies import TenancyManager
from pyopsview.v2.config.timeperiods import TimePeriodManager
from pyopsview.v2.config.users import UserManager
from pyopsview.v2.config.variables import VariableManager


class ConfigClient(object):

    def __init__(self, client):
        self.client = client
        self._init_managers()

    def _init_managers(self):
        self.bsmcomponents = BSMComponentManager(self.client)
        self.bsmservices = BSMServiceManager(self.client)
        self.flowcollectors = FlowCollectorManager(self.client)
        self.flowsources = FlowSourceManager(self.client)
        self.hashtags = HashTagManager(self.client)
        self.hostcheckcommands = HostCheckCommandManager(self.client)
        self.hostgroups = HostGroupManager(self.client)
        self.hosticons = HostIconManager(self.client)
        self.hosts = HostManager(self.client)
        self.hosttemplates = HostTemplateManager(self.client)
        self.monitoringservers = MonitoringServerManager(self.client)
        self.notificationmethods = NotificationMethodManager(self.client)
        self.roles = RoleManager(self.client)
        self.servicechecks = ServiceCheckManager(self.client)
        self.servicegroups = ServiceGroupManager(self.client)
        self.sharednotificationprofiles = \
            SharedNotificationProfileManager(self.client)
        self.tenancies = TenancyManager(self.client)
        self.timeperiods = TimePeriodManager(self.client)
        self.users = UserManager(self.client)
        self.variables = VariableManager(self.client)
