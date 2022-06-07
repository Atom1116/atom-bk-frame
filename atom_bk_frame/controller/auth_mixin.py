

from typing import Callable, Dict
from urllib.request import Request
from atom_bk_frame.auth.entities.auth_user_entity import AuthUserEntity
from atom_bk_frame.http.response.http_error_response import Response401, Response403, get_405_callback
from atom_bk_frame.http.response.response import Response


class AuthMixin:
    """認証Mixin
    コントローラで処理する認証処理メソッドを定義するMixinです、
    """

    is_admin = False

    def get_mehod_callback(self, method: str) -> Callable:
        return getattr(self, method + "_auth", get_405_callback())

    def get_auth(self, request: Request, **kwargs) -> Response:
        if not self.validate_authorized(kwargs):
            return Response401()

        if not self.validate_forbidden(kwargs):
            return Response403()

        response = self.get(request, **kwargs)
        return response

    def post_auth(self, request: Request, **kwargs) -> Response:
        if not self.validate_authorized(kwargs):
            return Response401()

        if not self.validate_forbidden(kwargs):
            return Response403()
        response = self.post(request, **kwargs)
        return response

    def put_auth(self, request: Request, **kwargs) -> Response:
        if not self.validate_authorized(kwargs):
            return Response401()

        if not self.validate_forbidden(kwargs):
            return Response403()
        response = self.put(request, **kwargs)
        return response

    def delete_auth(self, request: Request, **kwargs) -> Response:
        if not self.validate_authorized(kwargs):
            return Response401()

        if not self.validate_forbidden(kwargs):
            return Response403()
        response = self.delete(request, **kwargs)
        return response

    def validate_authorized(self, kwargs: Dict) -> bool:
        # ユーザ情報の有無チェック
        user_entity = kwargs.get('user')
        if not user_entity:
            return False

        return isinstance(user_entity, AuthUserEntity)

    def validate_forbidden(self, kwargs: Dict) -> bool:
        # 管理者のみ発火可能なコントローラであるかの判定
        if not self.is_admin:
            return True
        user_entity: AuthUserEntity = kwargs.get('user')
        return user_entity.is_admin.value
