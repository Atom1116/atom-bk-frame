class BaseItem:

    _value = None
    _default_value = None
    _is_primary = False
    _is_insert_require = True

    def __init__(self, is_praimary=False, is_insert_require=True) -> None:
        self._is_primary = is_praimary
        self._is_insert_require = is_insert_require

    @property
    def value(self,):
        return self._value

    @property
    def to_dict_value(self,):
        return self._value

    @property
    def is_primary(self):
        return self._is_primary

    @property
    def is_insert_require(self):
        return self._is_insert_require

    def set_value(self, value):
        self._value = value
