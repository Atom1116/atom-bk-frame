import cgi
import json
import urllib.parse


class Request:
    """HTTPリクエストクラス
    """

    def __init__(self, environ, charset='utf-8'):
        """コンストラクタ

        Args:
            environ (_type_): wsgi environ
            charset (str, optional): エンコード. Defaults to 'utf-8'.
        """
        self.environ = environ
        self._body = None
        self.charset = charset
        self._url_path = '/'

    def set_url_path(self, url_path: str):
        self._url_path = url_path

    @property
    def url_path(self):
        return self._url_path

    @property
    def path(self):
        return self.environ['PATH_INFO'] or '/'

    @property
    def server_name(self):
        return self.environ['SERVER_NAME']

    @property
    def server_protocol(self):
        return self.environ['SERVER_PROTOCOL']

    @property
    def method(self):
        return self.environ['REQUEST_METHOD'].upper()

    @property
    def path_query(self):
        return urllib.parse.parse_qs(self.environ['QUERY_STRING'])

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            self._body = self.environ['wsgi.input'].read(content_length)
        return self._body

    @property
    def text(self):
        return self.body.decode(self.charset)

    @property
    def json(self):
        return json.loads(self.body)

    @property
    def multipart_form(self):
        form = cgi.FieldStorage(fp=self.environ['wsgi.input'], environ=self.environ)
        return form

    @property
    def content_type(self):
        return self.environ['CONTENT_TYPE']

    @property
    def x_www_form_urlencoded(self):
        data = urllib.parse.parse_qs(self.body.decode())
        return data

    @property
    def cookie(self):
        if "HTTP_COOKIE" not in self.environ:
            return None
        data = urllib.parse.parse_qs(self.environ["HTTP_COOKIE"])
        return data
