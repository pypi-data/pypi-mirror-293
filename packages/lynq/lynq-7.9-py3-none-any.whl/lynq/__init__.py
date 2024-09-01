"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lynq. If not, see <https://www.gnu.org/licenses/>.
"""

import atexit, os, atexit

from lynq._backendutils.lynq.pycache_remover import remove_pycache_from

import logging

from typing import Any, Final

VERSION: Final[float] = 7.9

# GIT BASH ONLY
# rm -rf dist build *.egg-info; python setup.py sdist bdist_wheel; twine upload dist/*

PYCACHE_REMOVAL_LOCATIONS: tuple[str] = (
    "",
    "app",
    "_backendutils",
    "_backendutils.lynq",
    "_backendutils.app",
    "_backendutils.server",
    "_backendutils.launcher",
    "_backendutils.basin",
    "_backendutils.custom",
    "_backendutils.dependencies",
    "_backendutils.dependencies.basin"
)

try:
    from lynqconfig import LOGGER as logger # type: ignore
    from lynqconfig import LOGGINGCONFIG as additional # type: ignore
    from lynqconfig import LOGGINGLEVEL as level # type: ignore
    from lynqconfig import LOGGINGFORMAT as format_ # type: ignore

    from lynqconfig import CLEANLOGGER as cleanlogger # type: ignore
    from lynqconfig import CLEANPYCACHE as clean # type: ignore
except ModuleNotFoundError:
    logger, \
    additional, \
    level, \
    format_, \
    clean, \
    cleanlogger \
    = None, None, None, None, None, None

logging.basicConfig(
    level = eval(f"logging.{level}") if level else logging.DEBUG,
    format = format_ or "%(asctime)s ~ %(levelname)s | %(message)s",
    **additional or {}
)

GLOBAL_LOGGER: Any = logger or logging.getLogger(__name__)
CLEAN_CACHE: bool = clean or False
CLEAN_LOGGER: bool = cleanlogger or True

if not os.path.exists("lynqconfig.py"):
    GLOBAL_LOGGER.warning("There has either been an error or you have not set up your lynqconfig.py file. Do you want to return it to the default state? By default nothing is changed and you'll still have the same experience using Lynq.")
    while True:

        i: str = input("[Y/n] ").lower()

        if i.startswith("y"):
            with open("lynqconfig.py", "w") as file:
                file.write("""
# Logging related config                       

LOGGER = None
LOGGINGCONFIG = None
LOGGINGLEVEL = None
LOGGINGFORMAT = None

# Clean up related config

CLEANLOGGER = None
CLEANPYCACHE = None
CLEANLOGFILE = None
                    
# See README.md for more info
""")
            break
        elif i.startswith("n"):
            break

def _clean_up() -> None:
    handlers: list[logging.Handler] = GLOBAL_LOGGER.handlers

    logging.shutdown()

    if os.path.exists("throwaway.log"):
        os.remove("throwaway.log")

def _clean_up_cache() -> None:
    GLOBAL_LOGGER.debug("Commencing pycache clean up process.")

    for path in PYCACHE_REMOVAL_LOCATIONS:
        remove_pycache_from(f"./lynq/{path.replace(".", "/")}")

def _at_exit_func() -> None:

    GLOBAL_LOGGER.debug("Commencing logger deletion and clean up process.")
    
    if CLEAN_CACHE:
        _clean_up_cache()

    if CLEAN_LOGGER:
        _clean_up()

    print(f"[Exiting...] Program ended successfully. All active servers terminated.")

atexit.register(_at_exit_func)