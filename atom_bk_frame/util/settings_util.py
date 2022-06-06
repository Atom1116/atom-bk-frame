

import os
from importlib import import_module
from typing import Any, cast

MEMBER_APP_PATH = "APP_PATH"


def get_settings():
    """設定ファイルを取得します

    Raises:
        FileNotFoundError: _description_

    Returns:
        _type_: 設定ファイルモジュール
    """
    settings_path = os.environ.get('SETTINGS_PATH', None)
    if not settings_path:
        raise FileNotFoundError
    settings_module = import_module(cast(str, settings_path))

    return settings_module


def get_member_by_settings(member_name: str) -> Any:
    """設定ファイルから指定したメンバーを取得します

    Args:
        member_name (str): メンバー変数名

    Returns:
        Any: メンバー
    """
    settings = get_settings()
    return getattr(settings, member_name, None)


def get_module_path_by_settings(member_name: str) -> Any:
    """設定ファイルからモジュールパス文字列を返します

    Args:
        member_name (str): メンバー変数名

    Returns:
        Any: モジュールパス文字列
    """
    settings = get_settings()

    return ".".join(
        [getattr(settings, MEMBER_APP_PATH), getattr(settings, member_name)]
    )
