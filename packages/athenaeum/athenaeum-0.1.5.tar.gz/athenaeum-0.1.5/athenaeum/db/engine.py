from sqlalchemy import create_engine, Engine
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any


def get_mysql_engine(*, settings_object: Optional[LazySettings] = None,
                     **db_config_item: Dict[str, Any]) -> Optional[Engine]:
    mysql_engine = None

    db_config = {
        'MYSQL_USERNAME': None,
        'MYSQL_PASSWORD': None,
        'MYSQL_HOST': None,
        'MYSQL_PORT': None,
        'MYSQL_DBNAME': None,
    }

    if settings_object is None and not db_config_item:
        return mysql_engine

    if settings_object is not None:
        db_config['MYSQL_USERNAME'] = settings_object.MYSQL_USERNAME
        db_config['MYSQL_PASSWORD'] = settings_object.MYSQL_PASSWORD
        db_config['MYSQL_HOST'] = settings_object.MYSQL_HOST
        db_config['MYSQL_PORT'] = settings_object.MYSQL_PORT
        db_config['MYSQL_DBNAME'] = settings_object.MYSQL_DBNAME

    if db_config_item:
        for key, value in db_config_item.items():
            if key in db_config:
                db_config[key] = value

    mysql_uri = 'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DBNAME}?' \
                'charset=utf8mb4'.format(**db_config)

    mysql_engine = create_engine(mysql_uri)

    return mysql_engine
