from enum import IntEnum

from ..utils.YAMLObject import YAMLObject
from .ShellCom import Shell


class ROSVersion(IntEnum):
    ROS_1 = 1
    ROS_2 = 2
    ROS_1_2 = 3

    def name(self) -> str:
        for name, val in ROSVersion.__members__.items():
            if val == self.value:
                return name
        return "NotFound"


@YAMLObject(tag="config")
class PresetConfig:
    ros_version: ROSVersion

    def __post_init__(self) -> None:
        """
        Verification
        """
        self.ros_version = ROSVersion(self.ros_version)
