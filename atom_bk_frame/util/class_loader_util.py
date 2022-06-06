import sys
from importlib import import_module
from importlib.abc import MetaPathFinder
from importlib.util import spec_from_file_location
from typing import Any


def get_module_by_full_route(route: str) -> Any:
    """連結したモジュールルートから動的にモジュールをimportし、メンバーを取得します。

    Args:
        route (str): 連結したモジュールルート

    Returns:
        Any: モジュールメンバー
    """
    last_sepalation_index = route.rfind(".")
    if last_sepalation_index < 0:
        raise Exception()

    import_module_route = route[:last_sepalation_index]
    member_name = route[last_sepalation_index + 1:]

    return get_module_by_route(member_name, import_module_route)


def get_module_by_route(module_name: str, route: str) -> Any:
    """モジュールルートから動的にモジュールをimportし、メンバーを取得します

    Args:
        module_name (str): メンバー変数名
        route (str): ルート

    Returns:
        Any: メンバー
    """
    module = import_module(route)
    member = getattr(module, module_name, None)
    return member


def get_module_by_file_path(name, location):
    """ファイルパスから動的にモジュールをimportします

    Args:
        name (_type_): importモジュール名
        location (_type_): ファイルパス

    Returns:
        _type_: importモジュール
    """
    class Finder(MetaPathFinder):
        @staticmethod
        def find_spec(fullname, *_):
            if fullname == name:
                return spec_from_file_location(name, location)

    finder = Finder()
    sys.meta_path.insert(0, finder)
    try:
        return import_module(name)
    finally:
        sys.meta_path.remove(finder)
