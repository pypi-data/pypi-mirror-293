"""
Contains descriptions and default values for settings that are used by the sh command.
The settings can be overridden in the django settings file by prefexing the names with `DJANGO_SH_`.
"""

from typing import Callable, Optional, Union
from django.conf import settings
from django.core.management.base import CommandParser

IPYTHON_DIR: Optional[str] = getattr(settings, 'DJANGO_SH_IPYTHON_DIR', None)
"""The Path to a custom ipython directory. default: `None`"""

AUTO_IMPORT_MODELS: bool = getattr(settings, 'DJANGO_SH_AUTO_IMPORT_MODELS', True)
"""Tries to autodetect django apps with models and imports them. default: `True`"""

IMPORT_MODULES: tuple[str, Union[str, tuple[str], None]] = getattr(settings, 'DJANGO_SH_IMPORT_MODULES', ())
"""Defines additional modules that should be imported.
Should be a tuple or list containing entries like (module, imports).
Examples:
```
DJANGO_SH_IMPORT_MODULES = (
    ('datetime', ('datetime', 'timedelta')),  # -> from datetime import datetime, timedelta
    ('re', None),                             # -> import re
    ('decimal', 'Decimal'),                   # -> from decimal import Decimal
    ('foo.bar', '*')                          # -> from foo.bar import *
)
```
default: `()`"""

HOOK_ADD_ARGUMENTS: Optional[Callable[[CommandParser], None]] = getattr(settings, 'DJANGO_SH_HOOK_ADD_ARGUMENTS', None)
"""A function that adds arguments to the `sh` command. Example:
```
def DJANGO_SH_HOOK_ADD_ARGUMENTS(parser: CommandParser) -> None:
    parser.add_argument(...)
```
default: `None`"""

HOOK_GET_IMPORTED_OBJECTS: Optional[Callable[[dict, dict], None]] = getattr(settings, 'DJANGO_SH_HOOK_GET_IMPORTED_OBJECTS', None)
"""A function that is called after importing models and modules.
Can be used to further extend the `imported_objects` name space or to check command arguments. Example:
```
def DJANGO_SH_HOOK_GET_IMPORTED_OBJECTS(imported_objects: dict, options: dict) -> None:
    multiplier = int(options.get('multiplier', 0))
    imported_objects['multiply'] = lambda x: x * multiplier
```
default: `None`"""

HOOK_MODIFY_COMMAND: Optional[Callable[[str], str]] = getattr(settings, 'DJANGO_SH_HOOK_MODIFY_COMMAND', None)
"""Can be used to alter the command provided to `python manage.py sh -c '<command>'` Example:
```
def DJANGO_SH_HOOK_MODIFY_COMMAND(command: str) -> str:
    return f'start=time.time()\\n{command}\\nprint("Command took", time.time() - start, "seconds")'
```
default: `None`"""
