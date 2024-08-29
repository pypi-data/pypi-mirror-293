from peewee import PostgresqlDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any


def get_postgresql_orm(*, settings_object: Optional[LazySettings] = None, **db_config_item: Dict[str, Any]) -> Any:
    postgresql_orm = None

    db_config = {
        'host': None,
        'port': None,
        'user': None,
        'password': None,
        'database': None,
    }

    if settings_object is None and not db_config_item:
        return postgresql_orm

    if settings_object is not None:
        db_config['host'] = settings_object.POSTGRESQL_HOST
        db_config['port'] = settings_object.POSTGRESQL_PORT
        db_config['user'] = settings_object.POSTGRESQL_USERNAME
        db_config['password'] = settings_object.POSTGRESQL_PASSWORD
        db_config['database'] = settings_object.POSTGRESQL_DBNAME

    if db_config_item:
        for key, value in db_config_item.items():
            if key in db_config:
                db_config[key] = value

    postgresql_orm = PostgresqlDatabase(**db_config)

    return postgresql_orm
