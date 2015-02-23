from gitvendor import helpers
from mock import MagicMock, patch, Mock
import tempfile
import shlex
import shutil
from subprocess import call


class TestHelpers():

    @classmethod
    def setup_class(cls):
        cls.repodir = tempfile.mkdtemp()
        call(shlex.split("git clone "
                         "https://github.com/chuckbutler/git-vendor.git {}"
                         .format(cls.repodir)))
        cls.repo = cls.repodir
        cls.no_repo = tempfile.mkdtemp()

    # TODO: teardown_class (remove tmp files and be tidy)
    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.repodir)
        shutil.rmtree(cls.no_repo)

    @patch('gitvendor.helpers.Repo.is_dirty')
    def test_repository_clean(self, repomock):
        repomock.return_value = False
        ret = helpers.is_repository_clean(self.repo)
        assert repomock.is_dirty.called_once()
        assert ret is True

    @patch('gitvendor.helpers.Repo.is_dirty')
    def test_repository_dirty(self, repomock):
        repomock.return_value = True
        ret = helpers.is_repository_clean(self.repo)
        assert repomock.is_dirty.called_once()
        assert ret is False

    @patch('logging.getLogger')
    @patch('os.path.exists')
    def test_not_git_repository_sanity(self, pathmock, logmock):
        pathmock.return_value = False
        ret = helpers.is_path_sane(self.no_repo)
        assert pathmock.called_with('.git')
        assert logmock.warn.called_with('Not a git repository, doing nothing')
        assert ret is False

    @patch('logging.getLogger')
    @patch('gitvendor.helpers.is_repository_initialized')
    def test_initialized_repository_sanity(self, initmock, logmock):
        initmock.return_value = True
        ret = helpers.is_path_sane(self.repo)
        assert logmock.warn.called_with('Config exists, doing nothing')
        assert ret is False

    @patch('gitvendor.helpers.is_repository_initialized')
    def test_clean_repository_sanity(self, initmock):
        initmock.return_value = False
        ret = helpers.is_path_sane(self.repo)
        assert ret is True


