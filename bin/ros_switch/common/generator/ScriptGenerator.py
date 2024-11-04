from enum import Enum
from typing import List

from .ScriptWriter import ScriptWriter, WriterConfig
from .ShellWriter import ShellScriptWriter

from ..PresetConfig import PresetConfig, ROSEnvironment, ROSVersion
from ..ShellCom import Shell
from ..constants import (
    ENV_RSWITCH_PRE,
    OS_TYPE,
    OSType,
    OS_TYPE,
)
from ...utils.file import mk_file_dir


class Messages:
    PRE_LOAD_CMDS = "Pre-Load commands"
    ENV_VARIABLES = "Environment vars"
    WORKSPACES_SOURCE = "Workspaces sourcing"
    WORKSPACES_CLEAN = "Workspaces cleaning"
    POST_LOAD_CMDS = "Post-Load commands"
    PRE_UNLOAD_CMDS = "Pre-Unload commands"
    POST_UNLOAD_CMDS = "Post-Unload commands"
    ROS_ENVIRONMENT = "ROS environment"
    DEPENDENCIES = "Dependencies"


class Vars:
    # Preset
    PRESET_NAME = f"{ENV_RSWITCH_PRE}PRESET_NAME"
    PRESET_FNAME = f"{ENV_RSWITCH_PRE}FPRESET_NAME"
    PRESET_COLOR = f"{ENV_RSWITCH_PRE}PRESET_COLOR"
    PRESET_SUFFIX = f"{ENV_RSWITCH_PRE}SUFFIX"

    WORKSPACE_VAR = f"{ENV_RSWITCH_PRE}WORKSPACES"

    ROS_DISTRO = "ROS_DISTRO"
    ROS_VERSION = "ROS_VERSION"
    PYTHON_VERSION = "ROS_PYTHON_VERSION"
    AMENT_PREFIX_PATH = "AMENT_PREFIX_PATH"
    COLCON_PREFIX_PATH = "COLCON_PREFIX_PATH"
    PKG_CONFIG_PATH = "PKG_CONFIG_PATH"
    ROS_ETC = "ROS_ETC_DIR"
    ROS_PACKAGE_PATH = "ROS_PACKAGE_PATH"
    ROS_ROOT = "ROS_ROOT"
    ROSLISP_PKG_DIR = "ROSLISP_PACKAGE_DIRECTORIES"

    @staticmethod
    def get_vars_list() -> List[str]:
        return [
            val
            for name, val in Vars.__dict__.items()
            if type(val) is str and not name.startswith("_")
        ]


class Paths(Enum):
    PYTHON = "PYTHONPATH"
    CMAKE = "CMAKE_PREFIX_PATH"
    LIBRARIES = "LD_LIBRARY_PATH"
    GLOBAL = "PATH"


