import json
import os
import time

SERVICE_DISCOVERY_CONFIG_PATH = '/var/opt/service_discovery.json'


def get_address(microservice_name, env=None, app_id=None):
    config = get_combined_magellan_config()
    filtered = {key: value for key, value in config.items() if value['microservice_name'] == microservice_name}
    if env:
        filtered = {key: value for key, value in filtered.items() if value.get('env') == env}
    if app_id:
        filtered = {key: value for key, value in filtered.items() if value.get('app_id') == app_id}
    if len(filtered) == 1:
        return 'http://localhost:{}'.format(list(filtered.keys())[0])
    elif len(filtered) == 0:
        raise RequirementError('Required microservice not found: {}'.format(microservice_name))
    else:
        raise RequirementError('Found {} microservices with name: {}. Specify env or app_id'.format(len(filtered),
                                                                                                    microservice_name))


def get_combined_magellan_config():
    wait_till_requirements_are_ready()

    with open(SERVICE_DISCOVERY_CONFIG_PATH, 'r') as f:
        combined = json.load(f)
    return combined


def wait_till_requirements_are_ready():
    if os.path.isfile(SERVICE_DISCOVERY_CONFIG_PATH):
        return
    uptime_seconds = time.time() - os.stat('/proc/1').st_ctime
    if uptime_seconds < 3:
        time.sleep(3 - uptime_seconds)


class RequirementError(Exception):
    pass
