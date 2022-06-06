
from typing import Any, Dict


class BaseValidator:
    """バリデーション基底クラス
    """

    def __init__(self, target: Any) -> None:
        self.target = target
        self._result: Dict = {}
        self.init_validator_items()

    def init_validator_items(self) -> None:
        """バリデーションアイテムの設定

        Raises:
            NotImplementedError: オーバライド未設定例外
        """
        raise NotImplementedError()

    def validate(self) -> bool:
        """バリデーション処理

        Returns:
            bool: バリデーション判定
        """
        return True

    @property
    def result(self):
        """変換処理後のバリデーション対象のオブジェクト

        Returns:
            _type_:バリデーション対象オブジェクト
        """
        return self._result
