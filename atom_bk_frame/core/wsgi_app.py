
import typing as t
from todo_scratch.bk_base.core.router import Router
from todo_scratch.bk_base.http.request import Request
from todo_scratch.bk_base.http.response.response import Response
from todo_scratch.bk_base.core.middleware import Middleware, MiddlewareProcess
from todo_scratch.bk_base.util.class_loader_util import get_module_by_full_route
from todo_scratch.bk_base.util.settings_util import get_member_by_settings


class WsgiApp:
    """WSGIアプリケーションメインクラス
    """

    def __init__(self) -> None:
        self.router = Router()
        self.middleware = self._load_middleware()

    def wsgi_process(self, env: dict, start_response: t.Callable) -> t.Any:
        """WSGIアプリケーションメイン処理

        Args:
            env (dict): 環境変数
            start_response (t.Callable): HTTP応答メソッド

        Returns:
            t.Any: リクエストボディ
        """
        # レスポンスの取得
        request = Request(env)
        # メソッド、URLパスからコールバック、引数を取得
        callback, kwargs = self.router.match(request)
        # ミドルウェア処理を定義
        middleware_process: MiddlewareProcess = MiddlewareProcess(
            callback, self.middleware
        )
        # コールバックからレスポンスを取得
        response: Response = \
            middleware_process.get_response_with_middleware_chain(request, **kwargs)

        return self._create_wsgi_response(start_response, response)

    def _load_middleware(self,) -> Middleware:
        middlewares_str: t.List[str] = get_member_by_settings("MIDDLEWARES")
        middlewares = []
        for middleware in middlewares_str:
            middlewares.append(get_module_by_full_route(middleware)())
        if len(middlewares) <= 0:
            return None

        base_middleware = middlewares[0]

        if len(middleware) > 1:
            next_middleware: Middleware = base_middleware
            for middleware in middlewares[1:]:
                next_middleware = next_middleware.set_next_middleware(middleware)

        return base_middleware

    def _create_wsgi_response(self, start_response: t.Callable, response: Response) -> t.Any:
        # レスポンスからステータス、ヘッダーを設定
        start_response(response.status, response.header_list)
        # レスポンスボディを返す
        return [response.body]

    def __call__(self, env: dict, start_response: t.Callable) -> t.Any:
        return self.wsgi_process(env, start_response)
