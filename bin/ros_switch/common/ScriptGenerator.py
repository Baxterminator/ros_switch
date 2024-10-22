from datetime import datetime
from textwrap import wrap
from .PresetConfig import PresetConfig
from .ShellCom import Shell
from .constants import ENV_RSWITCH_PRE, APP_NAME, AUTHOR, VERSION, YEAR
from ..utils.file import mk_file_dir
from ..utils.string_title import StrSections, Justify


class ScriptGenerator:
    """
    This class generate the shell scripts to load and unload a profile
    """

    PRE_LOAD_CMDS = "Pre-Load commands"
    ENV_VARIABLES = "Environment vars"
    WORKSPACES_SOURCE = "Workspaces sourcing"
    POST_LOAD_CMDS = "Post-Load commands"
    PRE_UNLOAD_CMDS = "Pre-Unload commands"
    POST_UNLOAD_CMDS = "Post-Unload commands"

    def __init__(
        self, config: PresetConfig, preset_name: str, load_path: str, unload_path: str
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
        with open(self._load_path, "w+") as load_script:
            ScriptGenerator.make_header(load_script, self._preset_name, self._config)

            # Generate pre-load commands
            ScriptGenerator.log_step(
                load_script,
                ScriptGenerator.PRE_LOAD_CMDS,
                len(self._config.pre_load),
            )
            for cmd in self._config.pre_load:
                load_script.write(f"{cmd}\n")

            # Generate env variables
            ScriptGenerator.log_step(
                load_script,
                ScriptGenerator.ENV_VARIABLES,
                len(self._config.env_var.keys()),
            )
            for env, val in self._config.env_var.items():
                load_script.write(f"export {ENV_RSWITCH_PRE}OLD_{env}=${env}\n")
                load_script.write(f"export {env}={val}\n")

            # Load workspaces
            ScriptGenerator.log_step(
                load_script,
                ScriptGenerator.WORKSPACES_SOURCE,
                len(self._config.workspaces),
            )
            for wkspace in self._config.workspaces:
                load_script.write(f'source "{wkspace}/install/setup.sh"\n')

            # Generate post-load commands
            ScriptGenerator.log_step(
                load_script,
                ScriptGenerator.POST_LOAD_CMDS,
                len(self._config.post_load),
            )
            for cmd in self._config.post_load:
                load_script.write(f"{cmd}\n")

    def _generate_unload_script(self) -> None:
        Shell.start_section("Unloading script generation")
        Shell.debug(
            f"Unload script directory for preset: {mk_file_dir(self._unload_path)}"
        )
        with open(self._unload_path, "w+") as unload_script:
            ScriptGenerator.make_header(unload_script, self._preset_name, self._config)
            # Generate pre-unload commands
            ScriptGenerator.log_step(
                unload_script,
                ScriptGenerator.PRE_UNLOAD_CMDS,
                len(self._config.pre_unload),
            )
            for cmd in self._config.pre_unload:
                unload_script.write(f"{cmd}\n")

            # Manage env variables
            ScriptGenerator.log_step(
                unload_script,
                ScriptGenerator.ENV_VARIABLES,
                len(self._config.env_var.keys()),
            )
            for env, _ in self._config.env_var.items():
                unload_script.write(f"export {env}=${ENV_RSWITCH_PRE}OLD_{env}\n")

            # Generate post-unload commands
            ScriptGenerator.log_step(
                unload_script,
                ScriptGenerator.POST_UNLOAD_CMDS,
                len(self._config.post_unload),
            )
            for cmd in self._config.post_unload:
                unload_script.write(f"{cmd}\n")

    LOG_STEP_WIDTH = 50
    FILE_SECTION_WIDTH = 80

    @staticmethod
    def log_step(file_handle, txt: str, N: int):
        if N == 0:
            return
        Shell.txt(
            "\t- Exporting {0} ({1} registered)".format(
                f"{txt} ".ljust(ScriptGenerator.LOG_STEP_WIDTH, "."),
                N,
            )
        )
        file_handle.write(
            "\n"
            + StrSections.make_enclosed_section(
                txt, line_prefix="# ", width=ScriptGenerator.FILE_SECTION_WIDTH
            )
        )

    @staticmethod
    def make_header(file_handle, preset_name: str, config: PresetConfig):
        file_handle.write(
            StrSections.make_header(
                [
                    f"Compiled with {APP_NAME.upper()} - {VERSION}",
                    f"(c) {AUTHOR} - {YEAR}",
                    "",
                    f'Preset "{preset_name}" by {config.metadata.author}',
                    f"(compiled {datetime.today().strftime('%d/%m/%Y - %d %b %Y')})",
                    "",
                    Justify.LEFT,
                    *wrap(
                        config.metadata.description,
                        width=ScriptGenerator.FILE_SECTION_WIDTH - 4,
                    ),
                ],
                line_prefix="# ",
                width=ScriptGenerator.FILE_SECTION_WIDTH,
            )
        )
