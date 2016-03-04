# Hermes (python)
Configuration manager for python services.
This module can be used to find and load configuration files based on `MICROSERVICE_ENV` (--env) environment variable.
Hermes looks for specified config file in entire CONFIG_PATH and loads an appropriate one.

## Usage

Import module:

    from armada import hermes

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
    

    
