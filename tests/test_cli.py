import unittest

from mock import patch

class TestCLI(unittest.TestCase):
    @patch('sys.exit')
    def test_main_args(self, mexit):
        # self.assertEqual(None, cli.main([]))
        pass
