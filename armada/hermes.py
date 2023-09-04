import json
import os
from dotenv import load_dotenv

from .config import Config


def get_config_file_path(key):
    for env in os.environ.get('CONFIG_PATH', '').split(os.pathsep):
        path = os.path.join(env, key)
        if os.path.exists(path):
            return path


def get_merged_config(key, default=None, secrets_manager_client=None):
    config = Config.get(key, default)

    if isinstance(config, dict):
        secrets = _get_secrets(
            secret_id=config.get('secrets_manager', {}).get('name', ''),
            secrets_manager_client=secrets_manager_client,
        )

        if secrets:
            _merge_secrets_to_config(config, secrets)
    
    return config


def get_config(key, default=None, strip=True, secrets_manager_client=None):
    path = get_config_file_path(key)
    if path is None:
        return default
    with open(path) as config_file:
        result = config_file.read()
    if strip:
        result = result.strip()
    if key.endswith('.json'):
        result = json.loads(result)

        if isinstance(result, dict):
            secrets = _get_secrets(
                secret_id=result.get('secrets_manager', {}).get('name', ''),
                secrets_manager_client=secrets_manager_client,
            )

            if secrets:
                _merge_secrets_to_config(result, secrets)

    return result


def get_configs(key, default=None, strip=True, secrets_manager_client=None):
    path = get_config_file_path(key)
    if path is None or not os.path.isdir(path):
        return default
    result = {}
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            result[file_name] = get_config(
                key=os.path.join(key, file_name), 
                strip=strip,
                secrets_manager_client=secrets_manager_client,
            )
    return result


def get_configs_keys(key, default=None):
    path = get_config_file_path(key)
    if path is None or not os.path.isdir(path):
        return default
    result = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            result.append(os.path.join(key, file_name))
    return result

# ----------------------- SECRETS MANAGER --------------------- #

def _get_secrets(secret_id: str, secrets_manager_client=None) -> dict:
    if not secret_id:
        return {}
    
    if not secrets_manager_client:
        try:
            from boto3 import client

            env_path = get_config_file_path('.env')

            # Environment variables such as:
            # AWS_ACCESS_KEY_ID=AK...
            # AWS_SECRET_ACCESS_KEY=KXS...
            # AWS_DEFAULT_REGION=us-east-1
            # are required!
            load_dotenv(env_path)

            secrets_manager_client = client('secretsmanager', region_name='us-east-1')
        
        except:
            return {}

    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_id
        )
    except:
        return {}

    return json.loads(get_secret_value_response['SecretString'])

def _merge_secrets_to_config(config: dict, secrets: dict):
    for key, value in config.items():
        if isinstance(value, dict):
            _merge_secrets_to_config(value, secrets)
        
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _merge_secrets_to_config(item, secrets)
        
        else:
            # Values of the form "secrets_manager:KEY[:TYPE]" are read from Secrets Manager,
            # e.g. "secrets_manager:appsflyer_service/dev_key".

            value = str(value)
            value_list = value.split(':')

            if len(value_list) not in (2, 3) or not value_list[0] == 'secrets_manager':
                continue
            
            secret_key = value_list[1]
            secret_value = secrets.get(secret_key)
            secret_type = value_list[2] if len(value_list) == 3 else 'str'

            if secret_value:
                config[key] = _convert_secret_value(secret_type, secret_value, key)

def _convert_secret_value(secret_type: str, secret_value: str, config_key: str):
    secret_type = secret_type.lower()

    if secret_type == 'str':
        return secret_value
    elif secret_type == 'int':
        return int(secret_value)
    elif secret_type == 'dict' or secret_type == 'list':
        return json.loads(secret_value)
    elif secret_type == 'bool':
        return json.loads(secret_value.lower())
    elif secret_type == 'file':
        config_dir = os.path.dirname(get_config_file_path('config.json'))
        file_path = os.path.join(config_dir, config_key)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                # Secrets manager convert \n \t etc. to double slash so..
                # But just in case I also add split by \n
                lines = secret_value.split('\\n')
                if len(lines) == 1:
                    lines = secret_value.split('\n')

                file.write('\n'.join(lines) + '\n')
        
            os.chmod(file_path, 0o600)
        
        return os.path.abspath(file_path)

    raise Exception(f'Secret type: {secret_type} not supported.')
