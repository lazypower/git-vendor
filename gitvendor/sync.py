from dirsync import sync
from git import Repo, Git
from helpers import is_repository_clean, is_path_sane
from helpers import is_repository_initialized, parse_omissions
from helpers import delete_file_or_directory
import logging
import os
from path import path
from tempfile import mkdtemp
log = logging.getLogger('git-vendor.sync')


def list_tags(repository):
    print "The following tags are available:"
    for tag in repository.tags:
        print "> {}".format(tag)

    export_tag = pick_tag(repository.tags)
    return export_tag


def pick_tag(tags):
    tag = None
    while tag not in tags:
        tag = raw_input("Which tag would you like to vendor? ")
        if tag not in tags:
            log.error("{} is not an existing tag.".format(tag))
    return tag


def prep_export(tag, repository):
    tmpdir = mkdtemp()
    Repo.clone_from(repository.working_dir, tmpdir)
    log.debug('Cloned {} to {}'.format(repository.working_dir, tmpdir))
    clone = Git(tmpdir)
    clone.checkout(tag)
    log.debug('Checked out tag {}'.format(tag))
    return tmpdir


def overwrite_with_export(repo, output):
    repo = path(repo)
    output = path(output)
    if not os.path.exists(output):
        log.critical("Output dir does not exist: {}".format(output))
        create = raw_input("Shall I create the output directory? [N/y] ")
        if create is 'y' or create is 'Y':
            os.mkdir(output)
    sync(repo, output, 'sync')


def garbage_collection(tmpdir, repo):
    omissions = parse_omissions(repo.working_dir)
    log.debug("Omissions: {}".format(omissions))
    for f in omissions:
        garbage = os.path.join(tmpdir, f)
        delete_file_or_directory(garbage)


def run_export(repo, outdir=None):
    tag = list_tags(repo)
    log.debug('Target: {}'.format(tag))
    tmpdir = prep_export(tag, repo)
    garbage_collection(tmpdir, repo)
    overwrite_with_export(tmpdir, outdir)
    delete_file_or_directory(tmpdir)


def main(args, debug):
    if not args.repo:
        args.repo = '.'
    path = is_path_sane(args.repo)
    force = args.allow_dirty
    dirty = is_repository_clean(args.repo, force)
    initialized = is_repository_initialized(args.repo)

    if not path and not dirty:
        return 1

    if not initialized:
        log.warn("Directory: {} is not initialized. Perhaps you meant to"
                 " git-vendor init?".format(args.repo))
        return 1

    if not args.directory and not len(args.directory) == 0:
        print "no directory"
        return 1

    repository = Repo(args.repo)
    run_export(repository, args.directory)
