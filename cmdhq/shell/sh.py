
from commands import Command
from subprocess import CalledProcessError
import sys


class Sh(Command):
    "Call commands as if they were functions"

    def __init__(self, *args, **kws):
        kws['capture_stdout'] = True
        kws['capture_stderr'] = True
        super(Sh, self).__init__(*args, **kws)

    def __call__(self, *args, **kws):
        """The result is the stdout output of the command.  If the subprocess
        returns a non-zero exit code then CalledProcessError is
        thrown.  The stderr will be available as the output attribute
        of the exception instance.  :returns: stdout of the command
        :rtype: string

        """

        out, err, ret, args = super(Sh, self).__call__(*args, **kws)

        if ret is not 0:
            raise CalledProcessError(ret, str(args), output=err.read().strip())

        for line in err:
            sys.stderr.write(line)

        return out.read().strip()
