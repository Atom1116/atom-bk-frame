
import re
from typing import AnyStr, Pattern
from atom_bk_frame.controller.controller import Controller


class UrlPattern:
    """URLパターンクラス
    """

    def __init__(self, path='/$', controller: Controller = None) -> None:
        self.__path = "^/api" + path
        self.__path_compiled = re.compile(self._exchange_path_query(self.__path))
        self.__controller = controller

    @property
    def path(self,) -> str:
        return self.__path

    @property
    def path_compiled(self,) -> Pattern[AnyStr]:
        return self.__path_compiled

    @property
    def controller(self,) -> Controller:
        return self.__controller

    def _exchange_path_query(self, path: str):
        # TODO:数字のパスパラメータのみ対応している。他のデータ型でも対応できるようにする
        if path.find("<int>") < 0:
            return path

        return path.replace("<int>", "[0-9]+")
