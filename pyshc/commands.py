import shlex
import subprocess
import tempfile

import path


class Command(object):
    """This wraps functionality from the `subprocess` system library"""

    def __init__(self, name,
                 args=None,
                 bufsize=0,
                 capture_stdout=True,
                 capture_stderr=True):
        """Create a new shell command.

        The name is the command to be executed.
        Examples would be "ls", "echo", or "chmod".

        The name can be either the path to an executable or a name to
        search for in the PATH. If not found in PATH, an exception is
        thrown upon invocation.

        If :args: is provided, they will be prepended to all
        invocations. See the documentation for :__call__: for details
        on format and type.

        :param name: the name of the command
        :param args: arguments to add to all invocations
        :param bufsize: buffer size for output buffering
        :param capture_stdout: capture the stdout stream
        :param capture_stderr: capture the stderr stream

        """
        self._name = name
        self._args = args
        self._bufsize = bufsize
        self._capture_stdout = capture_stdout
        self._capture_stderr = capture_stderr

    def _format_args(self, args):
        """
        If :args: is a string:
        - parse using `shlex.split`

        if :args: is iterable:
        - each element is an argument

        :param args: string or iterable
        :returns: arguments to Popen
        :rtype: list
        """
        if args is None:
            args = list()

        if type(args) is str:
            cmd_args = shlex.split(args)
        else:
            cmd_args = []
            for a in args:
                cmd_args.append(a)

        return cmd_args

    def __call__(self, args=None):
        """Call a shell command with arguments.

        The `args` parameter should be either a string or
        an iterable of strings.

        If args is a string:

        - the arguments are parsed using the `shlex` module to
          create the arguments array to pass to the command.

        If args is an iterable:

        - each element must be a string
        - each element will be an argument to the command

        If captureing stdout or stderr, these will be returned as open
        file descriptors. This is in lieu of strings: the captureing
        is done by buffering in memory, and if the output is large
        this will cause problems. These file descriptors are to
        temporary files that will automatically be removed upon
        closing of the handle.

        :param args: the arguments to the command.
        :returns: the stdout, stderr, exit code, and calling parameters
        :rtype: (None or file, None or file, int, list of str)

        """

        if not path.find(self._name):
            raise OSError('Could not find command {}'.format(self._name))

        full_cmd = [self._name] \
            + self._format_args(self._args) \
            + self._format_args(args)

        # args to Popen
        kws = dict(bufsize=self._bufsize)

        if self._capture_stdout:
            stdout = tempfile.NamedTemporaryFile()
            kws['stdout'] = stdout
        else:
            stdout = None

        if self._capture_stderr:
            stderr = tempfile.NamedTemporaryFile()
            kws['stderr'] = stderr
        else:
            stderr = None

        proc = subprocess.Popen(full_cmd, **kws)

        try:
            proc.communicate()  # wait may deadlock, communicate will not
        except KeyboardInterrupt:
            proc.terminate()
            proc.kill()
            raise

        if stdout:
            stdout.seek(0)

        if stderr:
            stderr.seek(0)

        return stdout, stderr, proc.returncode, full_cmd
