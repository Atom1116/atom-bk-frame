import typing as t
from atom_bk_frame.core.url_pattern import UrlPattern
from atom_bk_frame.http.response.http_error_response import get_404_callback
from atom_bk_frame.http.request import Request
from atom_bk_frame.util.settings_util import get_member_by_settings, get_module_path_by_settings
from atom_bk_frame.util.class_loader_util import get_module_by_route


class Router:
    """ルータークラス

    Returns:
        _type_: _description_
    """

    URL_PATTERN = "urlpatterns"
    AUTH_URL_PATTERN = "auth_urlpatterns"

    def __init__(self) -> None:
        self.urlpatterns: t.List[UrlPattern] = []
        self.load_routes()
        self.load_auth_routes()

    def load_routes(self,) -> None:
        self.urlpatterns = get_module_by_route(
            self.URL_PATTERN,
            get_module_path_by_settings("URLS_PATH")
        )

    def load_auth_routes(self,) -> None:
        auth_user_entity = get_member_by_settings("AUTH_USER_ENTITY")

        if auth_user_entity is None:
            return
        auth_urlpatterns = get_module_by_route(
            self.AUTH_URL_PATTERN,
            "todo_scratch.bk_base.auth.controllers.auth_urls"
        )
        self.urlpatterns.extend(auth_urlpatterns)

    def match(self, request: Request) -> t.Tuple[t.Callable, dict]:
        """Urlの照合

        Args:
            method (str): メソッド
            path (str): Urlパス

        Returns:
            t.Tuple[t.Callable, dict]: wsgiレスポンスコールバック
        """
        for urlpattern in self.urlpatterns:
            matchd = urlpattern.path_compiled.match(request.path)
            if not matchd:
                continue
            request.set_url_path(urlpattern.path)
            return urlpattern.controller.dispatch(request)

        return get_404_callback()
