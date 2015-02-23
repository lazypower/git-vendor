from gitvendor import init
from mock import MagicMock, patch, Mock
import os
import pytest
from subprocess import call
import shlex
import shutil
import sys
import tempfile


class TestInit():

    @classmethod
    def setup_class(cls):
        cls.tmpdir = tempfile.mkdtemp()
        call(shlex.split("git clone "
                         "https://github.com/chuckbutler/git-vendor.git {}"
                         .format(cls.tmpdir)))
        cls.args = MagicMock()
        cls.args.repo = cls.tmpdir

    # TODO: teardown_class (remove tmp files and be tidy)
    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.tmpdir)

    def test_main_with_init(self):
        '''
            Test init with a basic set of arguments
        '''
        init.main(self.args, None)

    @patch('gitvendor.init.render_template')
    def test_main_with_dirty(self, rendermock):
        '''
            The init method should work regardless of repository state
        '''
        call(shlex.split("touch {}{}foobar".format(self.tmpdir, os.path.sep)))
        init.main(self.args, None)
        assert not rendermock.called

    @patch('gitvendor.init.render_template')
    def test_main_with_insane(self, rendermock):
        '''
            The init method should work regardless of repository state
        '''
        args = MagicMock()
        args.repo = '/tmp/foobarbazdoesnotexist'
        with pytest.raises(Exception):
            init.main(args, None)
            assert not rendermock.called

    @patch('gitvendor.helpers.is_repository_initialized')
    @patch('logging.getLogger')
    @patch('gitvendor.init.render_template')
    def test_main_already_initialized(self, rendermock,  logmock,  initmock):
        '''
            The method should not initialize a repository that has already
            been initialized
        '''
        initmock.return_value = True
        init.main(self.args, None)
        assert logmock.called_with('Repository: {} already initialized. Doing'
                                   ' nothing'.format(self.args.repo))
        assert not rendermock.called

    # TODO: Refactor this, and refactor the render_template method
    # both are beastly and seem really messy
    # @patch('builtins.open' if sys.version_info > (3,) else '__builtin__.open')
    # def test_render(self, mock_open):
    #    mock_open.return_value.__enter__ = lambda s: s
    #    mock_open.return_value.__exit__ = Mock()
    #    init.render_template(self.args.repo)
    #    assert mock_open.return_value.write.called_once()


