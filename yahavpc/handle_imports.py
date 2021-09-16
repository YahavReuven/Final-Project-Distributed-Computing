
import importlib

# TODO: maybe change
def validate_builtins(modules: list):
    for module in modules:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            raise ModuleNotFoundError

