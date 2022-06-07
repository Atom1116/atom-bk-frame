from atom_bk_frame.db.db_drivers.db_driver import DbDriver
from atom_bk_frame.db.db_drivers.db_driver_maneger import DbDriverManeger
from atom_bk_frame.db.entities.entity_service import EntityService
from atom_bk_frame.util.settings_util import get_member_by_settings


class BaseDbAccesor:

    def __init__(self, entity_type: type) -> None:
        self.db_driver: DbDriver = self._create_db_driver()
        self.query_factory = self.db_driver.get_query_factory()
        self.entity_type: type = entity_type
        self.entity_service = EntityService(entity_type)
        super().__init__()

    def _create_db_driver(self) -> DbDriver:
        db_type = get_member_by_settings('DB_TYPE')
        if not db_type:
            raise Exception()
        return DbDriverManeger.get_db_driver(db_type)
