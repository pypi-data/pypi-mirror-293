from typing import Dict, Union
from pymongo import MongoClient
from .lazy_database import LazyDatabase
from pymongo.typings import _Pipeline
import fun_things.logger

try:
    from simple_chalk import chalk
except:
    from fun_things.not_chalk import NotChalk

    chalk = NotChalk()


class LazyMongo:
    def __init__(self):
        self.mongo: MongoClient = None  # type: ignore
        self.default_database: str = None  # type: ignore
        self.default_collection: str = None  # type: ignore
        self.logger = fun_things.logger.new("LazyMongo")

    def _log_info(
        self,
        operation: str,
        message,
    ):
        self.__log(
            self.logger.info,
            operation,
            message,
        )

    def _log_warn(
        self,
        operation: str,
        message,
    ):
        self.__log(
            self.logger.warning,
            operation,
            message,
        )

    def _log_error(
        self,
        operation: str,
        message,
    ):
        self.__log(
            self.logger.error,
            operation,
            message,
        )

    def __log(
        self,
        fn,
        operation: str,
        message: str,
    ):
        operation = chalk.gray.dim(operation)

        if message:
            return fn(
                "<%s> %s",
                operation,
                chalk.white(message),
            )

        return fn(operation)

    def connect(self, uri_or_client: Union[str, MongoClient]):
        if isinstance(uri_or_client, MongoClient):
            self.mongo = uri_or_client
            return self

        try:
            self.mongo = MongoClient(uri_or_client)
        except:
            pass

        return self

    def __getitem__(self, key: str):
        return LazyDatabase(
            mongo=self,
            database=self.mongo[key or self.default_database],
            default_collection_name=self.default_collection,
        )

    def find_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.find_one(collection, query, project)

    def find(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.find(collection, query, project)

    def insert_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.insert_one(collection, document)

    def update_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        filter: Dict = None,  # type: ignore
        update: Dict = None,  # type: ignore
        **kwargs,
    ):
        db = self[database or self.default_database]

        return db.update_one(
            collection,
            filter,
            update,
            **kwargs,
        )

    def update_set_one(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        filter: Dict = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.update_set_one(
            collection,
            filter,
            document,
        )

    def count(
        self,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        query: Dict = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.count(collection, query)

    def distinct(
        self,
        key: str,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
    ):
        db = self[database or self.default_database]

        return db.distinct(key, collection)

    def aggregate(
        self,
        pipeline: _Pipeline,
        database: str = None,  # type: ignore
        collection: str = None,  # type: ignore
        **kwargs,
    ):
        db = self[database or self.default_database]

        return db.aggregate(pipeline, collection, **kwargs)
