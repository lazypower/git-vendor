from git import Repo
import logging
import os
import shutil
import yaml

log = logging.getLogger('git-vendor.helpers')


def is_repository_clean(directory, force):
    """ repository_sanity: predicate method for checking the status of a dirty'
    repository"""

    repo = Repo(directory)
    if repo.is_dirty() and not force:
        log.warn('Repository is dirty, doing nothing')
        return False
    return True


def is_path_sane(directory='.'):
    """ is_path_sane: predicate method for checking if we're pointed at an
    uninitialized git repository"""

    if not os.path.exists('.git'):
        log.warn('Not a git repository, doing nothing')
        return False

    if is_repository_initialized(directory):
        log.warn('Config exists, doing nothing')
        return False
    return True


def is_repository_initialized(directory):
    """ predicate method to determine if directory is initialized for
    vendoring"""
    return os.path.exists(os.path.join(directory, '.vendor-rc'))


def parse_omissions(directory):
    """ return list of omissions """
    with open(os.path.join(directory, '.vendor-rc'), 'r') as f:
        omissions = yaml.safe_load(f.read())
    return omissions['omit']


def delete_file_or_directory(directory):
    if os.path.exists(directory):
            if os.path.isdir(directory):
                # delete folder
                shutil.rmtree(directory)
                log.debug("Removed {}".format(directory))
            else:
                # delete file
                os.remove(directory)
                log.debug("Removed {}".format(directory))
    else:
        log.debug("{} not found".format(directory))
