# PyOpsview :snake:

**Python REST API Client for Opsview!**

![Opsview Logo](https://raw.githubusercontent.com/opsview/pyopsview/master/opsview.png)

Copyright (C) 2003-2025 ITRS Group Ltd

## Installation

### Installing Dependencies

```bash
# Using `pip`
pip install -r https://raw.githubusercontent.com/opsview/pyopsview/master/requirements.txt

# Using `apt`
apt update && apt install python-requests python-six

# Using `apt-get`
apt-get update && apt-get install python-requests python-six

# Using `yum`
yum install python-requests python-six

# Using `dnf`
dnf install python-requests python-six

# Using `urpmi`
urpmi python-requests python-six
```

### Installing

```bash
# From `pypi`
pip install pyopsview

# From source
git clone https://github.com/opsview/pyopsview
cd pyopsview
python setup.py install
```

## Usage

### Basic Usage

```python
from __future__ import print_function

from pyopsview import OpsviewClient
from pyopsview.exceptions import OpsviewClientException

# Authenticate the client and load the appropriate API schema for the
# specific Opsview version
client = OpsviewClient(username='admin', password='initial',
                       endpoint='https://opsview.example.com')

# Create a new client using the token; this is useful for things like ansible
# where the login operation would otherwise have to be done for every operation
auth_token = client.token
client = OpsviewClient(username='admin', token=auth_token,
                       endpoint='https://opsview.example.com')

# Get a list of the configured hosts. This returns a generator.
all_hosts = client.config.hosts.list()
for host in all_hosts:
    print(host['check_interval'])

# Find all hosts monitored by the master monitoring server.
monitored_by_master = client.config.hosts.find(monitored_by='Master Monitoring Server')

# Update the address of one host
update_host = all_hosts[-1]
update_host['address'] = '127.128.129.130'
update_host = client.config.hosts.update(update_host['id'], **update_host)

# Find the Master opsview server
opsview_master = client.config.hosts.find_one(name='Opsview')
if opsview_master is None:
    raise RuntimeError('Failed to find the Opsview master server!')

# Get a list of all Service Checks on the Opsview master
master_service_checks = []
master_service_checks += opsview_master['service_checks']

for template in opsview_master['host_templates']:
    template_detail = client.hosttemplates.find_one(template['name'])
    master_service_checks += template_detail['service_checks']

for status of a host and its service checks
    service_status = client.status.service.find_one(hostname=devicename)

for status of all unhandled hosts
    service_status = list(client.status.service.find(host_filter='unhandled'))

for all unhandled checks
    unhandled_checks = list(client.status.service.find(filter= 'unhandled'))

for adding an acknowledgement to the unhandled event for Opsview on check Connectivity - LAN
    acknowldege_details = client.acknowledge_event(params={'svc.hostname': 'Opsview', 'svc.servicename': 'Connectivity - LAN'} , data={'notify': str(int(bool(True))), 'sticky': str(int(bool(True))), 'comment': 'Acknowledged and actioned by user'})

for adding an acknowldegement to the unhandled host event for Opsview
    acknowldege_details = client.acknowledge_event(params={'hst.hostname': 'Opsview'}, data={'notify': str(int(bool(True))), 'sticky': str(int(bool(True))), 'comment': 'Acknowledged and actioned by user'})

for adding an acknowldegement to all unhandled host and service events for Opsview
    acknowldege_details = client.acknowledge_event(params={'svc.hostname': 'Opsview'}, data={'notify': str(int(bool(True))), 'sticky': str(int(bool(True))), 'comment': 'Acknowledged and actioned by user'})

for deleting the acknowledgement for Opsview against check Connectivity - LAN
    acknowledge_details = client.acknowledge_delete(params={'svc.hostname': 'Opsview', 'svc.servicename': 'Connectivity - LAN'})

for deleting the acknowledgement against a host event
    acknowledge_details = client.acknowledge_delete(params={'hst.hostname': 'Opsview'})

for deleting all the acknowledgements against service checks for a host
    acknowledge_details = client.acknowledge_delete(params={'svc.hostname': 'Opsview'})    
```


## TODO

* Add schemas for other versions of Opsview
* Add API operations for:
  * Downtime
  * Service/Host Status
  * Live Object Information (Runtime)
  * Acknowledgements
  * Scheduling Rechecks
  * Graphing Data
  * Event/History Data
  * Notes
  * SNMP queries


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
