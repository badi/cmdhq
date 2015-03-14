import imp
import os

def load_module(searchpath, name):
    try:
        fileobj, path, descr = imp.find_module(name, searchpath)

        # module found
        if path is not None:
            module = imp.load_module(name, fileobj, path, descr)
            return module

        else:
            raise Exception, 'Something bad happened when loading {} from {}'.format(name, searchpath)


    except ImportError:
        raise ImportError, 'No module name {} in path {}'.format(name, ':'.join(searchpath))

    finally:
        if fileobj is not None:
            fileobj.close()

def add_module(parent_module, name, searchpath):
    names = name.split('.')
    modules = []

    parent = parent_module
    path   = searchpath

    for name in names:
        module = load_module(path, name)

        setattr(parent, name, module)

        if hasattr(module, '__path__'):
            parent = getattr(parent, name)
            path   = module.__path__

    return module

