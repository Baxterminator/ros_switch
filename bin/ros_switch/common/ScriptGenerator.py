from datetime import datetime
from textwrap import wrap
from abc import ABC, abstractmethod
from typing import Any
from .PresetConfig import PresetConfig
from .ShellCom import Shell
from .constants import (
    ENV_RSWITCH_PRE,
    APP_NAME,
    AUTHOR,
    OS_TYPE,
    VERSION,
    YEAR,
    OSType,
    OS_TYPE,
)
from ..utils.file import mk_file_dir
from ..utils.string_title import StrSections, Justify


class ScriptGenerator(ABC):
    """
    This class generate the shell scripts to load and unload a profile
    """

    PRE_LOAD_CMDS = "Pre-Load commands"
    ENV_VARIABLES = "Environment vars"
    WORKSPACES_SOURCE = "Workspaces sourcing"
    POST_LOAD_CMDS = "Post-Load commands"
    PRE_UNLOAD_CMDS = "Pre-Unload commands"
    POST_UNLOAD_CMDS = "Post-Unload commands"
    ROS_ENVIRONMENT = "ROS environment"

    DEFAULT_ROS_ENV = [
        "ROS_DISTRO",
        "ROS_VERSION",
        "ROS_PYTHON_VERSION",
    ]

    def __init__(
        self,
        config: PresetConfig,
        preset_name: str,
        load_path: str,
        unload_path: str,
        prefix: str,
    ):
        self._config = config
        self._preset_name = preset_name
        self._load_path = load_path
        self._unload_path = unload_path
        self._prefix = prefix

    def generate_load_unload(self) -> None:
        self._generate_load_script()
        self._generate_unload_script()

    def _generate_load_script(self) -> None:
        Shell.start_section("Loading script generation")
        Shell.debug(
            f"Loading script directory for preset: {mk_file_dir(self._load_path)}"
        )
        with open(self._load_path, "w+") as load_script:
            self.make_header(load_script)

            # Generate pre-load commands
            self.log_step(
                load_script,
                ScriptGenerator.PRE_LOAD_CMDS,
                len(self._config.pre_load),
            )
            for cmd in self._config.pre_load:
                load_script.write(self._make_cmd(cmd))

            # Generate env variables
            self.log_step(
                load_script,
                ScriptGenerator.ENV_VARIABLES,
                len(self._config.env_var.keys()),
            )
            for env, val in self._config.env_var.items():
                load_script.write(self._make_load_env_var(env, val))

            # Load workspaces
            self.log_step(
                load_script,
                ScriptGenerator.WORKSPACES_SOURCE,
                len(self._config.workspaces),
            )
            for wkspace in self._config.workspaces:
                load_script.write(self._make_load_workspace(wkspace))

            # Generate post-load commands
            self.log_step(
                load_script,
                ScriptGenerator.POST_LOAD_CMDS,
                len(self._config.post_load),
            )
            for cmd in self._config.post_load:
                load_script.write(self._make_cmd(cmd))

    def _generate_unload_script(self) -> None:
        Shell.start_section("Unloading script generation")
        Shell.debug(
            f"Unload script directory for preset: {mk_file_dir(self._unload_path)}"
        )
        with open(self._unload_path, "w+") as unload_script:
            self.make_header(unload_script)
            # Generate pre-unload commands
            self.log_step(
                unload_script,
                ScriptGenerator.PRE_UNLOAD_CMDS,
                len(self._config.pre_unload),
            )
            for cmd in self._config.pre_unload:
                unload_script.write(self._make_cmd(cmd))

            # Manage env variables
            self.log_step(
                unload_script,
                ScriptGenerator.ENV_VARIABLES,
                len(self._config.env_var.keys()),
            )
            for env, _ in self._config.env_var.items():
                unload_script.write(self._make_unload_env_var(env))

            # Clearing ROS env variables
            self.log_step(unload_script, ScriptGenerator.ROS_ENVIRONMENT, None)
            for env_var in ScriptGenerator.DEFAULT_ROS_ENV:
                unload_script.write(self._make_unset_var(env_var))

            unload_script.write(self._make_unset_var("ROS_LOCALHOST_ONLY"))
            unload_script.write(self._make_unset_var("RCUTILS_COLORIZED_OUTPUT"))

            # Manage CMake, Python, LD and regular paths

            # Generate post-unload commands
            self.log_step(
                unload_script,
                ScriptGenerator.POST_UNLOAD_CMDS,
                len(self._config.post_unload),
            )
            for cmd in self._config.post_unload:
                unload_script.write(self._make_cmd(cmd))

    @staticmethod
    def get_generator(
        config: PresetConfig,
        preset_name: str,
        load_path: str,
        unload_path: str,
        prefix: str,
    ) -> "ScriptGenerator":
        match OS_TYPE:
            case OSType.LINUX | OSType.MACOS:
                return ShellScriptGenerator(config, preset_name, load_path, unload_path)

    @abstractmethod
    def _make_cmd(self, cmd: str) -> str: ...
    @abstractmethod
    def _make_load_env_var(self, var: str, val: Any) -> str: ...
    @abstractmethod
    def _make_unload_env_var(self, var: str) -> str: ...
    @abstractmethod
    def _make_load_workspace(self, ws: str) -> str: ...
    @abstractmethod
    def _make_unset_var(self, var: str) -> str: ...

    LOG_STEP_WIDTH = 50
    FILE_SECTION_WIDTH = 80

    def log_step(self, file_handle, txt: str, N: int | None):
        if N is not None and N == 0:
            return
        Shell.txt(
            "\t- Exporting {0} {1}".format(
                f"{txt} ".ljust(ScriptGenerator.LOG_STEP_WIDTH, "."),
                f"({N} registered)" if N is not None else "",
            )
        )
        file_handle.write(
            "\n"
            + StrSections.make_enclosed_section(
                txt, line_prefix=self._prefix, width=ScriptGenerator.FILE_SECTION_WIDTH
            )
        )

    def make_header(self, file_handle):
        file_handle.write(
            StrSections.make_header(
                [
                    f"Compiled with {APP_NAME.upper()} - {VERSION}",
                    f"(c) {AUTHOR} - {YEAR}",
                    "",
                    f'Preset "{self._preset_name}" by {self._config.metadata.author} - {self._config.metadata.date}',
                    f"(compiled {datetime.today().strftime('%d/%m/%Y - %d %b %Y')})",
                    "",
                    Justify.LEFT,
                    *wrap(
                        self._config.metadata.description,
                        width=ScriptGenerator.FILE_SECTION_WIDTH - 4,
                    ),
                ],
                line_prefix=self._prefix,
                width=ScriptGenerator.FILE_SECTION_WIDTH,
            )
        )


class ShellScriptGenerator(ScriptGenerator):
    """
    Script Generator for Shell terminals
    """

    def __init__(
        self,
        config: PresetConfig,
        preset_name: str,
        load_path: str,
        unload_path: str,
    ):
        super().__init__(config, preset_name, load_path, unload_path, "# ")

    def _make_cmd(self, cmd: str) -> str:
        return f"{cmd}\n"

    def _make_load_env_var(self, var: str, val: Any) -> str:
        return f"export {ENV_RSWITCH_PRE}OLD_{var}=${var}\nexport {var}={val}\n"

    def _make_unload_env_var(self, var: str) -> str:
        return f"export {var}=${ENV_RSWITCH_PRE}OLD_{var}\n"

    def _make_load_workspace(self, ws: str) -> str:
        return f'source "{ws}/install/local_setup.sh"\n'

    def _make_unset_var(self, var: str) -> str:
        return f"unset {var}\n"
