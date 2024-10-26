from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterator, List, Tuple
import os
import yaml
import re

from .ScriptGenerator import ScriptGenerator
from .PresetConfig import PresetConfig
from .ShellCom import Shell
from .constants import (
    PRESET_EXTENSION,
    PRESET_DIR,
    PRESET_PATHS,
    UNLOAD_DIR,
    LOAD_DIR,
    SCRIPT_EXT,
)
from ..utils.file import read_file
from ..utils.YAMLObject import YAMLProcessor


class PathType(Enum):
    BOTH = 0
    ADMIN = 1
    USER = 2


@dataclass
class PresetData:
    preset_name: str
    is_admin: bool
    preset_file: str
    install_script: str | None = None
    uninstall_script: str | None = None

    config: PresetConfig | None = None

    def __post_init__(self):
        self.install_script = PresetData.preset_file2install_file(self.preset_file)
        self.uninstall_script = PresetData.preset_file2uninstall_file(self.preset_file)

    def is_generated(self) -> bool:
        """
        Return True if the install / uninstall files have been generated
        """
        return (
            self.install_script is not None and os.path.exists(self.install_script)
        ) and (
            self.uninstall_script is not None and os.path.exists(self.uninstall_script)
        )

    def get_config(self) -> PresetConfig | None:
        """
        Get the configuration associated with this preset, or None if an error happened
        """
        if self.config is None:
            Shell.start_section("Preset YAML Loading")
            try:
                # Load file
                Shell.debug(f"Loading file {self.preset_file}")
                data = read_file(self.preset_file)
                if data is None:
                    raise RuntimeError(
                        f"Unable to load YAML data for preset {self.preset_name}"
                    )

                # Pre-processing YAML string
                Shell.debug(YAMLProcessor.print_mappings())
                data = YAMLProcessor.raw_2_tags(data)
                Shell.debug(f"Output of YAMLProcessor:\n{data}")

                # Parse YAML Configuration
                config: dict | None = yaml.safe_load(data)
                if config is None or "preset" not in config.keys():
                    raise RuntimeError("The YAML file couldn't be parsed correctly ...")
                self.config = config["preset"]
                Shell.txt("\t-> YAML loaded successfully")
                Shell.debug(f"{self.config}")
            except RuntimeError as e:
                raise RuntimeError(f"Error while loading configuration file: \n\t{e}")
        return self.config

    def generate_files(self, ignore_warnings: bool = False) -> None:
        """
        Launch the generation of install and uninstall scripts.
        """
        if not ignore_warnings and self.is_generated():
            Shell.warning(
                f"Loading / Unloading script for preset {self.preset_name} already exists! Overwriting ..."
            )

        # Check if config not loaded, then load it
        if self.config is None:
            self.get_config()

            if self.config is None:
                raise RuntimeError(
                    f"Trying to generate config on unexisting config `{self.preset_name}`!"
                )

        # Test if destination path exists
        if self.install_script is None or self.uninstall_script is None:
            raise RuntimeError("Trying to generate files on None paths ...")

        generator = ScriptGenerator.get_generator(
            self.config,
            self.preset_name,
            self.install_script,
            self.uninstall_script,
        )
        generator.generate_load_unload()

    # =========================================================================
    # Preset lookup functions
    # =========================================================================
    @staticmethod
    def find_profile(profile_name: str) -> "PresetData|None":
        """
        Look for a ROS profile inside of the profiles directories

        Args:
            profile_name (str): the name of the profile

        Returns:
            Tuple[str, str] | None: a tuple of
        """
        # Look for the several locations
        profile = None
        for path, is_admin in PresetData.path_iter():
            profile = PresetData.__find_profile_in_dir(path, is_admin, profile_name)
            if profile is not None:
                break
        return profile

    @staticmethod
    def list_admin_configs() -> "Dict[str, PresetData]":
        """
        Find the preset made by the admin

        Returns:
            Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
        """
        founds = {}
        for path, is_admin in PresetData.path_iter(PathType.ADMIN):
            founds = dict(
                founds,
                **PresetData.__list_profiles_in_dir(path, is_admin, founds.keys()),  # type: ignore
            )
        return founds

    @staticmethod
    def list_user_configs() -> "Dict[str, PresetData]":
        """
        Find the preset made by the user

        Returns:
            Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
        """
        founds = {}
        for path, is_admin in PresetData.path_iter(PathType.USER):
            founds = dict(
                founds,
                **PresetData.__list_profiles_in_dir(path, is_admin, founds.keys()),  # type: ignore
            )
        return founds

    @staticmethod
    def list_preset_files() -> "Dict[str, PresetData]":
        """
        Find all presets found on the system

        Returns:
            Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
        """
        founds = {}
        for path, is_admin in PresetData.path_iter():
            founds = dict(
                founds,
                **PresetData.__list_profiles_in_dir(path, is_admin, founds.keys()),  # type: ignore
            )
        return founds

    # =========================================================================
    # Helpers function
    # =========================================================================
    @staticmethod
    def path_iter(mode: PathType = PathType.BOTH) -> Iterator[Tuple[str, bool]]:
        """
        Generator yielding the known configuration paths.

        Yields:
            Iterator[Tuple[str, bool]]: an iterator yielding a (path, is admin conf) tuple
        """
        # Define the right test
        match mode:
            case PathType.ADMIN:
                test = lambda t: t[1]
            case PathType.USER:
                test = lambda t: not t[1]
            case _:
                test = lambda t: True

        # Iterate over the paths
        for t in PRESET_PATHS:
            if test(t):
                yield t

    @staticmethod
    def preset_file2preset_name(file_name: str) -> str:
        return file_name.split(".")[0].replace("_", " ").title()

    @staticmethod
    def preset_name2preset_file(preset_name: str) -> str:
        return preset_name.lower().replace(" ", "_") + PRESET_EXTENSION

    @staticmethod
    def preset_file2install_file(preset_file: str) -> str:
        """
        Return the path to the install file based on the preset file path

        Args:
            preset_file (str): the path of the preset file

        Returns:
            str: the path to the install script
        """
        return re.sub(
            PRESET_EXTENSION,
            SCRIPT_EXT,
            PresetData.change_path_last_dir(preset_file, LOAD_DIR),
        )

    @staticmethod
    def preset_file2uninstall_file(preset_file: str) -> str:
        """
        Return the path to the uninstall file based on the preset file path

        Args:
            preset_file (str): the path of the preset file

        Returns:
            str: the path to the uninstall script
        """
        return re.sub(
            PRESET_EXTENSION,
            SCRIPT_EXT,
            PresetData.change_path_last_dir(preset_file, UNLOAD_DIR),
        )

    @staticmethod
    def change_path_last_dir(input_path: str, new_dir: str) -> str:
        """
        Change the last directory in the provided path by the given one

        Args:
            input_path (str): the input path
            new_dir (str): the name of the last dir to change

        Returns:
            str: the modified path with the new directory
        """
        p_split = input_path.split(os.path.sep)
        return re.sub(p_split[-2], new_dir, input_path)

    # =========================================================================
    # Directories walks function
    # =========================================================================
    @staticmethod
    def __find_profile_in_dir(
        dirpath: str,
        is_admin: bool,
        preset_name: str,
    ) -> "PresetData|None":
        """
        Walk the dir to find the given ROS configuration file

        Args:
            dirpath (str): the path to look into
            is_admin (bool): whether or not the path is admin configs
            profile_name (str): the profile name to look for

        Returns:
            PresetData | None: the data of the preset if it exists, None otherwise
        """
        # Test for directory to exist
        if not os.path.exists(dirpath):
            return None

        for dpath, _, filenames in os.walk(os.path.join(dirpath, PRESET_DIR)):
            for f in filenames:
                # Check if profile file
                if not f.endswith(PRESET_EXTENSION):
                    continue

                # Compute simple name
                found_preset = PresetData.preset_file2preset_name(f)

                if found_preset.lower() == preset_name.lower():
                    return PresetData(
                        found_preset,
                        is_admin,
                        os.path.join(dpath, f),
                        "",
                        "",
                    )
        return None

    @staticmethod
    def __list_profiles_in_dir(
        dirpath: str,
        is_admin: bool,
        existing_names: List[str] = [],
    ) -> "Dict[str, PresetData]":
        """
        Walk the dir to find the ROS profile configuration files.

        Args:
            dirpath (str): the path to look into for conf files

        Returns:
            Dict[str, "Tuple[str, str]"]: a map (k,v) of {preset_name: (tag, preset_path)}
        """
        # Test for directory to exist
        if not os.path.exists(dirpath):
            return {}

        out = {}
        for dpath, _, filenames in os.walk(os.path.join(dirpath, PRESET_DIR)):
            for f in filenames:
                # Check if profile file
                if not f.endswith(PRESET_EXTENSION):
                    continue

                # Compute simple name
                found_preset = PresetData.preset_file2preset_name(f)

                # Test if name already used
                if found_preset in out.keys() or found_preset in existing_names:
                    i = 1
                    new_preset = f"{found_preset}_{i}"
                    while new_preset in out.keys() or new_preset in existing_names:
                        i += 1
                        new_preset = f"{found_preset}_{i}"
                    found_preset = new_preset

                out[found_preset] = PresetData(
                    found_preset, is_admin, os.path.join(dpath, f), "", ""
                )
        return out
