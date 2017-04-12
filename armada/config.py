import os
import json


class Config(object):
    config_paths = []

    @staticmethod
    def get(file_name, default=None, custom_file=None):
        config = {}
        file_list = Config.__get_path(file_name)
        if not file_list:
            if not default:
                return config
            return Config.__add_custom(default, custom_file)
        config = {}
        for file in file_list:
            config = dict(Config.__deep_update(config, Config.__load(file)))
        return Config.__add_custom(config, custom_file)

    @staticmethod
    def __add_custom(config, custom_file):
        if not custom_file:
            return config
        if not isinstance(custom_file, list):
            custom_file = [custom_file]
        for file in custom_file:
            if os.path.exists(file):
                config = dict(Config.__deep_update(config, Config.__load(file)))
        return config

    @staticmethod
    def __load(file):
        with open(file) as config_file:
            result = config_file.read()
            result = result.strip()
        if file.endswith('.json'):
            result = json.loads(result)
        return result

    @staticmethod
    def __get_path(file):
        path_list = Config.__get_env_path_list()
        file_paths = []
        for conf_dir in path_list:
            path = os.path.join(conf_dir, file)
            if os.path.exists(path):
                file_paths.append(path)
        return file_paths

    @staticmethod
    def __get_env_path_list():
        if Config.config_paths:
            return Config.config_paths

        Config.config_paths = os.environ.get('CONFIG_PATH', Config.__get_default_env_path()).split(os.pathsep)
        Config.config_paths.sort(key=len)
        for env in Config.config_paths:
            path = os.path.join(env, 'local')
            if os.path.exists(path):
                Config.config_paths.append(path)

        return Config.config_paths

    @staticmethod
    def __get_default_env_path():
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        python_paths = os.environ.get('PYTHONPATH', BASE_DIR).split(os.pathsep)
        paths = []
        for python_path in python_paths:
            path = os.path.join(python_path, 'config', 'dev')
            if os.path.exists(path):
                paths.append(path)
            path = os.path.join(python_path, 'config')
            if os.path.exists(path):
                paths.append(path)
        return os.pathsep.join(paths)

    @staticmethod
    def __deep_update(dict1, dict2):
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (k, dict(Config.__deep_update(dict1[k], dict2[k])))
                else:
                    yield (k, dict2[k])
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])
