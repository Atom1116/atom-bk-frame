from typing import List
from todo_scratch.bk_base.db.entities.entity import Entity


class BaseQueryFactory:

    def create_select_query(self, entity: Entity) -> str:
        pass

    def create_select_query_by_id(self, entity: Entity) -> str:
        pass

    def create_select_query_by_param(self, entity: Entity, key_names: List) -> str:
        pass

    def create_insert_query(self, entity: Entity, insert_rows_row: int) -> str:
        pass

    def create_update_query_by_id(self, entity: Entity) -> str:
        pass

    def create_delete_query_by_id(self, entity: Entity) -> str:
        pass
