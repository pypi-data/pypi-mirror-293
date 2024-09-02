"""
Expander - a module for dealing with expansion of ENV vars in a file path.
"""
import os
import re

from typing import (
    Pattern,
    Tuple
)


_ENV_VAR: Pattern[str] = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")
_DEFAULT_SHELL: str = "bash"
_VAR_DIVIDER: str = "##"
_ENV_VAR_SYNTAX: str = "$"

def expand(path: str) -> str:
    """
    Expands env vars in a file path.

    Raises an error if a value for the env var cannot be found.
    """
    parts: list[str] = re.split(_ENV_VAR, path)
    shell: str = _fetch_shell()
    expanded_parts: list[str] = []

    for part in parts:
        if part.startswith(_ENV_VAR_SYNTAX):
            expanded_parts.append(_perform_expansion(part, shell))
        else:
            expanded_parts.append(part)

    return "".join(expanded_parts)

def expand_list(filepath_list: list[str]) -> list[Tuple[str, str]]:
    """
    Returns a list of expanded filepaths from a list of filepaths.

    Removes a filepath from the list if its value is blank.
    """
    filepaths = _VAR_DIVIDER.join(filepath_list)
    shell = _fetch_shell()
    expanded_filepaths = _perform_expansion(filepaths, shell)
    expanded_filepath_list = list(zip(
        filepath_list,
        expanded_filepaths.split(_VAR_DIVIDER)
    ))

    return expanded_filepath_list

def _fetch_shell() -> str:
    # NOTE: Entire shell path cannot be used because Plover's shell location may
    # not be the same as the user's machine.
    return os.getenv("SHELL", _DEFAULT_SHELL).split("/")[-1]

def _perform_expansion(target: str, shell: str) -> str:
    # NOTE: Using an interactive mode command (bash/zsh/fish -ic) seemed to be
    # the only way to access a user's env vars on a Mac outside Plover's
    # environment.
    expanded: str = os.popen(f"{shell} -ic 'echo {target}'").read().strip()

    if not expanded:
        raise ValueError(f"No value found for env var: {target}")

    return expanded
