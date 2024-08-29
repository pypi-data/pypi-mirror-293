from abc import ABC
from typing import Any, Optional, Tuple


class AbstractMapper(ABC):

    # TODO stop using this method. only add fields that we want to show to 'entity' model, do not add everything only to exclude it later
    @staticmethod
    def get_exclude_fields() -> Tuple:
        return ()

    @staticmethod
    def build_entity(item: Any) -> Optional[Any]:
        raise NotImplementedError()
