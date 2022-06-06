from typing import Dict, Tuple
from todo_scratch.bk_base.http.request import Request
from todo_scratch.bk_base.http.response.response import Response
from todo_scratch.bk_base.core.middleware import Middleware
from todo_scratch.bk_base.util.log.log_util import get_main_logger


class HttpLogMiddleware(Middleware):
    """HTTP通信のロギング処理ミドルウェア
    アプリケーションのHTTP処理にまつわるロギング処理を実行します。

    Args:
        Middleware (_type_): ミドルウェア基底クラス
    """

    REQUEST_MESSAGE_FORMAT = "{server_protocol} {method} {path}"

    def request_process(self,
                        response: Response,
                        request: Request,
                        **kwargs) -> Tuple[bool, Response, Request, Dict]:
        get_main_logger().info(self.REQUEST_MESSAGE_FORMAT.format(
            server_protocol=request.server_protocol,
            method=request.method,
            path=request.server_name + request.path
        ))
        return True, response, request, kwargs

    def response_process(self,
                         response: Response) -> Tuple[bool, Response]:
        return True, response
