import pymysql
import collections
from base.config import routine_config_file, ConfigHelper

__all__ = [
    "create_connect"
]

DB = collections.namedtuple('DB', ['db_host', 'db_name', 'db_user', 'db_passwd'])


def _read_db_config(section):
    base_cfg = ConfigHelper(routine_config_file)
    db = DB(
        db_host=base_cfg.read_config(section, "db_host"),
        db_name=base_cfg.read_config(section, "db_name"),
        db_user=base_cfg.read_config(section, "db_user"),
        db_passwd=base_cfg.read_config(section, "db_passwd"),
    )
    return db


def create_connect(section):
    # section = "database-dw"
    db = _read_db_config(section)

    conn = pymysql.connect(
        host=db.db_host,
        port=3306,
        user=db.db_user,
        passwd=db.db_passwd,
        db=db.db_name
    )
    return conn