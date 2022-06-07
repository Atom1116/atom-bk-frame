from typing import Any, Callable, List
from atom_bk_frame.validator.base_validator import BaseValidator


class ValidatorItem:
    """バリデーションアイテム基底クラス
    """

    def __init__(self, is_required=False) -> None:
        self.is_required = is_required

        def none_callback(value: Any) -> bool:
            return True
        self.validate_callback: Callable[[Any], bool] = none_callback

    def set_validate_callback(self, validate_callback: Callable[[Any], bool]) -> None:
        """カスタマイズ用バリデーションコールバックの設定

        Args:
            validate_callback (Callable[[Any], bool]): バリデーションコールバック
        """
        self.validate_callback = validate_callback

    def execute_validate(self, value: Any) -> bool:
        """バリデーション処理

        Args:
            value (Any): バリデーション対象オブジェクト

        Returns:
            bool: バリデーション結果
        """
        if self.is_required:
            if value is None:
                return False

        if not self.validate(value):
            return False

        return self.validate_callback(value)

    def validate(self, value: Any) -> bool:
        """アイテム独自のバリデーション処理

        Args:
            value (Any): バリデーション対象オブジェクト

        Returns:
            bool: バリデーション結果
        """
        return True

    def convert(self, value: Any) -> Any:
        """バリデーション対象オブジェクトのバリデーション後の変換処理

        Args:
            value (Any): バリデーション対象オブジェクト

        Returns:
            Any: 返還後オブジェクト
        """
        return value


class VcharValidatorItem(ValidatorItem):
    """文字列用バリデーションアイテム

    Args:
        ValidatorItem (_type_): バリデーションアイテム基底クラス
    """

    def convert(self, value: Any):
        if not isinstance(value, str):
            return str(value)
        return value

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)


class TextValidatorItem(ValidatorItem):
    pass


class IntValidatorItem(ValidatorItem):
    pass


class BoolValidatorItem(ValidatorItem):
    pass


class DatetimeValidatorItem(ValidatorItem):
    pass


class ObjectValidatorItem(ValidatorItem):
    pass


class ListValidatorItem(ValidatorItem):
    def __init__(self, validator_type: type, is_required=False) -> None:
        self.validator: type = validator_type
        self.validator_validated_list: List[BaseValidator] = []
        super().__init__(is_required)

    def validate(self, list: List) -> bool:
        self.validator_validated_list = []
        if list is None or len(list) <= 0:
            return True

        for object in list:
            validator: BaseValidator = self.validator(object)

            if not validator.validate():
                return False

            self.validator_validated_list.append(validator)

        return True

    def convert(self, list: List) -> Any:

        if len(self.validator_validated_list) <= 0:
            raise Exception('not validated before convert')

        result = []
        for validator in self.validator_validated_list:
            result.append(validator.result)

        return result
