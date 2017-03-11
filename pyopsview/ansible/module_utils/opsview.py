#!/usr/bin/env python

from __future__ import print_function

import sys

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import _load_params
import six

from pyopsview import OpsviewClient


def _fail_early(message, **kwds):
    """The module arguments are dynamically generated based on the Opsview
    version. This means that fail_json isn't available until after the module
    has been properly initialized and the schemas have been loaded.
    """
    import json

    output = dict(kwds)
    output.update({
        'msg': message,
        'failed': True,
    })
    print(json.dumps(output))
    sys.exit(1)


def _compare_recursive(old, new):
    """Deep comparison between objects; assumes that `new` contains
    user defined parameters so only keys which exist in `new` will be
    compared. Returns `True` if they differ. Else, `False`.
    """
    if isinstance(new, dict):
        for key in six.iterkeys(new):
            try:
                if _compare_recursive(old[key], new[key]):
                    return True
            except (KeyError, TypeError):
                return True

    elif isinstance(new, list) or isinstance(new, tuple):
        for i, item in enumerate(new):
            try:
                if _compare_recursive(old[i], item):
                    return True
            except (IndexError, TypeError):
                return True
    else:
        return old != new

    return False


class OpsviewAnsibleModuleBasic(object):

    argument_spec = {
        'username': {'required': True, 'type': 'str'},
        'token': {'required': True, 'type': 'str'},
        'endpoint': {'required': True, 'type': 'str'},
    }

    def __init__(self):
        self.argspec = dict(self.argument_spec)

        module = AnsibleModule(supports_check_mode=True,
                               argument_spec=self.argspec)

        self.changed = False
        self.status = {}
        self.fail_json = module.fail_json
        self.exit_json = module.exit_json
        self.check_mode = module.check_mode
        self.params = module.params
        self.module = module

    def warn(self, warning):
        self.module._warnings.append(warning)
        self.module.log('[WARNING] %s' % warning)

    def exit(self):
        self.exit_json(changed=self.changed, **self.status)

    def fail(self, message):
        self.fail_json(msg=message, **self.status)

    def make_client(self):
        self.client = OpsviewClient(**{
            k: v for (k, v) in six.iteritems(self.params)
            if k in ['username', 'endpoint', 'token', 'password']
        })

    def __call__(self):
        pass


class OpsviewAnsibleModuleAdvanced(object):

    login_argument_spec = {
        'username': {'required': True, 'type': 'str'},
        'token': {'required': True, 'type': 'str'},
        'endpoint': {'required': True, 'type': 'str'},
    }

    additional_argument_spec = {
        'state': {'default': 'updated',
                  'choices': ['present', 'updated', 'absent']},
        'object_id': {'type': 'int'},
    }

    def _pre_init(self, object_type):
        """To know the arguments, they must be loaded from the schema. This is
        only possible once the client has been initialized (otherwise the
        opsview version is not known). This function gathers the connection
        arguments before the module is initialized so that the argument spec
        can be set.
        It also gets a list of all parameters which have been specified so that
        we can differentiate between null parameters and omitted parameters.
        """
        # Internal Ansible function to load the arguments
        pre_params = _load_params()

        login_params = {}
        for key in six.iterkeys(self.login_argument_spec):
            if key not in pre_params or not pre_params[key]:
                raise ValueError('Argument [%s] is required' % key)

            login_params[key] = pre_params[key]

        # Save a list of all the specified parameters so we know which null
        # parameters to remove
        self.specified_params = [k for k in six.iterkeys(pre_params)
                                 if not k.startswith('_')]

        # Save the manager as, for example `client.config.hostgroups`
        client = OpsviewClient(**login_params)
        self.manager = getattr(client.config, object_type)

        # Build the argument spec with the necessary values
        self.argspec = self._build_argspec()
        self.argspec.update(self.login_argument_spec)
        self.argspec.update(self.additional_argument_spec)

    def __init__(self, object_type):
        try:
            self._pre_init(object_type)
        except Exception as e:
            _fail_early("Error: %s" % e)

        module = AnsibleModule(supports_check_mode=True, bypass_checks=True,
                               argument_spec=self.argspec)

        self.changed = False
        self.status = {}
        self.fail_json = module.fail_json
        self.exit_json = module.exit_json
        self.check_mode = module.check_mode
        self.params = module.params
        self.module = module
        self._validate_arguments()

    def warn(self, warning):
        self.module._warnings.append(warning)
        self.module.log('[WARNING] %s' % warning)

    def _validate_arguments(self):
        for field_name, field in six.iteritems(self.argspec):
            if self.params.get(field_name) is None and field.get('required'):
                self.fail('Argument %s is required' % field_name)

    def _build_argspec(self):
        """Builds the ansible argument spec using the fields from the schema
        definition. It's the caller's responsibility to add any arguments which
        are not defined in the schema (e.g. login parameters)
        """
        fields = self.manager._schema.fields
        argspec = {}

        for (field_name, field) in six.iteritems(fields):
            # Readonly fields are omitted, obviously
            if field.get('readonly', False):
                continue

            argspec_field = {'required': field.get('required', False)}

            # Set the name of the argument as the `altname` if it's specified.
            # Otherwise, use the same name as the API does.
            if field['altname']:
                name = field['altname']
            else:
                name = field_name

            argspec[name] = argspec_field

        return argspec

    def get_object_params(self):
        """Returns all of the parameters which should be used to create/update
        an object.
        * Omits any parameters not defined in the schema
        * Omits any null parameters if they were not explicitly specified
        """
        return {name: value for (name, value) in six.iteritems(self.params)
                if (name not in self.additional_argument_spec and
                    name not in self.login_argument_spec and
                    (value is not None or name in self.specified_params))}

    def exit(self):
        self.exit_json(changed=self.changed, **self.status)

    def fail(self, message):
        self.fail_json(msg=message, **self.status)

    def _requires_update(self, old_object, new_object):
        """Checks whether the old object and new object differ; only checks
        keys which exist in the new object
        """
        old_encoded = self.manager._encode(old_object)
        new_encoded = self.manager._encode(new_object)
        return _compare_recursive(old_encoded, new_encoded)

    def ensure_absent(self, existing_object):
        if existing_object is None:
            self.changed = False
        else:
            self.changed = True
            if not self.check_mode:
                self.manager.delete(existing_object['id'])

    def ensure_present(self, existing_object):
        if existing_object is None:
            self.changed = True
            if not self.check_mode:
                existing_object = self.manager.create(
                    **self.get_object_params()
                )
        else:
            self.changed = False

        if not self.check_mode:
            self.status['object_id'] = existing_object['id']

    def ensure_updated(self, existing_object=None):
        if existing_object is None:
            self.changed = True
            if not self.check_mode:
                existing_object = self.manager.create(
                    **self.get_object_params()
                )
        else:
            if self._requires_update(existing_object, self.get_object_params()):
                self.changed = True
                existing_object = self.manager.update(
                    existing_object['id'],
                    **self.get_object_params()
                )
            else:
                self.changed = False

        if not self.check_mode:
            self.status['object_id'] = existing_object['id']

    def __call__(self):
        if self.params['object_id'] is not None:
            existing_object = self.manager.find_one(id=self.params['object_id'])

            if existing_object is None:
                self.fail('Failed to find object with id: {}'
                          .format(self.params['object_id']))

        else:
            existing_object = self.manager.find_one(name=self.params['name'])

        if self.params['state'] == 'absent':
            self.ensure_absent(existing_object)

        elif self.params['state'] == 'present':
            self.ensure_present(existing_object)

        elif self.params['state'] == 'updated':
            self.ensure_updated(existing_object)
