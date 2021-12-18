
import importlib

# TODO: allow to work with third library
def import_modules(obj, modules: list, *functions):
    """

    Note:
        cls should only be a parallel class.
    Args:
        obj:

    Returns:

    """
    for i in modules:
        try:
            module = importlib.import_module(i)
        except ModuleNotFoundError:
            print("third party library is not supported yet!")
        for fn in functions:
            if fn:
                fn.__globals__.update({i: module})
