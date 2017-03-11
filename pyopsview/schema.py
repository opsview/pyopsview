#!/usr/bin/env python

from __future__ import unicode_literals
import errno
import pkg_resources
import six
from pyopsview.utils import json

# Once a schema has been loaded will be cached here
_schemas_loaded = {}

# Dictionary of (encoder, decoders) for primitive types
_serializers = {
    'number': (None, None),
    'string': (None, None),
    'boolean': (None, None),
    'null': (None, None),
}


def encoder(type_name):
    def wrapped(func):
        existing = _serializers.get(type_name)
        _serializers[type_name] = (func, existing[1])
        return func
    return wrapped


def decoder(type_name):
    def wrapped(func):
        existing = _serializers.get(type_name)
        _serializers[type_name] = (existing[0], func)
        return func
    return wrapped


@encoder('number')
def encode_number(value):
    if value is None:
        raise ValueError('None type is not a number')

    try:
        return unicode(int(value))
    except ValueError:
        pass

    try:
        return unicode(float(value))
    except ValueError:
        pass

    return unicode(value)


@decoder('number')
def decode_number(value):
    if value is None:
        raise ValueError('None type is not a number')

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    raise ValueError('Invalid literal for number: \'{}\''.format(value))


@encoder('boolean')
def encode_boolean(value):
    if value is None:
        raise ValueError('None type is not a boolean')

    if not isinstance(value, bool) and not isinstance(value, int):
        try:
            value = int(value)
        except ValueError:
            pass

    return (unicode("1") if value else unicode("0"))


@decoder('boolean')
def decode_boolean(value):
    if value is None:
        raise ValueError('None type is not a boolean')

    if isinstance(value, bool):
        return value

    try:
        value = int(value)
    except ValueError:
        raise ValueError('Invalid literal for boolean: \'{}\''.format(value))

    if value == 0:
        return False

    if value == 1:
        return True

    raise ValueError('Invalid literal for boolean: \'{}\''.format(value))


@encoder('string')
@decoder('string')
def encode_decode_string(value):
    if value is None:
        raise ValueError('None type is not a string')

    return unicode(value)


@encoder('null')
@decoder('null')
def encode_decode_null(value):
    if value is not None:
        raise ValueError('Invalid literal for None: \'{}\''.format(value))
    return None


