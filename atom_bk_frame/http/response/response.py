from http.client import responses as http_responses
from typing import Dict, cast
from wsgiref.headers import Headers


class Response:
    """HTTPレスポンスクラス

    Returns:
        _type_: HTTPレスポンス情報
    """
    default_status = "200"
    default_charset = 'utf-8'
    default_content_type = 'text/html; charset=UTF-8'

    def __init__(self, body='', status=None, headers=None, charset=None):
        """コンストラクタ

        Args:
            body (str, optional): ボディ. Defaults to ''.
            status (_type_, optional): ステータス. Defaults to None.
            headers (_type_, optional): ヘッダー. Defaults to None.
            charset (_type_, optional): エンコード. Defaults to None.
        """
        self._body = body
        self.status = status or self.default_status
        self.headers = Headers()
        self.charset = charset or self.default_charset

        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)

    @property
    def status_code(self):
        """ステータスコード

        Returns:
            _type_: ステータスコード
        """
        return "%d %s" % (cast(int, self.status), http_responses[cast(int, self.status)])

    @property
    def header_list(self):
        """ヘッダーリスト

        Returns:
            _type_: ヘッダー情報のリスト
        """
        if 'Content-Type' not in self.headers:
            self.headers.add_header('Content-Type', self.default_content_type)
        return self.headers.items()

    @property
    def body(self):
        """ボディ

        Returns:
            _type_: エンコード済みのボディ
        """
        if isinstance(self._body, str):
            return self._body.encode(self.charset)
        return self._body

    def set_cookie(self, item: str) -> None:
        """set-cookie設定

        Args:
            cookies (Dict): クッキー情報
        """
        self.headers.add_header('Set-Cookie', item)

    def add_headers(self, headers: Dict) -> None:
        """ヘッダー追加

        Args:
            headers (Dict): ヘッダー辞書
        """
        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)
