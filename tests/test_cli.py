from gitvendor import cli
from mock import patch
import pytest


class TestCLI():

    def test_empty_argument_exception(self):
        with pytest.raises(SystemExit):
            cli.main([])

    @patch('pkg_resources.require')
    def test_version(self, mock_package):
        with pytest.raises(SystemExit):
            cli.main(['version'])
            assert mock_package.called_with('git-vendor')

    @patch('importlib.import_module')
    def test_arg_parsing(self, import_mock):
        cli.main(['init'])
        assert import_mock.called_with('gitvendor.init')

    @patch('importlib.import_module')
    @patch('gitvendor.cli.setup_logging')
    def test_exit_exception_logging(self, log_mock, import_mock):
        import_mock.side_effect = Exception('boom')
        with pytest.raises(SystemExit):
            cli.main(['sync'])
            log_mock.assert_called_with('boom')


