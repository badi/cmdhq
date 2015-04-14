from sh import Sh, CalledProcessError
import unittest


class TestSh(unittest.TestCase):

    def test_default(self):
        "Default usage should work"
        sh = Sh('ls')
        out = sh()
        self.assertIsInstance(out, str)

    def test_error_raises(self):
        "Error on subprocess should raise exception with stderr as output"
        sh = Sh('which')

        with self.assertRaises(CalledProcessError):
            try:
                sh('this_command_does_not_exist_00000000000000000000000000000')
            except Exception, e:
                self.assertTrue(hasattr(e, 'output'))
                self.assertIsInstance(e.output, str)
                self.assertTrue(len(e.output) > 0)
                raise
