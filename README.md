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
