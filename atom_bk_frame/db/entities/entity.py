from typing import Dict, List
from todo_scratch.bk_base.db.entities.items.base_item import BaseItem


class Entity:

    table_name = None

    def to_dict(self) -> Dict:
        result: Dict = {}
        for key, item in self.__dict__.items():
            if not isinstance(item, BaseItem):
                continue
            result[key] = item.to_dict_value

        return result

    def set_values_by_row(cls, row: Dict):
        """Queryの結果をentityへ設定
        """
        for key, value in row.items():
            item = getattr(cls, key, None)
            if not item or not isinstance(item, BaseItem):
                continue
            item.set_value(value)

    def validate(self,):
        pass

    def count_is_insert_required_item(self,):
        """更新時に必須なカラム数を返します

        Returns:
            _type_: カラム数
        """
        count = 0
        for value in self.__dict__.values():
            if not hasattr(value, "is_insert_require"):
                continue
            if value.is_insert_require:
                count += 0
        return count

    def get_is_insert_required_items(self,) -> List:
        """更新時に必須なカラムの値を返します

        Returns:
            List: カラム値リスト
        """

        items = []
        for value in self.__dict__.values():
            if not hasattr(value, "is_insert_require"):
                continue
            if value.is_insert_require:
                items.append(value.value)
        return items

    def get_primary_colums(self,) -> List[str]:
        """主キーのカラムを取得します

        Returns:
            List[str]: 主キーのカラムリスト
        """
        primary_colums = []
        for key, value in self.__dict__.items():
            if not hasattr(value, "is_primary"):
                continue
            if value.is_primary:
                primary_colums.append(key)
        return primary_colums

    def get_primary_colum_values(self,) -> List:
        """主キーのカラムを取得します

        Returns:
            List[str]: 主キーのカラムリスト
        """
        primary_colums_values = []
        for value in self.__dict__.values():
            if not hasattr(value, "is_primary"):
                continue
            if value.is_primary:
                primary_colums_values.append(value.value)
        return primary_colums_values
