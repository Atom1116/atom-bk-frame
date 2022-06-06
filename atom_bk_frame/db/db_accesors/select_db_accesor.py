import logging
import traceback
from typing import Dict, List
from todo_scratch.bk_base.db.db_accesors.base_db_accesor import BaseDbAccesor
from todo_scratch.bk_base.db.entities.entity import Entity
from todo_scratch.bk_base.util.log.log_util import get_main_logger


class SelectDbAccesor(BaseDbAccesor):
    """Selectクエリを発火するAccesorクラス
    自作のクエリによりデータ取得する場合に使用します

    Args:
        BaseDbAccesor (_type_): Accesor基底クラス
    """

    def __init__(self, entity_type: type) -> None:
        self.logger: logging.Logger = get_main_logger()
        super().__init__(entity_type)

    def select(self, query: str, param=()) -> List[Entity]:
        entities: List = []
        try:
            self.db_driver.connect()
            rows: Dict = {}
            rows = self.db_driver.fetch_with_param(query, param)
            entities = self.entity_service.create_entity_list(rows)
            self.db_driver.disconnect()
        except Exception:
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()

        return entities
