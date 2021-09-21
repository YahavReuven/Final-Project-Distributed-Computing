
import importlib

# TODO: allow to work with third library
def import_modules(cls, modules: list):
    """

    Note:
        cls should only be a parallel class.
    Args:
        cls:

    Returns:

    """
    fn = cls.parallel_func
    for i in modules:
        try:
            module = importlib.import_module(i)
        except ModuleNotFoundError:
            print("third library is not supported yet!")
        fn.__globals__.update({i: module})




