from atom_bk_frame.auth.entities.auth_user_entity import AuthUserEntity
from atom_bk_frame.auth.entities.session_entitiy import SessionEntity
from atom_bk_frame.auth.session_maneger import SessionManeger
from atom_bk_frame.controller.auth_mixin import AuthMixin
from atom_bk_frame.controller.controller import Controller
from atom_bk_frame.db.db_accesors.db_accesor import DbAccesor
from atom_bk_frame.http.request import Request
from atom_bk_frame.http.response.response import Response


class SignOutController(AuthMixin, Controller):
    """セッション削除コントローラ

    Args:
        Controller (_type_): コントローラ基底クラス
    """

    def post(self, request: Request, user: AuthUserEntity, **kwargs) -> Response:

        session_db_accesor = DbAccesor(SessionEntity)
        delete_session_entities = session_db_accesor.select_by_param(param={
            'user_id': user.user_id.value
        })

        if len(delete_session_entities) <= 0:
            return Response(status='202')

        effected_rows_count = session_db_accesor.delete_bulk(delete_session_entities)

        if effected_rows_count <= 0:
            return Response(status='202')

        response = Response(status="200", )

        session_maneger = SessionManeger()
        response.set_cookie(session_maneger.generate_delete_cookie_syntax())
        return response
