from atom_bk_frame.db.db_drivers.db_driver import DbDriver
from atom_bk_frame.util.class_loader_util import get_module_by_route


class DbDriverManeger:
    DB_TYPE_DICT = {
        "mysql": ["MySqlDriver", "atom_bk_frame.db.db_drivers.mysql_driver"]
    }

    @classmethod
    def get_db_driver(cls, db_type: str) -> DbDriver:

        for key, value in cls.DB_TYPE_DICT.items():
            if key == db_type:
                driver_module_member = \
                    get_module_by_route(value[0], value[1])
                return driver_module_member()
        return Exception("not exist db driver")