class SchemaField(object):

    def __init__(self, schema):
        if not isinstance(schema, dict):
            raise ValueError('Expected \'schema\' to be a dictionary')

        definitions = schema.pop('definitions', None)
        if definitions:
            schema = self._resolve_definitions(schema, definitions)

        self._encoders = []
        self._decoders = []

        self._types = schema['type']
        # type can be a list of types so ensure we can iter them
        if not isinstance(self._types, list):
            self._types = [self._types]

        # Items for array type
        self._items = schema.get('items', {})

        # Properties for object type
        self._properties = schema.get('properties', {})

        # Holds information about the fields if this is an object type
        self._object_fields = {}

        # Additional information if it has an object/array parent
        self._readonly = schema.get('readonly', False)
        self._update = schema.get('update', True)
        self._required = schema.get('required', False)
        self._default = schema.get('default', None)
        self._altname = schema.get('altname', None)

        # Populate the encoders and decoders
        for _type in self._types:
            encoder, decoder = self._get_serializer(_type)
            self._encoders.append(encoder)
            self._decoders.append(decoder)

    @property
    def fields(self):
        return {
            key: {'default': field._default,
                  'readonly': field._readonly,
                  'update': field._readonly,
                  'required': field._required,
                  'altname': field._altname,
                  'types': field._types,
                  'field': field}
            for (key, field) in six.iteritems(self._object_fields)
        }

    def _resolve_definitions(self, schema, definitions):
        """Interpolates definitions from the top-level definitions key into the
        schema. This is performed in a cut-down way similar to JSON schema.
        """
        if not definitions:
            return schema

        if not isinstance(schema, dict):
            return schema

        ref = schema.pop('$ref', None)
        if ref:
            path = ref.split('/')[2:]
            definition = definitions
            for component in path:
                definition = definitions[component]

            if definition:
                # Only update specified fields
                for (key, val) in six.iteritems(definition):
                    if key not in schema:
                        schema[key] = val

        for key in six.iterkeys(schema):
            schema[key] = self._resolve_definitions(schema[key], definitions)

        return schema

    def _get_serializer(self, _type):
        """Gets a serializer for a particular type. For primitives, returns the
        serializer from the module-level serializers.
        For arrays and objects, uses the special _get_T_serializer methods to
        build the encoders and decoders.
        """
        if _type in _serializers:  # _serializers is module level
            return _serializers[_type]
        # array and object are special types
        elif _type == 'array':
            return self._get_array_serializer()
        elif _type == 'object':
            return self._get_object_serializer()

        raise ValueError('Unknown type: {}'.format(_type))

    def _get_array_serializer(self):
        """Gets the encoder and decoder for an array. Uses the 'items' key to
        build the encoders and decoders for the specified type.
        """
        if not self._items:
            raise ValueError('Must specify \'items\' for \'array\' type')

        field = SchemaField(self._items)

        def encode(value, field=field):
            if not isinstance(value, list):
                value = [value]

            return [field.encode(i) for i in value]

        def decode(value, field=field):
            return [field.decode(i) for i in value]

        return (encode, decode)

    def _get_object_serializer(self):
        """Gets the encoder and decoder for an object. Uses the 'properties'
        key to build the encoders and decoders for the specified types,
        mapping them to their specified names and parameters. These include:
            * default  (Default: None)
            * required (Default: true)
            * readonly (Default: false)
            * update   (Default: true)
            * altname  (Default: None)
        """
        if not self._properties:
            raise ValueError('Must specify \'properties\' for \'object\' type')

        fields = {}
        for (name, definition) in six.iteritems(self._properties):
            fields[name] = SchemaField(definition)

        # Allow intraspection of field information via `fields` property
        self._object_fields = fields

        def get_pyname(name, field):
            return (field._altname if field._altname else name)

        def encode(value, fields=fields):
            """Encode an object (dictionary) for the Opsview API. Uses the
            altname for each field schema if specified.
            """
            if not isinstance(value, dict):
                # This is gonna be quite clever... if we're given a value which
                # ISNT a dictionary type, try and encode it anyway by finding
                # the only field it can go in
                required_fields = [
                    (name, field) for (name, field) in six.iteritems(fields)
                    if field._required
                ]

                mutable_fields = [
                    (name, field) for (name, field) in six.iteritems(fields)
                    if not field._readonly
                ]

                field = None
                if len(required_fields) == 1:
                    field = required_fields[0]
                elif len(mutable_fields) == 1:
                    field = mutable_fields[0]

                if field:  # Success!
                    pyname = get_pyname(field[0], field[1])
                    value = {pyname: value}
                else:
                    raise ValueError('Expected object type but got: \'{}\''
                                     .format(value))

            encoded = {}
            allowed_fields = []
            for name, field in six.iteritems(fields):
                if field._altname:
                    allowed_fields.append(field._altname)
                else:
                    allowed_fields.append(name)

            # Don't allow unknown keys for encoding
            unknown_keys = [name for name in six.iterkeys(value)
                            if name not in allowed_fields]

            if unknown_keys:
                raise ValueError('Unknown fields: \'{}\''
                                 .format('\', \''.join(unknown_keys)))

            for (key, field) in six.iteritems(fields):
                # Only encode if the field has a default value or the field has
                # actually been specified
                pyname = (field._altname if field._altname else key)
                if pyname in value or field._default is not None:
                    encoded[key] = field.encode(value.get(pyname))
                elif field._required:
                    raise ValueError('Missing required field: \'{}\''
                                     .format(pyname))

            return encoded

        def decode(value, fields=fields):
            if not isinstance(value, dict):
                raise ValueError('Cannot decode type {} as object'
                                 .format(type(value)))
            decoded = {}

            unknown_keys = [k for k in six.iterkeys(value) if k not in fields]
            if unknown_keys:
                raise ValueError('Unknown fields: \'{}\''.format(
                    '\', \''.join(unknown_keys)
                ))

            for (key, field) in six.iteritems(fields):
                # Only decode if the field has a default value or the field has
                # actually been specified
                pyname = (field._altname if field._altname else key)
                if key in value or field._default is not None:
                    decoded[pyname] = field.decode(value.get(key))

            return decoded

        return (encode, decode)

    def encode(self, value):
        """The encoder for this schema.
        Tries each encoder in order of the types specified for this schema.
        """
        if value is None and self._default is not None:
            value = self._default

        for encoder in self._encoders:
            try:
                return encoder(value)
            except ValueError as ex:
                pass

        raise ValueError('Value \'{}\' is invalid. {}'
                         .format(value, ex.message))

    def decode(self, value):
        """The decoder for this schema.
        Tries each decoder in order of the types specified for this schema.
        """
        if value is None and self._default is not None:
            value = self._default

        for decoder in self._decoders:
            try:
                return decoder(value)
            except ValueError as ex:
                pass

        raise ValueError('Value \'{}\' is invalid. {}'
                         .format(value, ex.message))


def _get_schema(_version, _type, name):
    version = _version.split('.')

    while len(version):
        try:
            return pkg_resources.resource_string(
                __name__,
                # E.g. /v2/schemas/5.3.0/config/host
                '/'.join(('v2', 'schemas',
                          '.'.join(version),
                          _type, name))
            )
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise

        version.pop()

    # Fall back to latest
    if _version != 'latest':
        return _get_schema('latest', _type, name)

    raise ValueError('Failed to find schema: {}/{}'.format(_type, name))


def load_schema(_type, name, version):
    if not name.endswith('.json'):
        name += '.json'

    schema_hash = (_type, name, version)
    if schema_hash not in _schemas_loaded:
        schema_str = _get_schema(version, _type, name)
        _schemas_loaded[schema_hash] = json.loads(unicode(schema_str))

    return SchemaField(_schemas_loaded[schema_hash])
