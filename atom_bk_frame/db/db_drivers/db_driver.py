
from abc import ABCMeta, abstractclassmethod
from typing import Dict

from todo_scratch.bk_base.db.db_accesors.base_query_factory import BaseQueryFactory


class DbDriver(metaclass=ABCMeta):

    @abstractclassmethod
    def __enter__(self,):
        pass

    @abstractclassmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get_query_factory(self) -> BaseQueryFactory:
        pass

    @abstractclassmethod
    def connect(self, is_transaction=False):
        pass

    @abstractclassmethod
    def disconnect(self,):
        pass

    @abstractclassmethod
    def commit(self,):
        pass

    @abstractclassmethod
    def rollback(self):
        pass

    @abstractclassmethod
    def is_connect(self,) -> bool:
        pass

    @abstractclassmethod
    def fetch(self, query: str) -> Dict:
        pass

    @abstractclassmethod
    def fetch_with_param(self, query: str, param) -> Dict:
        pass

    @abstractclassmethod
    def execute(self, query: str, param) -> int:
        pass

    @abstractclassmethod
    def execute_bulk(self, query: str, param) -> int:
        pass
