from dataclasses import dataclass
from argparse import _SubParsersAction, ArgumentParser
from typing import Dict, Any, Literal


@dataclass
class Argument:
    T: type
    arg_main: str
    arg_sec: str | None = None
    default: Any = None
    help: str = ""
    action: Literal["store_true", "store_false"] | None = None
    nargs: Literal["+", "?", "*"] | int | None = None


def ArgumentGroup(name: str, help: str | None = None):
    def decorator(cls, _name, _help):
        # Gather the fields for the dataclass
        cls_vals: Dict[str, Argument] = {}
        for k, v in cls.__dict__.items():
            if type(v) is Argument:
                cls_vals[k] = v

        # -------------------------------------------------
        # Data class configuration
        # -------------------------------------------------
        # From fiels to dataclass arguments
        dtc_annotations = {}
        dtc_defauts = {}
        for name, config in cls_vals.items():
            dtc_annotations[name] = config.T

            if config.default is not None:
                dtc_defauts[name] = config.default

        # Making a new class
        obj_cls = type(
            f"{cls.__name__}Data",
            (object,),
            {
                "__annotations__": dtc_annotations,
                **dtc_defauts,
            },
        )
        obj_cls = dataclass(obj_cls)
        setattr(cls, "Data", obj_cls)

        # -------------------------------------------------
        # Parent class configuration
        # -------------------------------------------------
        @staticmethod
        def setup_parser(sp: _SubParsersAction):
            parser = sp.add_parser(_name, help=_help)

        setattr(cls, "setup_parser", setup_parser)
        setattr(
            cls,
            "__annotations__",
            {
                "Data": obj_cls,
                "setup_parser": type(setup_parser),
            },
        )

        # Look for the dataclass structure
        return cls

    # Return decorator
    return lambda cls: decorator(cls, name, help)
