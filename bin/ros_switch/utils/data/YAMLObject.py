from typing import TypeVar, Callable

from .UseDefault import dataclass_use_default
from .YAMLProcessor import YAMLProcessor

T = TypeVar("T")


def YAMLObject(
    _cls: T | None = None,  # type: ignore
    *,
    tag: str | None = None,
    str_corresp: str | None = None,
    auto_implement: bool = True,
):
    """
    Decorator that take care of all YAML Tag automatic parsing.

    Args:
        _cls (_type_, optional): the class that represent the data structure of the tag
        tag (str, optional): the tag name (e.g. if the tag is "foo", then it will automatically parse !foo blocks in the file)
        str_corresp (str, optional): the string to look in the YAML string when the YAMLPreprocessor will run to include tags (else will consider it the same as the tag argument)
        auto_implement (bool, optional): should the decorator implement an automatic parsing function (that simply redirect all values into the class constructor)

    Raises:
        UnImplementedMethod: if auto_implement is False and the class doesn't have a written static yaml_constructor method,
                            then raise an error since it won't be possible to load the YAML Tag.
    """
    from yaml import SafeLoader

    def decorator(cls: T) -> T:
        if auto_implement:

            def yaml_constructor(loader, node):
                return cls(**loader.construct_mapping(node))  # type: ignore

            setattr(cls, "yaml_constructor", yaml_constructor)

        # Register constructor
        if not hasattr(cls, "yaml_constructor"):
            raise RuntimeError(f"Class {str(cls)} has not implemented yaml_constructor")

        real_tag = tag if tag is not None else str(cls)
        real_key = str_corresp if str_corresp is not None else real_tag
        SafeLoader.add_constructor(f"!{real_tag}", cls.yaml_constructor)  # type: ignore

        # Register tag
        YAMLProcessor.register_tag(real_key, real_tag)

        return cls

    if _cls is None:
        l: Callable[[T], T] = lambda c: decorator(dataclass_use_default(c))  # type: ignore
        return l
    else:
        return decorator(dataclass_use_default(_cls))  # type: ignore
