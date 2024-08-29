# django-shell-extended

Provides a `sh` management-command that can be customized via django settings.

## Quick start
1. Install with `pip install django-shell-extended`
2. Add `"django_shell_extended"` to your `INSTALLED_APPS` setting like this:
    ```python
    INSTALLED_APPS = [
        # ...
        "django_shell_extended",
    ]
    ```
3. (Optional) Change the settings described in the next section in your `settings.py`
4. Start the shell via `python manage.py sh`

## Available settings
```python
# The Path to a custom ipython directory.
# default: None
DJANGO_SH_IPYTHON_DIR = "/some/path/.ipython/"

# Tries to autodetect django apps with models and imports them as `from my_app.models import *`
# default: True
DJANGO_SH_AUTO_IMPORT_MODELS = True

# Defines additional modules that should be imported.
# Should be a tuple or list containing entries like `(module, imports)`.
# default: ()
DJANGO_SH_IMPORT_MODULES = (
    ('datetime', ('datetime', 'timedelta')),  # -> from datetime import datetime, timedelta
    ('re', None),                             # -> import re
    ('decimal', 'Decimal'),                   # -> from decimal import Decimal
    ('foo.bar', '*')                          # -> from foo.bar import *
)

# A function that adds command line arguments to the `sh` command.
# default: None
def DJANGO_SH_HOOK_ADD_ARGUMENTS(parser: CommandParser) -> None:
    parser.add_argument(...)


# A function that is called after importing models and modules.
# Can be used to further extend the `imported_objects` name space or to check command arguments. Example::
# default: None
def DJANGO_SH_HOOK_GET_IMPORTED_OBJECTS(imported_objects: dict, options: dict) -> None:
    multiplier = int(options.get('multiplier', 0))
    imported_objects['multiply'] = lambda x: x * multiplier


# Can be used to alter the command provided to `python manage.py sh -c '<command>'`
# default: None
def DJANGO_SH_HOOK_MODIFY_COMMAND(command: str) -> str:
    return f'start=time.time()\\n{command}\\nprint("Command took", time.time() - start, "seconds")'
```
