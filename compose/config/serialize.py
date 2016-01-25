from __future__ import absolute_import
from __future__ import unicode_literals

import six
import yaml

from compose.config import types
from compose.config.config import V1
from compose.config.config import V2_1


def serialize_config_type(dumper, data):
    representer = dumper.represent_str if six.PY3 else dumper.represent_unicode
    return representer(data.repr())


yaml.SafeDumper.add_representer(types.VolumeFromSpec, serialize_config_type)
yaml.SafeDumper.add_representer(types.VolumeSpec, serialize_config_type)


def serialize_config(config):
    output = {
		service.pop('name'): service for service in config.services
    }
    return yaml.safe_dump(
        output,
        default_flow_style=False,
        indent=2,
        width=80)


def denormalize_service_dict(service_dict, version):
    service_dict = service_dict.copy()

    if 'restart' in service_dict:
        service_dict['restart'] = types.serialize_restart_spec(service_dict['restart'])

    if version == V1 and 'network_mode' not in service_dict:
        service_dict['network_mode'] = 'bridge'

    return service_dict
