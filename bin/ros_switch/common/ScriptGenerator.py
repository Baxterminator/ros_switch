from datetime import datetime
from textwrap import wrap
from abc import ABC, abstractmethod
from typing import Any, List

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
    WORKSPACES_CLEAN = "Workspaces cleaning"
    POST_LOAD_CMDS = "Post-Load commands"
    PRE_UNLOAD_CMDS = "Pre-Unload commands"
    POST_UNLOAD_CMDS = "Post-Unload commands"
    ROS_ENVIRONMENT = "ROS environment"
    DEPENDENCIES = "Dependencies"

    # Environment variables
    DEFAULT_ROS_ENV = [
        "ROS_DISTRO",
        "ROS_VERSION",
        "ROS_PYTHON_VERSION",
        "AMENT_PREFIX_PATH",
        "COLCON_PREFIX_PATH",
    ]
    PRESET_NAME_VAR = f"{ENV_RSWITCH_PRE}PRESET_NAME"
    WORKSPACE_VAR = f"{ENV_RSWITCH_PRE}WORKSPACES"
    ENV_TO_CLEAR = ["PYTHONPATH", "CMAKE_PREFIX_PATH", "LD_LIBRARY_PATH"]
    PRESET_COLOR = f"{ENV_RSWITCH_PRE}PRESET_COLOR"
    PRESET_SUFFIX = f"{ENV_RSWITCH_PRE}SUFFIX"

    def __init__(
        self,
        config: PresetConfig,
        preset_name: str,
        load_path: str,
        unload_path: str,
        prefix: str,
        eol: str,
    ):
        self._config = config
        self._preset_name = preset_name
        self._load_path = load_path
        self._unload_path = unload_path
        self._prefix = prefix
        self._eol = eol

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

            # Add dependencies
            self.log_step(load_script, ScriptGenerator.DEPENDENCIES, None)
            self.__write(load_script, self._custom_load_dep())
            self.__write(load_script, self._mk_workspace_list(self._config.workspaces))

            # Generate pre-load commands
            self.log_step(
                load_script,
                ScriptGenerator.PRE_LOAD_CMDS,
                len(self._config.pre_load),
            )
            for cmd in self._config.pre_load:
                self.__write(load_script, self._make_cmd(cmd))

            # Generate env variables
            self.log_step(
                load_script,
                ScriptGenerator.ENV_VARIABLES,
                len(self._config.env_var.keys()),
            )
            self.__write(
                load_script,
                self._mk_export_env(
                    ScriptGenerator.PRESET_NAME_VAR, self._format(self._preset_name)
                ),
            )
            self.__write(
                load_script,
                self._mk_export_env(
                    ScriptGenerator.PRESET_COLOR,
                    self._format(self._config.term.preset_color.term_color),
                ),
            )
            self.__write(
                load_script,
                self._mk_export_env(
                    ScriptGenerator.PRESET_SUFFIX,
                    self._format(self._config.term.preset_color.BASH_SUFFIX),
                ),
            )
            for env, val in self._config.env_var.items():
                self.__write(load_script, self._mk_load_env(env, self._format(val)))
                self.__write(load_script)
            self.log_step(load_script, ScriptGenerator.ROS_ENVIRONMENT, None)
            for env, val in self._config.ros.get_env().items():
                self.__write(load_script, self._mk_export_env(env, self._format(val)))

            # Load workspaces
            self.log_step(
                load_script,
                ScriptGenerator.WORKSPACES_SOURCE,
                len(self._config.workspaces),
            )
            for wkspace in self._config.workspaces:
                self.__write(load_script, self._make_load_workspace(wkspace))

            # Generate post-load commands
            self.log_step(
                load_script,
                ScriptGenerator.POST_LOAD_CMDS,
                len(self._config.post_load),
            )
            for cmd in self._config.post_load:
                self.__write(load_script, self._make_cmd(cmd))

    def _generate_unload_script(self) -> None:
        Shell.start_section("Unloading script generation")
        Shell.debug(
            f"Unload script directory for preset: {mk_file_dir(self._unload_path)}"
        )
        with open(self._unload_path, "w+") as unload_script:
            self.make_header(unload_script)

            # Add dependencies
            self.log_step(unload_script, ScriptGenerator.DEPENDENCIES, None)
            self.__write(unload_script, self._custom_unload_dep())
            self.__write(
                unload_script, self._mk_workspace_list(self._config.workspaces)
            )

            # Generate pre-unload commands
            self.log_step(
                unload_script,
                ScriptGenerator.PRE_UNLOAD_CMDS,
                len(self._config.pre_unload),
            )
            for cmd in self._config.pre_unload:
                self.__write(unload_script, self._make_cmd(cmd))

            # Manage env variables
            self.log_step(
                unload_script,
                ScriptGenerator.ENV_VARIABLES,
                len(self._config.env_var.keys()),
            )
            for env, _ in self._config.env_var.items():
                self.__write(unload_script, self._make_unload_env_var(env))

            # Clearing application env var
            for env in [
                ScriptGenerator.PRESET_COLOR,
                ScriptGenerator.PRESET_SUFFIX,
                ScriptGenerator.PRESET_NAME_VAR,
            ]:
                self.__write(unload_script, self._make_unset_env_var(env))

            # Clearing ROS env variables
            self.log_step(unload_script, ScriptGenerator.ROS_ENVIRONMENT, None)
            for env_var in ScriptGenerator.DEFAULT_ROS_ENV:
                self.__write(unload_script, self._make_unset_var(env_var))
            for env, _ in self._config.ros.get_env().items():
                self.__write(unload_script, self._make_unset_env_var(env))

            # Manage CMake, Python, LD and regular paths
            self.log_step(unload_script, ScriptGenerator.WORKSPACES_CLEAN, None)
            for p in ScriptGenerator.ENV_TO_CLEAR:
                self.__write(
                    unload_script,
                    self._make_clean_path(p, ScriptGenerator.WORKSPACE_VAR),
                )

            # Generate post-unload commands
            self.log_step(
                unload_script,
                ScriptGenerator.POST_UNLOAD_CMDS,
                len(self._config.post_unload),
            )
            for cmd in self._config.post_unload:
                self.__write(unload_script, self._make_cmd(cmd))

    @staticmethod
    def get_generator(
        config: PresetConfig,
        preset_name: str,
        load_path: str,
        unload_path: str,
    ) -> "ScriptGenerator":
        match OS_TYPE:
            case OSType.LINUX | OSType.MACOS:
                return ShellScriptGenerator(config, preset_name, load_path, unload_path)
            case OSType.WINDOWS:
                raise RuntimeError(
                    "Script generator not implemented for Windows systems !"
                )

    def __format_line(self, txt: str) -> str:
        return "{}{}".format(txt, self._eol)

    def __write(self, file, txt="") -> None:
        return file.write(self.__format_line(txt))

    @abstractmethod
    def _make_cmd(self, cmd: str) -> str: ...
    @abstractmethod
    def _mk_export_env(self, var: str, val: Any) -> str: ...
    @abstractmethod
    def _make_unset_env_var(self, var: str) -> str: ...
    @abstractmethod
    def _make_load_workspace(self, ws: str) -> str: ...
    @abstractmethod
    def _make_unset_var(self, var: str) -> str: ...
    @abstractmethod
    def _format(self, val: Any) -> Any: ...
    @abstractmethod
    def _mk_workspace_list(self, l: List[str]) -> str: ...
    @abstractmethod
    def _make_clean_path(self, path, ws) -> str: ...

    def _custom_load_dep(self) -> str:
        return ""

    def _custom_unload_dep(self) -> str:
        return ""

    def _mk_load_env(self, var: str, val: Any) -> str:
        return self._eol.join(
            [
                self._mk_export_env(f"{ENV_RSWITCH_PRE}OLD_{var}", f"${var}"),
                self._mk_export_env(var, val),
            ]
        )

    def _make_unload_env_var(self, var: str) -> str:
        return self._eol.join(
            [
                self._mk_export_env(var, f"${ENV_RSWITCH_PRE}OLD_{var}"),
                self._make_unset_var(f"{ENV_RSWITCH_PRE}OLD_{var}"),
            ],
        )

    LOG_STEP_WIDTH = 50
    FILE_SECTION_WIDTH = 80

    def log_step(self, file_handle, txt: str, N: int | None):
        if N is not None and N == 0:
            return
        Shell.txt(
            "\t- Exporting {0} {1}".format(
                f"{txt} ".ljust(
                    0 if N is None else ScriptGenerator.LOG_STEP_WIDTH, "."
                ),
                f"({N} registered)" if N is not None else "",
            )
        )
        file_handle.write(
            self._eol
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
        super().__init__(config, preset_name, load_path, unload_path, "# ", "\n")

    def _make_cmd(self, cmd: str) -> str:
        return f"{cmd}"

    def _mk_export_env(self, var: str, val: Any) -> str:
        return f"export {var}={val}"

    def _make_unset_env_var(self, var: str) -> str:
        return f"unset {var}"

    def _make_load_workspace(self, ws: str) -> str:
        return f'source "{ws}/install/local_setup.sh"'

    def _make_clean_path(self, path, ws) -> str:
        return f"export {path}=$(_remove_paths ${path} ${ws})"

    def _make_unset_var(self, var: str) -> str:
        return f"unset {var}"

    def _format(self, val: Any) -> Any:
        if type(val) is bool:
            return 1 if val else 0
        if type(val) is str:
            s = val.replace('"', r"\"")
            return f'"{s}"'
        return val

    def _mk_workspace_list(self, l: List[str]) -> str:
        out = f"{ScriptGenerator.WORKSPACE_VAR}=({self._eol}"
        for wk in l:
            out += f'\t"{wk}"{self._eol}'
        out += ")"
        return out

    def _custom_unload_dep(self) -> str:
        out = """_remove_paths()
{
    if [[ $SHELL_TYPE == "bash" ]]; then
        IFS=':' read -ra PATHES <<< "$1"
    else
        IFS=':' read -rA PATHES <<< "$1"
    fi
    local THISPATH=""
    local fpath
    local ARGS="$@"
    local N_ARGS="$#"
    for fpath in "${PATHES[@]}"; do
        local to_remove=0
        local i
        for (( i=2; i <=$N_ARGS; i++ )); do
            if [[ $fpath = *"${ARGS[i]}"* ]]; then
                to_remove=1
            break
            fi
        done
        if [ $to_remove -eq 0 ]; then
            THISPATH="$THISPATH:$path"
        fi
    done
    echo $THISPATH | cut -c2-
}
        """
        return out
