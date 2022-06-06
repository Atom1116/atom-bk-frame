import logging
import traceback
from typing import Dict, List
from todo_scratch.bk_base.db.db_accesors.base_db_accesor import BaseDbAccesor
from todo_scratch.bk_base.db.entities.entity import Entity
from todo_scratch.bk_base.util.log.log_util import get_main_logger


class DbAccesor(BaseDbAccesor):
    """エンティティテーブルのCRUD処理をまとめたクラス

    Args:
        BaseDbAccesor (_type_): DBAccesor基底クラス
    """

    def __init__(self, entity_type: type) -> None:
        self.logger: logging.Logger = get_main_logger()
        super().__init__(entity_type)

    def select_all(self,) -> List[Entity]:
        """全てのレコードを取得します

        Returns:
            List[Entity]: 取得したレコードエンティティリスト
        """
        entities: List[Entity] = []
        try:
            self.db_driver.connect()
            query = self.query_factory.create_select_query(self.entity_type())
            rows = self.db_driver.fetch_with_param(query, ())
            entities = self.entity_service.create_entity_list(rows)
        except Exception:
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return entities

    def select_by_id(self, id) -> Entity:
        """指定した主キーのレコードを取得します

        Args:
            id (_type_): 主キー

        Returns:
            Entity: 取得したレコードエンティティリスト
        """
        entities: List[Entity] = []
        try:
            self.db_driver.connect()
            query = self.query_factory.create_select_query_by_id(self.entity_type())
            rows = self.db_driver.fetch_with_param(query, (id,))
            entities = self.entity_service.create_entity_list(rows)
        except Exception:
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return None if len(entities) <= 0 else entities[0]

    def select_by_param(self, param: Dict) -> Entity:
        """指定した条件のレコードを取得します

        Args:
            param (Dict): 取得条件

        Returns:
            Entity: 取得したレコードエンティティリスト
        """
        entities: List[Entity] = []
        try:
            self.db_driver.connect()
            query = self.query_factory.\
                create_select_query_by_param(self.entity_type(), param.keys())
            rows = self.db_driver.fetch_with_param(query, param)
            entities = self.entity_service.create_entity_list(rows)
        except Exception:
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return entities

    def insert(self, entity: Entity) -> int:
        """レコードの追加

        Args:
            entity (Entity): 追加するレコード

        Returns:
            int: 追加したレコードのID
        """
        try:
            self.db_driver.connect(is_transaction=True)
            query = self.query_factory.create_insert_query(
                entity,
                1
            )
            params = self._create_param_extra_insert_require([entity])
            insert_row_id = self.db_driver.execute(query, params)
            self.db_driver.commit()
        except Exception:
            self.db_driver.rollback()
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return insert_row_id

    def insert_bulk(self, entities: List[Entity]) -> int:
        """レコードの一括追加

        Args:
            entities (List[Entity]): 追加するレコード

        Returns:
            int: 追加したレコード数
        """
        try:
            self.db_driver.connect(is_transaction=True)
            query = self.query_factory.create_insert_query(
                entities[0],
                len(entities)
            )
            params = self._create_param_extra_insert_require(entities)
            rows = self.db_driver.execute_bulk(query, params)
            self.db_driver.commit()
        except Exception:
            self.db_driver.rollback()
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return rows

    def update(self, entity: Entity) -> int:
        """レコードの更新

        Args:
            entity (Entity): 更新するレコード

        Returns:
            int: 更新したレコードのID
        """
        effect_row_id = 0
        try:
            self.db_driver.connect(is_transaction=True)
            query = self.query_factory.create_update_query_by_id(entity)
            set_params = entity.get_is_insert_required_items()
            where_params = entity.get_primary_colum_values()
            effect_row_id = self.db_driver.execute(query, set_params + where_params)
            self.db_driver.commit()
        except Exception:
            self.db_driver.rollback()
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return effect_row_id

    def update_bulk(self, entities: List[Entity]) -> int:
        """レコードの一括更新

        Args:
            entities (List[Entity]): 更新するレコード

        Returns:
            int: 更新したレコードの数
        """
        effect_row_count = 0
        try:
            self.db_driver.connect(is_transaction=True)
            for entity in entities:
                query = self.query_factory.create_update_query_by_id(entity)
                set_params = entity.get_is_insert_required_items()
                where_params = entity.get_primary_colum_values()
                effect_row_count += self.db_driver.execute_bulk(query, set_params + where_params)
            self.db_driver.commit()
        except Exception:
            self.db_driver.rollback()
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return effect_row_count

    def delete(self, entity: Entity) -> int:
        """レコードの削除

        Args:
            entity (Entity): 削除するレコード

        Returns:
            int: 削除したレコードのID
        """
        effect_row_id = 0
        try:
            self.db_driver.connect(is_transaction=True)
            query = self.query_factory.create_delete_query_by_id(entity)
            where_params = entity.get_primary_colum_values()
            effect_row_id += self.db_driver.execute_bulk(query, where_params)

            self.db_driver.commit()
        except Exception:
            self.db_driver.rollback()
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return effect_row_id

    def delete_bulk(self, entities: List[Entity]) -> int:
        """レコードの一括削除

        Args:
            entities (List[Entity]): 削除するレコード

        Returns:
            int: 削除したレコードの数
        """
        effect_row_count = 0
        try:
            self.db_driver.connect(is_transaction=True)
            for entity in entities:
                query = self.query_factory.create_delete_query_by_id(entity)
                where_params = entity.get_primary_colum_values()
                effect_row_count += self.db_driver.execute_bulk(query, where_params)
            self.db_driver.commit()
        except Exception:
            self.db_driver.rollback()
            self.logger.error(traceback.format_exc())
        finally:
            self.db_driver.disconnect()
        return effect_row_count

    def _create_param_extra_insert_require(self, entities: List[Entity]) -> List[str]:
        params = []
        for entity in entities:
            for value in entity.__dict__.values():
                if value.is_insert_require:
                    params.append(value.value)

        return params
