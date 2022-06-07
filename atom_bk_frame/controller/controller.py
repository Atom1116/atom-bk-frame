import re
from typing import Dict, Tuple, Callable
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.http_error_response import Response405, get_405_callback
from atom_bk_frame.http.response.response import Response


class Controller:
    """アプリケーション実行処理操作クラス

    Returns:
        _type_: _description_
    """
    http_methods = ["GET", "POST", "PUT", "DELETE"]

    def dispatch(self, request: Request) -> Tuple[Callable, Dict]:
        handler = self.get

        if request.method in self.http_methods:
            handler = self.get_mehod_callback(request.method.lower())
        else:
            return get_405_callback(), {}

        argument = self.get_argument(request)

        return handler, argument

    def get_argument(self, request: Request) -> Dict:
        """リクエストからコントローラへ渡す引数値を取得します

        Args:
            request (Request): リクエスト

        Returns:
            Dict: リクエストからコントローラへ渡す引数値
        """

        # urlパラメータの取得
        # TODO:intのみ対応している。他のデータ型も対応する。
        if not request.url_path.find("<int>"):
            return {}

        return {
            "url_path_param": re.findall(r'[0-9]+', request.path)
        }

    def get_mehod_callback(self, method: str) -> Callable:
        return getattr(self, method, get_405_callback())

    def get(self, request: Request, **kwargs) -> Response:
        return Response405()

    def post(self, request: Request, **kwargs) -> Response:
        return Response405()

    def put(self, request: Request, **kwargs) -> Response:
        return Response405()

    def delete(self, request: Request, **kwargs) -> Response:
        return Response405()
