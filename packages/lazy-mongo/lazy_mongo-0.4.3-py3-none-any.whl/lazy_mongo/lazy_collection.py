from typing import Dict, NamedTuple, TYPE_CHECKING
from pymongo.collection import Collection
from pymongo.results import UpdateResult
from pymongo.typings import _Pipeline
from pymongo.errors import DuplicateKeyError
from .update_response import UpdateResponse
from .insert_response import InsertResponse

if TYPE_CHECKING:
    from .lazy_database import LazyDatabase
    from .lazy_mongo import LazyMongo

try:
    from simple_chalk import chalk
except:
    from fun_things.not_chalk import NotChalk

    chalk = NotChalk()


class LazyCollection(NamedTuple):
    mongo: "LazyMongo"
    database: "LazyDatabase"
    collection: Collection

    def find_one(
        self,
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        return self.collection.find_one(query, project)

    def find(
        self,
        query: Dict = None,  # type: ignore
        project: Dict = None,  # type: ignore
    ):
        return self.collection.find(query, project)

    def __log_acknowledged(self, ok: bool):
        return chalk.green("✓") if ok else chalk.red("✕")

    def __log_duplicate(
        self,
        operation: str,
        e: DuplicateKeyError,
    ):
        details = ""

        if e.details != None:
            details = e.details["keyValue"].items()
            details = [f"{chalk.yellow(k)}={chalk.yellow(v)}" for k, v in details]
            details = chalk.dim.gray(", ").join(details)
            details = "{0} {1} {2}".format(
                chalk.dim.gray("{"),
                details,
                chalk.dim.gray("}"),
            )

        self.mongo._log_warn(
            operation,
            "{0} {1}".format(
                "Duplicate",
                details,
            ),
        )

    def __log_update(
        self,
        operation: str,
        result: UpdateResult,
    ):
        if result.upserted_id != None:
            self.mongo._log_info(
                operation,
                "{0} {1}".format(
                    str(result.upserted_id),
                    self.__log_acknowledged(result.acknowledged),
                ),
            )
            return

        n = result.modified_count

        if n == 0:
            n = chalk.yellow(n)

        self.mongo._log_info(
            operation,
            "{0} of {1} {2}".format(
                n,
                result.matched_count,
                self.__log_acknowledged(result.acknowledged),
            ),
        )

    def insert_one(
        self,
        document: Dict = None,  # type: ignore
    ):
        OPERATION = "InsertOne"

        try:
            result = self.collection.insert_one(document)

            self.mongo._log_info(
                OPERATION,
                "{0} {1}".format(
                    str(result.inserted_id),
                    self.__log_acknowledged(result.acknowledged),
                ),
            )

            return InsertResponse(
                ok=True,
                result=result,
            )

        except DuplicateKeyError as e:
            self.__log_duplicate(OPERATION, e)

            return InsertResponse(
                ok=False,
                is_duplicate=True,
                error=e,
            )

        except Exception as e:
            self.mongo._log_error(OPERATION, e)

            return InsertResponse(
                ok=False,
                error=e,
            )

    def update_one(
        self,
        filter: Dict = None,  # type: ignore
        update: Dict = None,  # type: ignore
        **kwargs,
    ):
        OPERATION = "UpdateOne"

        try:
            result = self.collection.update_one(
                filter=filter,
                update=update,
                **kwargs,
            )

            self.__log_update(OPERATION, result)

            return UpdateResponse(
                ok=True,
                result=result,
            )

        except DuplicateKeyError as e:
            self.__log_duplicate(OPERATION, e)

            return UpdateResponse(
                ok=False,
                is_duplicate=True,
                error=e,
            )

        except Exception as e:
            self.mongo._log_error(OPERATION, e)

            return UpdateResponse(
                ok=False,
                error=e,
            )

    def update_set_one(
        self,
        filter: Dict = None,  # type: ignore
        document: Dict = None,  # type: ignore
    ):
        """
        Shortcut for `$set`.

        Upsert = `False`
        """
        return self.update_one(
            filter,
            update={
                "$set": document,
            },
            upsert=False,
        )

    def count(
        self,
        query: Dict = None,  # type: ignore
    ):
        return self.collection.count_documents(query)

    def distinct(self, key: str):  # type: ignore
        return self.collection.distinct(key)

    def aggregate(self, pipeline: _Pipeline, **kwargs):
        return self.collection.aggregate(
            pipeline,
            **kwargs,
        )
