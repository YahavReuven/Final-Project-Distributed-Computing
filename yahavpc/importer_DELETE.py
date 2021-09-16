import importlib

def importee(*modules):
    def decorating(fn):
        def inner(*args, **kwargs):
            for i in modules:
                module = importlib.import_module(i)
                fn.__globals__.update({i: module})
            return fn(*args, **kwargs)
        return inner
    return decorating