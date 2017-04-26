import json

import os
import pytest

from armada.hermes import get_merged_config, get_config

config_default = {"foo": 0}
config_dev = {"foo": 1,
              "dev": True}

config_local = {"foo": 2}


@pytest.fixture(scope='module')
def tmp_config_path(tmpdir_factory):
    def dump_config(path, values):
        with open(str(path), 'w+') as config_file:
            json.dump(values, config_file)

    tmp_config_path = tmpdir_factory.mktemp('config')

    default_path = tmp_config_path.join('config.json')
    dump_config(default_path, config_default)

    os.mkdir(str(tmp_config_path.join('dev')))
    dev_path = tmp_config_path.join('dev/config.json')
    dump_config(dev_path, config_dev)

    os.mkdir(str(tmp_config_path.join('local')))
    local_config_path = tmp_config_path.join('local/config.json')
    dump_config(local_config_path, config_local)
    return str(tmp_config_path)


@pytest.fixture(autouse=True)
def set_config_path(monkeypatch, tmp_config_path):
    tmp_dev_config_path = os.path.join(tmp_config_path, 'dev')
    monkeypatch.setenv('CONFIG_PATH', ':'.join([tmp_dev_config_path, tmp_config_path]))


def test_getting_simple_config():
    config = get_config('config.json')
    assert config == {"foo": 1, "dev": True}


def test_getting_merged_config():
    config = get_merged_config('config.json')
    assert config == {"foo": 2, "dev": True}
