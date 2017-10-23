import json
import os
import pyfscache

MAGELLAN_CONFIG_PATH = '/var/opt/local-magellan/'

cache_it = pyfscache.FSCache('/tmp/cache', hours=1)


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
        raise Exception('microservice not found')
    else:
        raise Exception('Please specify env or app_id')


@cache_it
def get_combined_magellan_config():
    root, dirs, files = os.walk(MAGELLAN_CONFIG_PATH)
    combined = {}
    for file in files:
        with open(file, 'r') as f:
            combined.update(json.load(f))

    return combined
