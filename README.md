# PyOpsview :snake:

**Python REST API Client for Opsview!**

![Opsview Logo](https://raw.githubusercontent.com/jpgxs/pyopsview/master/opsview.png)

## Installation

### Installing Dependencies

```bash
# Using `pip`
pip install -r https://raw.githubusercontent.com/jpgxs/pyopsview/master/requirements.txt

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
git clone https://github.com/jpgxs/pyopsview
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
