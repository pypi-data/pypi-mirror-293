import json
from typing import TypeVar, Dict, Any, Type, Optional

from pydantic import TypeAdapter

from src.mapper.core.singleton import Singleton
from src.util.catch import catch

T = TypeVar("T")


class Mapper(metaclass=Singleton):

    @staticmethod
    @catch(on_fail="Could not map provided source to type '{target}'")
    def map(source: Dict[str, Any], target: Type[T]) -> Optional[T]:
        """
        :param source: Input dictionary to be mapped
        :param target: The class expected at the output
        :return:
        """
        return TypeAdapter(target).validate_python(source)

    @staticmethod
    def to_bytes(obj: Any) -> bytes:
        return TypeAdapter(type(obj)).dump_json(obj)

    def to_dict(self, obj: Any) -> dict:
        result = json.loads(self.to_bytes(obj))
        return self._clear_nones(result)

    def _clear_nones(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                key: self._clear_nones(value)
                for key, value in obj.items()
                if key is not None and value is not None
            }
        if isinstance(obj, list):
            return [
                self._clear_nones(value)
                for value in obj
                if value is not None
            ]
        return obj

    def to_json(self, obj: Any, indent: Optional[int] = None) -> str:
        return json.dumps(self.to_dict(obj), indent=indent)
