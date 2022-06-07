from typing import List
from atom_bk_frame.db.db_accesors.base_query_factory import BaseQueryFactory
from atom_bk_frame.db.entities.entity import Entity
from atom_bk_frame.db.entities.items.base_item import BaseItem


class MysqlQueryFactory(BaseQueryFactory):

    select = """
    SELECT
    {items}
    FROM {table_name}
    """

    insert = """
    INSERT INTO {table_name}({items})
    VALUES
    {insert_rows}
    """

    update = """
    UPDATE {table_name} SET {update_cloums}
    WHERE {where_colums}
    """

    delete = """
    DELETE FROM {table_name}
    WHERE {where_colums}
    """

    def create_select_query(self, entity: Entity) -> str:
        items = []
        for key in entity.__dict__.keys():
            items.append(key)
        select_query = self.select.format(
            items=",".join(items),
            table_name=entity.table_name
        )
        return select_query

    def create_select_query_by_id(self, entity: Entity) -> str:
        items = []
        primary_item_key = None
        for key, value in entity.__dict__.items():
            items.append(key)
            if value.is_primary:
                primary_item_key = key

        select_query = self.select.format(
            items=",".join(items),
            table_name=entity.table_name
        )
        if not primary_item_key:
            return select_query
        return select_query + "WHERE {key} = %s".format(key=primary_item_key)

    def create_select_query_by_param(self, entity: Entity, key_names: List) -> str:
        items = []
        for key in entity.__dict__.keys():
            items.append(key)

        select_query = self.select.format(
            items=",".join(items),
            table_name=entity.table_name
        )

        def generate_where_query(key_name):
            return "{key_name} = %({key_name})s".format(key_name=key_name)
        return select_query + \
            "WHERE " + \
            " AND ".join(list(map(generate_where_query, key_names)))

    def create_insert_query(self, entity: Entity, insert_rows_row: int) -> str:

        item_keys = []
        for key, value in entity.__dict__.items():
            if not isinstance(value, BaseItem):
                continue
            if value.is_insert_require:
                item_keys.append(key)

        insert_row = "(" + ",".join(["%s" for _ in range(len(item_keys))]) + ")"

        return self.insert.format(
            table_name=entity.table_name,
            items=",".join(item_keys),
            insert_rows=",".join([insert_row for _ in range(insert_rows_row)])
        )

    def create_update_query_by_id(self, entity: Entity) -> str:
        update_cloums = []
        where_colums = []
        for key, value in entity.__dict__.items():
            if not value.is_primary and value.is_insert_require:
                update_cloums.append(key)

            if value.is_primary:
                where_colums.append(key)

        return self.update.format(
            table_name=entity.table_name,
            update_cloums=",".join(["{}=%s".format(colum) for colum in update_cloums]),
            where_colums=" AND ".join(["{}=%s".format(colum) for colum in where_colums])
        )

    def create_delete_query_by_id(self, entity: Entity) -> str:
        update_cloums = []
        where_colums = []
        for key, value in entity.__dict__.items():
            if not value.is_primary and value.is_insert_require:
                update_cloums.append(key)

            if value.is_primary:
                where_colums.append(key)

        return self.delete.format(
            table_name=entity.table_name,
            where_colums=" AND ".join(["{}=%s".format(colum) for colum in where_colums])
        )
