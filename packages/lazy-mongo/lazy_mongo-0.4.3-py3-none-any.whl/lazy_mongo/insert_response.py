from typing import NamedTuple
from pymongo.results import InsertOneResult


class InsertResponse(NamedTuple):
    ok: bool
    is_duplicate: bool = False
    result: InsertOneResult = None  # type: ignore
    error: Exception = None  # type: ignore
