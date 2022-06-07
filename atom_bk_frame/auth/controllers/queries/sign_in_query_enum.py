from enum import Enum

class SignInQueryEnum(Enum):
    MYSQL = """
        SELECT
            user_id,
            user_name,
            email,
            `password`,
            created_at,
            updated_at
        FROM todo_scratch.`user`
        WHERE(user_name = %(user_name)s OR email = %(email)s)
        AND `password` = %(password)s
    """

    @staticmethod
    def get_value(id) -> str:
        if id == SignInQueryEnum.MYSQL.name:
            return SignInQueryEnum.MYSQL.value
        return ""
