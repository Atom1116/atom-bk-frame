from todo_scratch.bk_base.db.entities.entity import Entity
from todo_scratch.bk_base.db.entities.items import items


class AuthUserEntity(Entity):

    def __init__(self) -> None:
        self.user_id = items.IntItem(is_praimary=True, is_insert_require=False)
        self.user_name = items.CharItem(length=30)
        self.email = items.CharItem(length=50)
        self.password = items.CharItem(length=100)
        self.is_admin = items.BoolItem()
        self.created_at = items.DatetimeItem(is_insert_require=False)
        self.updated_at = items.DatetimeItem(is_insert_require=False)
        super().__init__()

    def set_entity_values(self, user_name, email, password, is_admin):
        self.user_name.set_value(user_name)
        self.email.set_value(email)
        self.password.set_value(password)
        self.is_admin.set_value(is_admin)
