from abc import ABCMeta, abstractclassmethod
from typing import Dict, Tuple
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.response import Response


class MiddlewareProcess:
    """ミドルウェア処理プロセスクラス
    """

    def __init__(self, callback, middleware) -> None:
        """コンストラクタ

        Args:
            callback (function): controllerコールバック
            middleware (_type_): ミドルウェアクラス
        """
        self.callback = callback
        self.middleware: Middleware = middleware

    def get_response_with_middleware_chain(self,
                                           request: Request,
                                           **kwargs) -> Response:
        """ミドルウェア処理を通したレスポンス取得処理
        コンストラクタで設定したミドルウェアクラスの処理を通してレスポンス取得処理を実行する。
        Args:
            request (Request): リクエスト

        Returns:
            Response: レスポンス
        """
        initial_response = None
        response, request, kwargs = self.middleware.get_request_chain(
            initial_response,
            request,
            **kwargs)

        if response is not None:
            return response

        response = self.callback(request, **kwargs)
        return self.middleware.get_response_chain(response)


class Middleware(metaclass=ABCMeta):
    """ミドルウェア抽象基底クラス

    Args:
        metaclass (_type_, optional): Defaults to ABCMeta.
    """

    def set_next_middleware(self, next):
        """チェインするミドルウェア設定

        Args:
            next (function): チェインするミドルウェア

        Returns:
            Middleware : チェイン先のミドルウェア
        """
        self.next: Middleware = next
        return next

    def get_request_chain(self,
                          response: Response,
                          request: Request,
                          **kwargs) -> Tuple[Response, Request, Dict]:
        """リクエスト情報取得チェイン

        Args:
            response (Response): 一時的なレスポンス
            request (Request): リクエスト

        Returns:
            Tuple[Response, Request, Dict]: リクエスト情報
        """
        is_continue, response, request, kwargs = self.request_process(response, request, **kwargs)

        if not is_continue:
            return response, request, kwargs

        if getattr(self, "next", None) is None:
            return response, request, kwargs
        else:
            return self.next.get_request_chain(response, request, **kwargs)

    def get_response_chain(self, response: Response) -> Response:
        """レスポンス情報取得チェイン

        Args:
            response (Response): レスポンス

        Returns:
            Response: レスポンス
        """

        is_continue, response = self.response_process(response)

        if not is_continue or getattr(self, "next", None) is None:
            return response
        else:
            return self.next.get_response_chain(response)

    @abstractclassmethod
    def request_process(self,
                        response: Response,
                        request: Request,
                        **kwargs) -> Tuple[bool, Response, Request, Dict]:
        """リクエスト時のミドルウェア処理

        Args:
            response (Response): 一時リクエスト情報
            request (Request): レスポンス情報

        Returns:
            Tuple[is_continue: bool, Response, Request, Dict]: 続行可否, 一時レスポンス, リクエスト情報
        """
        return True, response, request, kwargs

    @abstractclassmethod
    def response_process(self,
                         response: Response) -> Tuple[bool, Response]:
        """レスポンス時のミドルウェア処理

        Args:
            response (Response): レスポンス

        Returns:
            Tuple[is_continue: bool, Response]: 続行可否, リクエスト
        """
        return True, response
