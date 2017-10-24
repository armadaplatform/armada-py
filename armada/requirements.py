import json
import glob
import os
import pyfscache
import time

MAGELLAN_CONFIG_PATH = '/var/opt/local-magellan/'

cache_it = pyfscache.FSCache('/tmp/cache')


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


@cache_it
def get_combined_magellan_config():
    wait_till_requirements_are_ready()

    files = glob.glob(os.path.join(MAGELLAN_CONFIG_PATH, '*.json'))
    combined = {}
    for file in files:
        with open(file, 'r') as f:
            combined.update(json.load(f))
    return combined


def wait_till_requirements_are_ready():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    if uptime_seconds < 3:
        time.sleep(3 - uptime_seconds)


class RequirementError(Exception):
    pass
