from typing import Dict
from todo_scratch.bk_base.validator.base_validator import BaseValidator
from todo_scratch.bk_base.validator.validator_item import ValidatorItem


class JsonValidator(BaseValidator):
    """Jsonバリデーションクラス

    Args:
        BaseValidator (_type_): バリデーション基底クラス
    """

    def validate(self):
        self._result: Dict = {}

        for key, value in self.__dict__.items():
            if not isinstance(value, ValidatorItem):
                continue

            validator: ValidatorItem = value
            target_item = self.target.get(key, None)

            if not validator.execute_validate(target_item):
                return False

        self._convert_when_success_validate()

        return True

    def _convert_when_success_validate(self) -> None:
        for key, value in self.__dict__.items():
            if not isinstance(value, ValidatorItem):
                continue

            validator: ValidatorItem = value
            target_item = self.target.get(key)

            if target_item is None:
                continue

            self._result[key] = validator.convert(target_item)

    @property
    def result(self):
        return self._result
