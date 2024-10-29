from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, get_origin, Dict, Any, List, Generic, Iterator, Tuple

from ...common.ShellCom import Shell

_T = TypeVar("_T", object, None)

from typing import Type, Any


def isclass(cl: Type[Any]):
    try:
        return issubclass(cl, cl)
    except TypeError:
        return False


class CustomClassField(ABC, Generic[_T]):

    @abstractmethod
    def _make(self, val: _T): ...

    @staticmethod
    def _is_custom_field(c) -> bool:
        return isclass(c) and issubclass(c, CustomClassField)


INDEX_LOOKUP = [(0, 1), (0, 3), (2, 1), (2, 3)]


def _iterate_over_types(v1: Type, v2: Type) -> Iterator[Tuple[Type, Type]]:
    v = [v1, v2, get_origin(v1), get_origin(v2)]
    for x1, x2 in INDEX_LOOKUP:
        yield (v[x1], v[x2])


def _has_mismatch_type(v1: Type, v2: Type) -> bool:
    """
    Return True if both types are mismatched. Also support generic types.

    Args:
        v1 (Type): first type
        v2 (Type): second type

    Returns:
        bool: True if both types are not the same
    """
    for t1, t2 in _iterate_over_types(v1, v2):
        if t1 is t2:
            return False
    return True


def __process_class(cls: _T):
    """
    Process the class by generating a custom __post_init__ function where all values loaded into
    the dataclass are placed inside the default values.

    Args:
        cls (_T): the class to modifyx
    """
    defaults: Dict[str, Any] = {}

    # Get fields of interest
    for name, val in cls.__annotations__.items():
        origin = get_origin(val)
        if CustomClassField._is_custom_field(origin):
            defaults.update({name: getattr(cls, name)})
    setattr(cls, "_defaults", defaults)

    # Generate the post init function
    if len(defaults.keys()) != 0:

        def __post_init(self: _T):
            to_modify: List[str] = []
            for name, val in self.__annotations__.items():
                if _has_mismatch_type(val, type(getattr(self, name))) and name in self._defaults.keys():  # type: ignore
                    Shell.debug(f"Found field of key `{name}` to be replaced")  # type: ignore
                    to_modify.append(name)
            for name in to_modify:
                v = getattr(self, name)
                setattr(self, name, self._defaults[name]._make(v))  # type: ignore

        setattr(cls, "__post_init__", __post_init)

    return dataclass(cls)  # type: ignore


def dataclass_use_default(cls: _T = None):
    """
    Decorator wrapping around the dataclass decorator that allows the usage
    of custom classes (and already initialized instances) to be used when
    making a dataclass with default values.

    It automatically detect classes sub-instances of the CustomClassField
    interface and will automatically cast any primitive type into

    Args:
        cls (_type_, optional): _description_. Defaults to None.
    """
    if cls is None:
        return __process_class
    return __process_class(cls)
