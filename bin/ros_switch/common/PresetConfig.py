from enum import IntEnum
from typing import Dict, List
from dataclasses import field

from ..utils.YAMLObject import YAMLObject


class ROSVersion(IntEnum):
    ROS_1 = 1
    ROS_2 = 2
    ROS_1_2 = 3

    def name(self) -> str:
        for name, val in ROSVersion.__members__.items():
            if val == self.value:
                return name
        return "NotFound"


@YAMLObject(tag="metadata")
class MetaData:
    description: str = ""
    author: str = ""
    date: str = ""


@YAMLObject(tag="preset")
class PresetConfig:
    ros_version: ROSVersion

    metadata: MetaData = field(default_factory=MetaData)

    workspaces: List[str] = field(default_factory=list)
    env_var: Dict[str, str] = field(default_factory=dict)
    pre_load: List[str] = field(default_factory=list)
    post_load: List[str] = field(default_factory=list)

    pre_unload: List[str] = field(default_factory=list)
    post_unload: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Verification
        """
        self.ros_version = ROSVersion(self.ros_version)
