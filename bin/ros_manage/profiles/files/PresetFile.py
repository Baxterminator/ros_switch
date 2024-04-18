from dataclasses import dataclass
from enum import IntEnum


class ROSVersion(IntEnum):
    ROS_1 = 1
    ROS_2 = 2
    ROS_1_2 = 3


@dataclass
class PresetConfig:
    ros_version: ROSVersion


@dataclass
class PresetFile:
    preset_name: str
    config_file: str
    bash_file: str

    config: PresetConfig

    def load_file(self):
        # Check for the existance of the config file
        if self.config_file is None:
            raise RuntimeError(
                f"Trying to load config file {self.config_file} that doesn't exist!"
            )
