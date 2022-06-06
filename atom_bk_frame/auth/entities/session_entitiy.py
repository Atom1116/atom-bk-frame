from todo_scratch.bk_base.db.entities.entity import Entity
from todo_scratch.bk_base.db.entities.items import items


class SessionEntity(Entity):
    table_name = "session"

    def __init__(self) -> None:
        self.session_id = items.IntItem(is_praimary=True, is_insert_require=False)
        self.user_id = items.IntItem()
        self.session = items.CharItem(length=100)
        self.expired_at = items.DatetimeItem()
        self.created_at = items.DatetimeItem(is_insert_require=False)
        self.updated_at = items.DatetimeItem(is_insert_require=False)
        super().__init__()

    def set_entity_values(self, user_id, session, expired_at):
        self.user_id.set_value(user_id)
        self.session.set_value(session)
        self.expired_at.set_value(expired_at)

    @staticmethod
    def create_instance(user_id, session, expired_at):
        entity = SessionEntity()
        entity.set_entity_values(user_id, session, expired_at)
        return entity
