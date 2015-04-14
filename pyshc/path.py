import os
import os.path


def find(name):
    """Search for :name: in PATH

    :param name: the command to search for
    :returns: presence of :name: in PATH
    :rtype: bool
    """

    PATH = os.environ['PATH']
    for directory in PATH.split(':'):
        path = os.path.join(directory, name)
        if os.path.exists(path):
            return True
    return False
