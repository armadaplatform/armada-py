# Hermes (python)
Configuration manager for python services.
This module can be used to find and load configuration files based on `MICROSERVICE_ENV` (--env) environment variable.
Hermes looks for specified config file in entire CONFIG_PATH and loads an appropriate one.

## Usage

Import module:

    from armada import hermes

#### One file at a time

Load `myconfig.json`. 
    
    hermes.get_config('myconfig.json') 
    {"db_host: "localhost", "db_port": 3306}
    

If config file is not a `json` type, plain string is returned.
Load `myconfig.notjson`.

    hermes.get_config('myconfig.notjson') 
    "{\"db_host\": \"localhost\", \"db_port\": 3306}"

If configuration file does not exist in CONFIG_PATH `None` is returned.
    
    hermes.get_config('im_sure_it_doesnt_exist')
    None
    
#### Merged configs

merged configs can load for now only json files

Load `myconfig.json`.

    hermes.get_merged_config('myconfig.json') 
    {"db_host: "localhost", "db_port": 3306}
    
How it works:

if CONFIG_PATH is set to: `/example/config/:/example/config/dev/`   
merged config will look for file in:  
  * /example/config/myconfig.json
  * /example/config/dev/myconfig.json
  * /example/config/local/myconfig.json  

1. if all of them exists  
  /example/config/myconfig.json is overwritten by /example/config/dev/myconfig.json, and then result is overwritten by /example/config/local/myconfig.json  

2. if only one of them exists it will work as hermes.get_config

3. if configuration file does not exist, an empty dict is returned.

    ```
    hermes.get_merged_config('myconfig.json') 
    {"db_host: "localhost", "db_port": 3306}
    ```

if additionaly TEST_ENV is set to true, merged config will look for file in:
  * /example/config/myconfig.json
  * /example/config/dev/myconfig.json
  * /example/config/test/myconfig.json  

1. if all of them exists  
  /example/config/myconfig.json is overwritten by /example/config/dev/myconfig.json, and then result is overwritten by /example/config/test/myconfig.json  
  
2. rest is as when TEST_ENV is never set.

## Secrets manager

Added in version 1.4.

### Usage
1. Config must be a json file. 
2. Add secrets_manager block to config
    ```
    "secrets_manager": {
      "name": "production-example"
    }
    ```
3. Add value for specific key in form:
    ```
   secrets_manager:KEY[:TYPE]
   "password": "secrets_manager:orders-db/password"
    ```
4. Install boto3 to get secrets
    ```
    from boto3 import client

    sm_client = client('secretsmanager')

    hermes.get_merged_config(
      key='config.json',
      secrets_manager_client=sm_client,
    )
    ```
  If you didn't put client as a parameter, but you have installed boto3 we create client for you.

  From version 1.7 armada-py supports AWS CLI profiles. If you want to use them to get secrets simply add "aws_profile".
  ```
    "secrets_manager": {
      "name": "production-example",
      "aws_profile": "production"
    }
  ```
  <br><br>
KEY in secrets manager can be totally different then key in config.

Default type is 'str'. You don't need to add ':str' to value. Otherwise you need to specify data type.

### Supported types
* str
* int
* bool
* list
* dict
* file

File type - this will create a file with content from secrets manager. Filename will be KEY FROM CONFIG . Value in config for this key will be absolute path to file.

Types usage examples:
```
  "blacklisted_ips": "secrets_manager:cheater-ips:list"
  "ssh_key": "secrets_manager:orders-db/ssh-proxy/ci-deploy.key:file"
```
