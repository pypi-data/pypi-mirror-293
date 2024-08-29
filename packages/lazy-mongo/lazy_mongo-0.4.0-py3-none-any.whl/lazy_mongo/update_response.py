from typing import NamedTuple
from pymongo.results import UpdateResult


class UpdateResponse(NamedTuple):
    ok: bool
    is_duplicate: bool = False
    result: UpdateResult = None  # type: ignore
    error: Exception = None  # type: ignore
