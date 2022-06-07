import base64
import hashlib
from atom_bk_frame.util.settings_util import get_member_by_settings


class EncryptManeger:
    """暗号化マネージャークラス
    """

    @staticmethod
    def get_hash(password_origin: str) -> str:
        """パスワードをハッシュ化します

        Args:
            password_origin (str): オリジナルパスワード

        Returns:
            str: ハッシュ化したパスワード
        """
        password = bytes(password_origin, 'utf-8')
        secret_key = get_member_by_settings("SECRET_KEY")
        if secret_key is None:
            raise Exception()
        hash = hashlib.sha256(base64.b64encode(secret_key.encode()) + password).hexdigest()
        return hash
