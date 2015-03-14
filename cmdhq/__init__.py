import plugins

from loader import add_module as _add_module

_PLUGINS = plugins

if __name__ == '__main__':
    import sys
    import os
    name = sys.argv[1]

    try:
        paths = os.environ['CMDHQ_PLUGINS_PATH'].split(':')
    except KeyError:
        sys.stderr.write('CMDHQ_PLUGINS_PATH is not set\n')
        sys.exit(1)

    module = _add_module(_PLUGINS, name, paths)

    args = sys.argv[2:]
    module.main(args)
