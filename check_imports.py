import pkgutil
import importlib
import sys
import app

def load_all_modules(pkg):
    for importer, modname, ispkg in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
        try:
            importlib.import_module(modname)
        except Exception as e:
            print(f'Error importing {modname}: {type(e).__name__} - {e}')

load_all_modules(app)
