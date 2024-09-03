import os
from pydantic import BaseModel, ValidationError
from typing import Optional, Any
import yaml
class MissingConfigError(Exception):
    def __init__(self,message='Configuration file not found. Please set the environment variable, CTGENERICS_CONFIG, or create a config.yaml file in the root directory. An example config file can be seen in ./config/sample_config.yaml'):
        self.message = message
        super().__init__(self.message)

class DBConfig(BaseModel):
    host: str
    port: int
    dbname: str
    user: str
    password: str
    default_schema: Optional[str]


def load_dbconfig(config_directory:str, **kwargs: Any) -> DBConfig:
    with open(config_directory,'r') as f:
        db_config = yaml.safe_load(f)
    return DBConfig(**db_config)


class Redshift:
    def __init__(self, source="redshift_ds", schema=None):

        config_path = os.getenv('CTGENERICS_CONFIG')
        if config_path and os.path.exists(config_path):
            pass
        else:
            if os.path.exists('config.yaml'):
                config_path = 'config.yaml'
            else:
                raise MissingConfigError()
        try: 
            db_config = load_dbconfig(config_path)
        except ValidationError as e:
            print(f'Error loading db config: {e}')
    
        conn_str = f'postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.dbname}'
        conn_str