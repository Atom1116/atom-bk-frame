from abc import ABCMeta, abstractclassmethod
import logging
import os
import sys
from typing import List
from todo_scratch.bk_base.util.file_util import create_dir
from todo_scratch.bk_base.util.settings_util import get_member_by_settings


def get_main_logger() -> logging.Logger:
    """Mainロガーを取得します

    Returns:
        logging.Logger: Mainロガー
    """
    return get_logger('main')


def get_logger(logging_name) -> logging.Logger:
    """指定したロガー名のロガーを取得します

    Args:
        logging_name (_type_): ロガー名

    Returns:
        logging.Logger: ロガー
    """
    logger_maneger = LoggerManeger()
    return logger_maneger.get_logger_by_logger_name(logging_name).logger


class LoggerManeger:
    """ロガー管理クラス
    """
    __logger_maneger = None
    _logger_list: List = []

    def __new__(cls, *args, **kwargs):
        if cls.__logger_maneger is None:
            cls.__logger_maneger = super(LoggerManeger, cls).__new__(cls)
            cls.__logger_maneger._init_logger_list()
        return cls.__logger_maneger

    def _init_logger_list(self) -> None:
        """ローガーリストの初期化処理
        ロガー管理クラスで管理するロガーを追加
        2022/4時点では、mainロガーのみをセット。他にロガーを追加する場合は、ここで設定する。
        """
        self._logger_list.append(
            MainLogger('main')
        )

    def get_logger_by_logger_name(self, logger_name):
        """指定した名称のロガーを取得します

        Args:
            logger_name (_type_): ロガー名

        Returns:
            _type_: ロガー
        """
        for logger in self._logger_list:
            if logger.logger_name == logger_name:
                return logger

        return None


class Logger(metaclass=ABCMeta):
    """ロガー基底クラス

    Args:
        metaclass (_type_, optional):  Defaults to ABCMeta.
    """

    def __init__(self, logger_name) -> None:
        self._logger_name = logger_name
        self._logger = self.create_logger()

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def logger_name(self,) -> str:
        return self._logger_name

    @abstractclassmethod
    def create_logger(self,) -> logging.Logger:
        """ロガーを作成します
        Raises:
            NotImplementedError: _description_

        Returns:
            logging.Logger: ロガー
        """
        raise NotImplementedError


class MainLogger(Logger):
    """メイン処理のロガークラス

    Args:
        Logger (_type_): ロガー基底クラス
    """
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    LOG_DIR_NAME = "log"
    LOG_FILE_NAME = 'main.log'
    LOG_FILE_ENCORD = "utf-8"

    def __init__(self, logger_name) -> None:
        create_dir('/'.join([
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            self.LOG_DIR_NAME
        ]))
        super().__init__(logger_name)

    def create_logger(self,):
        logger = logging.getLogger(self._logger_name)
        fmt = logging.Formatter(self.LOG_FORMAT, self.LOG_DATE_FORMAT)
        handler1 = logging.StreamHandler(sys.stdout)
        handler1.setFormatter(fmt)
        handler2 = logging.FileHandler(filename='/'.join(
            [
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                self.LOG_DIR_NAME,
                self.LOG_FILE_NAME
            ]), encoding=self.LOG_FILE_ENCORD
        )
        handler2.setFormatter(fmt)
        logger.addHandler(handler1)
        logger.addHandler(handler2)
        logger.setLevel(logging.DEBUG if get_member_by_settings("IS_DEBUG") else logging.INFO)
        return logger
