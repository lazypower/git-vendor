from git import Repo
import logging
import os

log = logging.getLogger('git-vendor.helpers')


def repository_sanity(directory):
    """ repository_sanity: predicate method for checking the status of a dirty'
    repository"""

    repo = Repo(directory)
    if repo.is_dirty():
        log.warn('Repository is dirty, doing nothing')
        return False
    return True


def is_path_sane(directory='.'):
    """ is_path_sane: predicate method for checking if we're pointed at a git
    repository"""

    if os.path.exists('.vendor-rc'):
        log.warn('Config exists, doing nothing')
        return False

    if not os.path.exists('.git'):
        log.warn('Not a git repository, doing nothing')
        return False
    return True
