from enum import Enum
from atom_bk_frame.util.settings_util import get_module_path_by_settings

class SignInQueryEnum(Enum):
    MYSQL = """
        SELECT
            user_id,
            user_name,
            email,
            `password`,
            created_at,
            updated_at
        FROM {db_name}.`user`
        WHERE(user_name = %(user_name)s OR email = %(email)s)
        AND `password` = %(password)s
    """

    @staticmethod
    def get_value(id) -> str:
        if id == SignInQueryEnum.MYSQL.name:
            return SignInQueryEnum.MYSQL.value.format(get_module_path_by_settings("DB_NAME"))
        return ""
