from path import find
import unittest


class TestPath(unittest.TestCase):
    def test_find_in_path_fail(self):
        "Test that a nonexistent command should not be found"
        name = "this_does_not_exist_000000000000000000000000"
        found = find(name)
        self.assertFalse(found)

    def test_find_in_path_success(self):
        "Test that an existing command should be found"
        name = 'env'
        found = find(name)
        self.assertTrue(found)
