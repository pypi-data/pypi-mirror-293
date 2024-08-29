import os
from typing import Tuple, Union
from django.core.management.base import BaseCommand
from django_shell_extended import settings


class Command(BaseCommand):
    help = "Like the 'shell' command but customizable. To find out more, see sh/settings.py"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        if settings.HOOK_ADD_ARGUMENTS:
            settings.HOOK_ADD_ARGUMENTS(parser)
        parser.add_argument('-c', '--command', type=str, help='A command that should be executed; closes shell afterwards.')

    def handle(self, *args, **options):
        shell = self.get_ipython(options)
        if not callable(shell):
            if shell:
                print(shell)
            print("Could not load IPython interactive Python environment.")
            return

        shell()

    def get_ipython(self, options):
        """starts the ipython session"""
        try:
            from IPython import start_ipython

            def run_ipython():
                self.get_imported_objects(options)

                argv = ['--no-confirm-exit']
                command = options.get('command')
                if command is not None:
                    print(command)
                    if settings.HOOK_MODIFY_COMMAND:
                        command = settings.HOOK_MODIFY_COMMAND(command)
                    argv += ['-c', command]

                ipythonDir = settings.IPYTHON_DIR
                if ipythonDir:
                    argv += ["--ipython-dir", ipythonDir]

                start_ipython(argv=argv, user_ns=self.imported_objects)

            return run_ipython
        except ImportError as e:
            return e

    def get_imported_objects(self, options):
        """imports objects as configured"""
        self.imported_objects = {}

        if settings.AUTO_IMPORT_MODELS:
            self.auto_import_models()

        for module, imports in settings.IMPORT_MODULES:
            self.importModule(module, imports)

        if settings.HOOK_GET_IMPORTED_OBJECTS:
            settings.HOOK_GET_IMPORTED_OBJECTS(self.imported_objects, options)

    def auto_import_models(self):
        """tries to autodetect packages and import their models"""
        for path in os.listdir():
            if os.path.isdir(path):
                try:
                    self.importModule(f'{path}.models', '*')
                except (ImportError, KeyError, ModuleNotFoundError, ValueError):
                    pass

    def importModule(self, module: str, imports: Union[str, Tuple[str], None]):
        """imports like `from {module} import {imports}`"""
        if imports is None:
            self.imported_objects[module] = __import__(module)
            print(f'>>> import {module}')
        else:
            imported = __import__(module, {}, {}, imports)
            if isinstance(imports, str):
                imports = (imports, )
            [self.imported_objects.update({k: getattr(imported, k)}) for k in dir(imported) if k in imports or '*' in imports]
            print(f'>>> from {module} import {", ".join(imports)}')
