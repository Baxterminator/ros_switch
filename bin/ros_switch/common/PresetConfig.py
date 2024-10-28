from enum import IntEnum
from typing import Dict, Generic, List, Any, TypeVar, get_args, get_origin
from dataclasses import field

from ..utils.data.YAMLObject import YAMLObject
from ..utils.data.UseDefault import CustomClassField

T = TypeVar("T")


class EnvVar(Generic[T], CustomClassField[T]):
    def __init__(self, env: str, value: T | None = None):
        self.env = env
        self.value = value

    def __repr__(self) -> str:
        return f"EnvVar(env={self.env}, val={self.value})"

    def _make(self, val: T):
        return EnvVar[T](self.env, val)


class ROSVersion(IntEnum):
    ROS_1 = 1
    ROS_2 = 2
    ROS_1_2 = 3

    def name(self, val: int) -> str:
        for name, val in ROSVersion.__members__.items():
            if val == self.value:
                return name
        return "NotFound"


@YAMLObject(tag="metadata")
class MetaData:
    description: str = ""
    author: str = ""
    date: str = ""


@YAMLObject(tag="ros")
class ROSEnvironment:
    # ROS
    localhost: EnvVar[bool] = EnvVar[bool]("ROS_LOCALHOST_ONLY")
    ros_root: EnvVar[str] = EnvVar[str]("ROS_ROOT")
    log_dir: EnvVar[str] = EnvVar[str]("ROS_LOG_DIR")

    # ROS 1 exclusives
    ros_master_uri: EnvVar[str] = EnvVar[str]("ROS_MASTER_URI")
    ros_hostname: EnvVar[str] = EnvVar[str]("ROS_HOSTNAME")
    ros_ip: EnvVar[str] = EnvVar[str]("ROS_IP")

    # ROS 2 exclusives
    domain_id: EnvVar[int] = EnvVar[int]("ROS_DOMAIN_ID")

    # RCUtils
    colorized: EnvVar[bool] = EnvVar[bool]("RCUTILS_COLORIZED_OUTPUT")
    output_format: EnvVar[str] = EnvVar[str]("RCUTILS_CONSOLE_OUTPUT_FORMAT")
    use_stdout: EnvVar[bool] = EnvVar[bool]("RCUTILS_LOGGING_USE_STDOUT")
    buffered: EnvVar[bool] = EnvVar[bool]("RCUTILS_LOGGING_BUFFERED_STREAM")

    def get_env(self) -> Dict[str, Any]:
        out = {}
        for _, val in self.__dict__.items():
            assert type(val) is EnvVar
            if val.value is not None:
                out.update({val.env: val.value})
        return out


@YAMLObject(tag="preset")
class PresetConfig:
    ros_version: ROSVersion

    metadata: MetaData = field(default_factory=MetaData)

    workspaces: List[str] = field(default_factory=list)

    env_var: Dict[str, str] = field(default_factory=dict)
    ros: ROSEnvironment = field(default_factory=ROSEnvironment)

    pre_load: List[str] = field(default_factory=list)
    post_load: List[str] = field(default_factory=list)
    pre_unload: List[str] = field(default_factory=list)
    post_unload: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Verification
        """
        self.ros_version = ROSVersion(self.ros_version)
