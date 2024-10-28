from typing import Dict
import re


class YAMLProcessor:
    """
    Class to preprocess YAML string to get all the modifications needed for a proper parsing
    """

    FORWARD: Dict[str, str] = {}  # Key (string in YAML to replace) -> tag
    BACKWARD: Dict[str, str] = {}  # Tag -> key

    @staticmethod
    def register_tag(key: str, tag: str) -> None:
        if tag not in YAMLProcessor.BACKWARD.keys():
            YAMLProcessor.FORWARD[key] = f"!{tag}"
            YAMLProcessor.BACKWARD[f"!{tag}"] = key

    @staticmethod
    def print_mappings() -> str:
        out_str = "YAMLProcessor mappings:\n"
        for key, tag in YAMLProcessor.FORWARD.items():
            out_str += f"\t{key} <-> {tag}\n"

        return out_str

    @staticmethod
    def raw_2_tags(raw_yaml: str) -> str:
        """
        Replace

        Args:
            raw_yaml (str): the raw YAML string in which to place tags

        Returns:
            str: the modified string with tags for
        """
        # Get root tag
        root_tag = raw_yaml.split(":")[0]
        out_str = str(raw_yaml)
        for k, tag in YAMLProcessor.FORWARD.items():
            out_str = re.sub(f"(^|\n\s+){k} ?:", rf"\1{k}: {tag}", out_str, flags=re.IGNORECASE)  # type: ignore
        return out_str

    @staticmethod
    def tag_2_raw(tag_yaml: str) -> str:
        out_str = str(tag_yaml)
        for tag, k in YAMLProcessor.BACKWARD.items():
            out_str = re.sub(tag, f"{k}:", out_str, flags=re.IGNORECASE)
        return out_str
