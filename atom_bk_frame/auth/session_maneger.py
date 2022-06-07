import random
import string
import datetime
from atom_bk_frame.auth.entities.session_entitiy import SessionEntity
from atom_bk_frame.db.db_accesors.db_accesor import DbAccesor
from atom_bk_frame.util.settings_util import get_member_by_settings


class SessionManeger:
    """セッション管理関連の処理をまとめたクラス
    """

    SESSION_CODE_LEN = 32
    DEFAULT_EXPIRED_DAYS = 31

    def generete_session(self, user_id: int) -> str:
        """新しいセッションを生成します

        Args:
            user_id (int): ユーザID

        Returns:
            str: セッションコード
        """
        session_db_accesor = DbAccesor(SessionEntity)
        session_code = self._create_session_code()
        session_entity = SessionEntity.create_instance(
            user_id=user_id,
            session=session_code,
            expired_at=self._create_expired_datetime()
        )
        session_db_accesor.insert(session_entity)

        return session_code

    def _create_session_code(self,) -> str:
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(self.SESSION_CODE_LEN)]
        return ''.join(randlst)

    def _create_expired_datetime(self,) -> datetime.datetime:
        now = datetime.datetime.now()
        session_expired_days = get_member_by_settings("SESSION_EXPIRED_DAYS")

        return now + \
            datetime.timedelta(days=session_expired_days if session_expired_days is not None else self.DEFAULT_EXPIRED_DAYS)

    @staticmethod
    def generate_set_cookie_syntax(session_code: str) -> str:
        """セッションクッキー文字列を生成します

        Args:
            session_code (str): セッションコード

        Returns:
            str: セッションクッキー文字列
        """
        return "session={0}; Path=/api;SameSite=Strict;HttpOnly".format(session_code)

    @staticmethod
    def generate_delete_cookie_syntax() -> str:
        """削除用セッションクッキー文字列を生成します

        Args:
            session_code (str): セッションコード

        Returns:
            str: 削除用セッションクッキー文字列
        """

        expired_datatime = datetime.datetime.now() - datetime.timedelta(days=1)
        expired_datatime_str = expired_datatime.strftime('%a,%d %b %Y %H:%M:%S GMT')
        return "session={0}; Path=/api;Expires={1};SameSite=Strict;HttpOnly".format("delete", expired_datatime_str)

    @ staticmethod
    def check_epired(expired: datetime.datetime) -> bool:
        """セッションの期限チェック

        Args:
            expired (datetime): セッション日時

        Returns:
            bool: 期限切れ有無
        """
        return expired >= datetime.datetime.now()
