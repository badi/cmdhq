from commands import Command
import gc
import os.path
import unittest


class TestCommandConstructor(unittest.TestCase):

    def test_existing_command(self):
        "The command should exist"
        Command('ls')
        Command('/usr/bin/env')


class TestCommandCall(unittest.TestCase):

    def test_default(self):
        "default usage"
        cmd = Command('ls')
        out, err, ret, args = cmd()

        self.assertIsNotNone(out)
        self.assertIsNotNone(err)
        self.assertIs(ret, 0)
        self.assertEqual(len(args), 1)

    def test_intermediate_files_cleaned_close(self):
        "Intermediate files should be removed after closing"
        cmd = Command('ls')
        out, err, ret, args = cmd()

        tmps = [out, err]
        for tmp in tmps:
            self.assertTrue(os.path.exists(tmp.name))
            tmp.close()
            self.assertFalse(os.path.exists(tmp.name))

    def test_intermediate_files_cleaned_gc(self):
        "Intermediate files should be removed after GC"
        def inner_scope():
            cmd = Command('ls')
            out, err, ret, args = cmd()

            tmps = [out, err]
            for tmp in tmps:
                self.assertTrue(os.path.exists(tmp.name))

            paths = [tmp.name for tmp in tmps]
            return paths

        paths = inner_scope()
        gc.collect()
        for p in paths:
            self.assertFalse(os.path.exists(p))

    def check_capture(self, capture_stdout=False, capture_stderr=False):
        "Test behavior of stdout and stderr capturing"

        cmd = Command('ls',
                      capture_stdout=capture_stdout,
                      capture_stderr=capture_stderr)
        out, err, ret, args = cmd()

        tmps = []
        if capture_stdout:
            self.assertIsNotNone(out)
            tmps.append(out)
        if capture_stderr:
            self.assertIsNotNone(err)
            tmps.append(err)

        self.assertIs(ret, 0)

        for tmp in tmps:
            self.assertTrue(os.path.exists(tmp.name))
            tmp.close()
            self.assertFalse(os.path.exists(tmp.name))

    def test_capture_stdout(self):
        "Capture stdout"
        self.check_capture('stdout')

    def test_capture_stderr(self):
        "Capture stderr"
        self.check_capture('stderr')

    def test_string_args(self):
        "String arguments should be accepted"
        cmd = Command('ls',
                      capture_stdout=True,
                      capture_stderr=True)
        out, err, ret, args = cmd('-lht')

    def test_list_args(self):
        "A list of arguments should be accepted"
        raise NotImplementedError

    def test_unknown_command(self):
        "Should throw an exception"
        cmd = Command('this_cmd_should_not_exist_0000000000000000000000000')
        with self.assertRaises(OSError):
            cmd()
