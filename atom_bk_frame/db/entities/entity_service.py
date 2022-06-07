from typing import Dict, List
from atom_bk_frame.db.entities.entity import Entity
from atom_bk_frame.util.class_loader_util import get_module_by_route


class EntityService:
    """エンティティ処理サービス
    エンティティのサービス処理をまとめたクラスです
    """

    def __init__(self, entity_module: type) -> None:
        self.entity_module: type = entity_module

    def create_entity_list(self, rows: List[Dict]) -> List:
        """クエリ結果からエンティティのリストを作成します

        Args:
            rows (List[Dict]): クエリ結果

        Returns:
            List: エンティティリスト
        """
        entities = []
        for row in rows:
            entity_module: type = get_module_by_route(
                self.entity_module.__name__,
                self.entity_module.__module__
            )
            entity: Entity = entity_module()
            entity.set_values_by_row(row)
            entities.append(entity)
        return entities