class ScriptGenerator:
    """
    This class generate the shell scripts to load and unload a profile
    """

    LOG_STEP_WIDTH = 50
    FILE_SECTION_WIDTH = 80

    def __init__(
        self,
        config: PresetConfig,
        preset_name: str,
        load_path: str,
        unload_path: str,
    ):
        self._config = config
        self._preset_name = preset_name
        self._load_path = load_path
        self._unload_path = unload_path

    def generate_load_unload(self) -> None:
        self._generate_load_script()
        self._generate_unload_script()

    def _generate_load_script(self) -> None:
        Shell.start_section("Loading script generation")
        Shell.debug(
            f"Loading script directory for preset: {mk_file_dir(self._load_path)}"
        )
        with self._get_writer(self._load_path) as ldscript:
            ldscript.make_header(
                self._preset_name,
                self._config.metadata.author,
                self._config.metadata.date,
                self._config.metadata.description,
            )
            self._load_dependencies(ldscript)
            self._pre_load_commands(ldscript)
            self._set_app_env_vars(ldscript)
            self._set_custom_env_vars(ldscript)
            self._set_ros_env(ldscript)
            self._post_load_commands(ldscript)

    def _generate_unload_script(self) -> None:
        Shell.start_section("Unloading script generation")
        Shell.debug(
            f"Unload script directory for preset: {mk_file_dir(self._unload_path)}"
        )
        with self._get_writer(self._unload_path) as uldscript:
            uldscript.make_header(
                self._preset_name,
                self._config.metadata.author,
                self._config.metadata.date,
                self._config.metadata.description,
            )
            self._unload_dependencies(uldscript)
            self._pre_unload_commands(uldscript)
            self._unload_env_vars(uldscript)
            self._unload_ros_env(uldscript)
            self._clear_pathes(uldscript)
            self._post_unload_commands(uldscript)

    # -------------------------------------------------------------------------
    # Loading script steps
    # -------------------------------------------------------------------------
    def _load_dependencies(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.DEPENDENCIES)
        writer._custom_load_dep(self._config)
        writer._write_workspace_list(
            Vars.WORKSPACE_VAR,
            self._config.workspaces,
        )

    def _pre_load_commands(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.PRE_LOAD_CMDS, len(self._config.pre_load))
        for cmd in self._config.pre_load:
            writer._write_cmd(cmd)

    def _set_app_env_vars(self, writer: ScriptWriter) -> None:
        writer.log_step(
            Messages.ENV_VARIABLES,
            len(self._config.env_var.keys()),
        )
        writer.export_var(Vars.PRESET_NAME, self._preset_name)
        writer.export_var(Vars.PRESET_FNAME, f" {self._preset_name} ")
        writer.export_var(Vars.PRESET_COLOR, self._config.term.preset_color.term_color)
        writer.export_var(
            Vars.PRESET_SUFFIX,
            self._config.term.preset_color.BASH_SUFFIX,
        )

    def _set_custom_env_vars(self, writer: ScriptWriter) -> None:
        for env, val in self._config.env_var.items():
            writer._mk_load_env(env, val)

    def _set_ros_env(self, writer: ScriptWriter) -> None:
        # ROS environement variables
        writer.log_step(Messages.ROS_ENVIRONMENT)

        # ROS IP special case
        if self._config.ros_version == ROSVersion.ROS_1:
            writer.export_ros_ip(
                self._config.ros.ros_ip.env, self._config.ros.ros_ip.value
            )

        for env, val in self._config.ros.get_env().items():
            if env == ROSEnvironment.ros_ip.env:
                if self._config.ros_version == ROSVersion.ROS_1:
                    continue
                writer.export_ros_ip(env, val)
            writer.export_var(env, val)

        # ROS workspaces
        writer.log_step(Messages.WORKSPACES_SOURCE, len(self._config.workspaces))
        for wkspace in self._config.workspaces:
            writer._write_load_workspace(wkspace)

    def _post_load_commands(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.POST_LOAD_CMDS, len(self._config.post_load))
        for cmd in self._config.post_load:
            writer._write_cmd(cmd)

    # -------------------------------------------------------------------------
    # Unloading script steps
    # -------------------------------------------------------------------------

    def _unload_dependencies(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.DEPENDENCIES)
        writer._custom_unload_dep(self._config)
        writer._write_workspace_list(Vars.WORKSPACE_VAR, self._config.workspaces)

    def _pre_unload_commands(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.PRE_UNLOAD_CMDS, len(self._config.pre_unload))
        for cmd in self._config.pre_unload:
            writer._write_cmd(cmd)

    def _unload_env_vars(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.ENV_VARIABLES, len(self._config.env_var.keys()))
        for env, _ in self._config.env_var.items():
            writer._make_unload_env_var(env)

    def _unload_ros_env(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.ROS_ENVIRONMENT)
        for env_var in Vars.get_vars_list():
            writer.unset_var(env_var)
        for env, _ in self._config.ros.get_env().items():
            writer.unset_var(env)

    def _clear_pathes(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.WORKSPACES_CLEAN)
        for p in Paths.__members__.values():
            writer._write_clean_path(p.value, Vars.WORKSPACE_VAR)

    def _post_unload_commands(self, writer: ScriptWriter) -> None:
        writer.log_step(Messages.POST_UNLOAD_CMDS, len(self._config.post_unload))
        for cmd in self._config.post_unload:
            writer._write_cmd(cmd)

    # -------------------------------------------------------------------------
    # Static method
    # -------------------------------------------------------------------------

    @staticmethod
    def _get_writer(
        file_name: str,
    ) -> ScriptWriter:
        config = WriterConfig(
            ScriptGenerator.LOG_STEP_WIDTH,
            ScriptGenerator.FILE_SECTION_WIDTH,
        )
        match OS_TYPE:
            case OSType.LINUX | OSType.MACOS:
                return ShellScriptWriter(file_name, config)
            case OSType.WINDOWS:
                raise RuntimeError(
                    "Script generator not implemented for Windows systems !"
                )
