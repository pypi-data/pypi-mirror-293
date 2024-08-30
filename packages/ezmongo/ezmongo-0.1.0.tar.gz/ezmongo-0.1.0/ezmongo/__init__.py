from pymongo import MongoClient
from pymongo.database import Collection, Database as MongoDB
from typing import Callable, Type, TypeVar, Generic
from pydantic import BaseModel, computed_field
from secrets import token_urlsafe


IdT = TypeVar("IdT", str, int)


class IdAlreadyExisting(NameError):
    ...



class TableObject(BaseModel):
    __table: "Table"
    object_id: str | None

    @computed_field
    @property
    def id(self) -> IdT:
        if self.__table.id_key:
            return self.__getattribute__(self.__table.id_key)
        else:
            return self.object_id



T = TypeVar('T', bound=TableObject)



class Table(Generic[T]):

    def __init__(self,
                 db: "Database",
                 name: str,
                 klass: Type[T],
                 id_key: str | None) -> None:
        self.db = db
        self.name = name
        self.klass = klass
        self.id_key = id_key


    def __call__(self, *args, **kwargs) -> T:
        if not self.id_key:
            if not "object_id" in kwargs:
                kwargs["object_id"] = token_urlsafe(8)
        return self.klass(*args, **kwargs)


    @property
    def client_coll(self) -> Collection:
        return self.db.client_db.get_collection(self.name)


    def push(self, obj: T) -> None:
        existing_id = self.get(obj.id)
        if existing_id:
            raise IdAlreadyExisting(f"an object with ID {repr(obj.id)} already exists")
        self.db.table_push(self, obj)


    def update(self, obj: T) -> None:
        self.db.table_update(self, obj)


    def remove(self, obj: T) -> None:
        self.db.table_remove(self, obj)


    def find(self, filter: dict[str], limit: int = 0) -> list[T]:
        return self.db.table_find(self, filter, limit=limit)


    def get(self, id: str) -> T | None:
        res = self.find({"id": id})
        if not res:
            return
        return self.klass.model_validate(res[0])


    __getitem__ = get



class Database:

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url
        self.tables: list[Table] = []


    @property
    def client_db(self) -> MongoDB:
        return MongoClient(self.url).get_database(self.name)


    def CreateTable(self,
                    name: str,
                    id_key: str | None = None) -> Callable[[Type[T]], Table[T]]:
        def decorator(klass: Type[T]) -> Table[T]:
            table = Table(self, name, klass, id_key)
            self.tables.append(table)
            return table
        return decorator


    def table_push(self, table: Table[T], obj: T) -> None:
        coll = self.client_db.get_collection(table.name)
        coll.insert_one(obj.model_dump())


    def table_update(self, table: Table[T], obj: T) -> None:
        coll = self.client_db.get_collection(table.name)
        coll.update_one({"id": obj.id}, {"$set": obj.model_dump()})


    def table_remove(self, table: Table[T], obj: T) -> None:
        coll = self.client_db.get_collection(table.name)
        coll.delete_one({"id": obj.id})


    def table_find(self,
                   table: Table[T],
                   filter: dict[str],
                   limit: int = 0) -> list[T]:
        coll = self.client_db.get_collection(table.name)
        res = coll.find(filter, limit=limit)
        return [table.klass.model_validate(data) for data in res]