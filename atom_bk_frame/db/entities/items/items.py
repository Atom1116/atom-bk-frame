import datetime
from atom_bk_frame.db.entities.items.base_item import BaseItem


class CharItem(BaseItem):
    def __init__(self, length=0, is_praimary=False, is_insert_require=True) -> None:
        self.length = length
        super().__init__(is_praimary, is_insert_require)


class VcharItem(BaseItem):
    pass


class TextItem(BaseItem):
    pass


class IntItem(BaseItem):
    pass


class BoolItem(BaseItem):
    pass


class DatetimeItem(BaseItem):
    def set_value(self, value):
        if isinstance(value, str):
            value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        self._value = value

    @property
    def to_str(self,):
        return self._value.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def to_dict_value(self,):
        return self._value.strftime('%Y-%m-%d %H:%M:%S')
