from walrus import Database
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any


def get_redis_orm(*, settings_object: Optional[LazySettings] = None, **db_config_item: Dict[str, Any]) -> Any:
    redis_orm = None

    db_config = {
        'host': None,
        'port': None,
        'db': None,
        'password': None,
    }

    if settings_object is None and not db_config_item:
        return redis_orm

    if settings_object is not None:
        db_config['host'] = settings_object.REDIS_HOST
        db_config['port'] = settings_object.REDIS_PORT
        db_config['db'] = settings_object.REDIS_DBNAME
        db_config['password'] = settings_object.REDIS_PASSWORD

    if db_config_item:
        for key, value in db_config_item.items():
            if key in db_config:
                db_config[key] = value

    redis_orm = Database(**db_config)

    return redis_orm
