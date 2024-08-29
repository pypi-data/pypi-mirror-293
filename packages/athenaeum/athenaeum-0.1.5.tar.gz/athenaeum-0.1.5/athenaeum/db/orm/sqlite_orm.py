from peewee import SqliteDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any


def get_sqlite_orm(*, settings_object: Optional[LazySettings] = None, **db_config_item: Dict[str, Any]) -> Any:
    sqlite_orm = None

    db_config = {
        'database': None
    }

    if settings_object is None and not db_config_item:
        return sqlite_orm

    if settings_object is not None:
        db_config['database'] = settings_object.SQLITE_PATH

    if db_config_item:
        for key, value in db_config_item.items():
            if key in db_config:
                db_config[key] = value

    sqlite_orm = SqliteDatabase(**db_config)

    return sqlite_orm
