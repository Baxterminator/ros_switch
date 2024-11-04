from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any
from datetime import datetime
from textwrap import wrap

from ...utils.string_title import StrSections, Justify
from ..constants import (
    ENV_RSWITCH_PRE,
    APP_NAME,
    AUTHOR,
    VERSION,
    YEAR,
)
from ..ShellCom import Shell


@dataclass
class WriterConfig:
    # Logging
    log_term_width: int
    log_file_width: int

    # Special chars
    comment_prefix: str = "#"
    eol: str = "\n"

    def update_from(self, d: dict) -> "WriterConfig":
        for key, val in d.items():
            if key in self.__dict__.keys():
                setattr(self, key, val)
        return self


class ScriptWriter(ABC):
    def __init__(self, file_name: str, config: WriterConfig) -> None:
        self._filename = file_name
        self._config = config

    # --------------------------------------------------------
    # Low Level IO functions
    # --------------------------------------------------------

    def __enter__(self) -> "ScriptWriter":
        self._file = open(self._filename, "w+")
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._file.close()

    def _write_line(self, txt: str) -> None:
        self._file.write("{}{}".format(txt, self._config.eol))

    def _write_comment(self, txt: str) -> None:
        self._file.write(
            "{}{}{}".format(self._config.comment_prefix, txt, self._config.eol)
        )

    def new_line(self) -> None:
        self._write_line(self._config.eol)

    @abstractmethod
    def _format(self, val: Any) -> Any: ...

    # --------------------------------------------------------
    # Standard export functions
    # --------------------------------------------------------

    @abstractmethod
    def _write_cmd(self, cmd: str) -> None: ...
    @abstractmethod
    def export_var(self, var: str, val: Any) -> None: ...
    @abstractmethod
    def unset_var(self, var: str) -> None: ...
    @abstractmethod
    def _write_load_workspace(self, ws: str) -> None: ...
    @abstractmethod
    def _write_workspace_list(self, var: str, l: List[str]) -> None: ...
    @abstractmethod
    def _write_clean_path(self, path, ws) -> None: ...
    def _custom_load_dep(self) -> None: ...
    def _custom_unload_dep(self) -> None: ...

    # --------------------------------------------------------
    # High Level export
    # --------------------------------------------------------
    def _mk_load_env(self, var: str, val: Any) -> None:
        self.export_var(f"{ENV_RSWITCH_PRE}OLD_{var}", f"${var}")
        self.export_var(var, val)

    def _make_unload_env_var(self, var: str) -> None:
        self.export_var(var, f"${ENV_RSWITCH_PRE}OLD_{var}")
        self.unset_var(f"${ENV_RSWITCH_PRE}OLD_{var}")

    # --------------------------------------------------------
    # Writer utils
    # --------------------------------------------------------
    def log_step(self, txt, N: int | None = None) -> None:
        if N is not None and N == 0:
            return
        Shell.txt(
            "\t- Exporting {0} {1}".format(
                f"{txt} ".ljust(0 if N is None else self._config.log_term_width, "."),
                f"({N} registered)" if N is not None else "",
            )
        )
        self._write_line(
            self._config.eol
            + StrSections.make_enclosed_section(
                txt,
                line_prefix=self._config.comment_prefix,
                width=self._config.log_file_width,
            )
        )

    def make_header(
        self,
        preset_name: str,
        author: str,
        date: str,
        desc: str,
    ) -> None:
        self._write_line(
            StrSections.make_header(
                [
                    f"Compiled with {APP_NAME.upper()} - {VERSION}",
                    f"(c) {AUTHOR} - {YEAR}",
                    "",
                    f'Preset "{preset_name}" by {author} - {date}',
                    f"(compiled {datetime.today().strftime('%d/%m/%Y - %d %b %Y')})",
                    "",
                    Justify.LEFT,
                    *wrap(desc, width=self._config.log_file_width - 4),
                ],
                line_prefix=self._config.comment_prefix,
                width=self._config.log_file_width,
            )
        )
