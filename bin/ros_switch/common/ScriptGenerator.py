from .PresetConfig import PresetConfig
from .ShellCom import Shell


class ScriptGenerator:
    """
    This class generate the shell scripts to load and unload a profile
    """

    def __init__(self, config: PresetConfig):
        self._config = config

    def generate_load_unload(self) -> None:
        self._generate_load_script()
        self._generate_unload_script()

    def _generate_load_script(self) -> None:
        Shell.start_section("Loading script generation ...")

    def _generate_unload_script(self) -> None:
        Shell.start_section("Unloading script generation ...")
